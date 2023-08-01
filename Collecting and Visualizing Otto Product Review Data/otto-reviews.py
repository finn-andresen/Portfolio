import requests
from bs4 import BeautifulSoup
import json
from textblob import TextBlob
import psycopg2
import hidden
import sys


def main():
    """Get product information and reviews (if exist)"""

    # Create tables in PostgreSQL database
    create_db_tables()

    # Connect to database for inserting data
    secrets = hidden.secrets()
    conn = psycopg2.connect(host=secrets["host"],port=secrets["port"], dbname=secrets["dbname"], user=secrets["user"], password=secrets["pass"])
    cur = conn.cursor()

    # Create list of all product URLs
    product_links = get_product_links()
    number_products = len(product_links)
    for link in product_links:
        print(link)

    collected_product_ids = []

    for i, product_link in enumerate(product_links):
        print(f"Starting product extraction: {i} of {number_products}")

        # Send a GET request to the URL
        response = requests.get(product_link)
        if response.status_code != 200:
            print(f"Error when accessing product page ({product_link}). Skipping product.")
            continue

        html_doc = response.text

        # Create a BeautifulSoup object from the HTML content
        soup = BeautifulSoup(html_doc, "html.parser")

        # Find the <script> element with id="product_data_json"
        script_element = soup.find("script", id="product_data_json")

        # Extract the content of the <script> element as a string
        script_content = script_element.string.strip()

        # Parse the JSON content within the <script> element
        product_data = json.loads(script_content)

        # Extract the required information
        product_url = product_data["offers"]["url"] # without variation id
        product_id = product_url.rsplit("-", 1)[1][:-1]
        # Different variations share the same product id and should therefore be skipped
        if product_id in collected_product_ids:
            print(f"Product ID {product_id} already extracted. Skip.")
            continue
        collected_product_ids.append(product_id)
        name = product_data.get("name")
        price = float(product_data["offers"]["price"])
        brand = product_data["brand"]["name"]
        image_url = product_data["image"]
        # Take first image if there are more than one
        if len(image_url) > 1:
            image_url = image_url[0]
        
        # Print the extracted information
        print("Extracted: Name:", name, "URL:", product_url, "Product ID:", product_id, "Price:", price, "Brand:", brand), "Image:", image_url

        # Insert data into products table
        sql = """
        INSERT INTO products (id, name, brand, price, product_url, image_url)
        VALUES (%s, %s, %s, %s, %s, %s);
        """

        cur.execute(sql, (product_id, name, brand, price, product_url, image_url))
        
        # Check if there are reviews (link to review page). Skip if none exist.
        reviews_exist = soup.find("div", class_="cr_aggregation")
        if reviews_exist is None:
            print("There are NO reviews.")
            continue
        else:
            print("There are reviews:")
            page_count = 1

            while True:
                # Create url to product review page
                url_review = f"https://www.otto.de/kundenbewertungen/{product_id}/?page={page_count}"

                # Send a GET request to the URL
                response = requests.get(url_review)
                if response.status_code != 200:
                    print(f"Error when accessing review page ({url_review}). Skipping reviews.")
                    break

                html_doc = response.text

                # Create a BeautifulSoup object from the HTML content
                soup = BeautifulSoup(html_doc, "html.parser")

                # Review pages
                try:
                    last_page = int(soup.find("span", class_="cr_paging__currentPage cr_js_paging__currentPage").text.split("/")[1])
                except AttributeError:
                    print(f"Couldn't find reviews for {url_review}")
                    break

                # Find all reviews per page
                reviews = soup.find_all(class_="cr_review cr_review-content cr_js_review")

                # Extract information for each review
                for review in reviews:
                    location = review.find("span", attrs={"data-qa": "cr-review-reviewerLocation"}).text
                    title = review.find("h4", class_="pl_headline50 pl_my25").text
                    text = review.find("span", attrs={"data-qa": "cr-review-text"}).text
                    date = review.get("data-review-creationdate")
                    review_id = review.get("data-review-id")
                    rating = int(review.get("data-review-rating"))

                    # Print the extracted information
                    print("Extracted: Review ID:", review_id, "Date:", date, "Location:", location, "Rating:", rating, "Title:", title, "Text:", len(text), "characters.")
                    
                    # Get polarity and subjectivity scores for written reviews
                    polarity_score = None
                    subjectivity_score = None
                    
                    if len(text) > 1:
                        blob_german = TextBlob(title + ". " + text)
                        try:
                            blob_english = blob_german.translate(from_lang="de", to="en")
                        except:
                            blob_english = blob_german
                        polarity_score = blob_english.sentiment.polarity
                        subjectivity_score = blob_english.sentiment.subjectivity

                    # Insert data into reviews table
                    sql = """
                    INSERT INTO reviews (id, created_at, location, product_id, rating, title, text, polarity, subjectivity)
                    VALUES (%s, TO_TIMESTAMP(%s, 'YYYY-MM-DD HH24:MI') AT TIME ZONE 'Europe/Berlin', %s, %s, %s, %s, %s, %s, %s);
                    """

                    cur.execute(sql, (review_id, date, location, product_id, rating, title, text, polarity_score, subjectivity_score))
                                
                if page_count >= last_page:
                    # conn.commit()
                    break
                else:
                    page_count += 1

    conn.commit()
    print("Extraction successful. Database updated.")
    cur.close()
    conn.close()


def get_product_links():
    """Storing all unique links from the product overview page in a list"""

    # Set url for product overview page and variables for iteration
    url_overview = "https://www.otto.de/herren/sportmode/sportschuhe/fussballschuhe/"
    product_links = []
    max_o_value = 0

    while True:
        # Send a GET request to the URL
        response = requests.get(url_overview)
        if response.status_code != 200:
            print(f"Error when accessing product overview page ({url_overview}).")
            sys.exit("Can't continue without list of product links.")

        html_doc = response.text

        soup = BeautifulSoup(html_doc, "html.parser")

        product_link_elements = soup.find_all("a", href=lambda href: href and href.startswith("/p/"))

        # Fill list with all product urls
        for element in product_link_elements:
            product_links.append("https://www.otto.de" + element.get("href"))

        # Find the <button> element with the data-page attribute
        button_element = soup.find_all("button", class_="js_pagingLink ts-link p_btn50--4th")[-1]

        if button_element is None:
            break

        # Extract the data-page attribute as a string
        data_page_attr = button_element["data-page"]

        # Parse the data-page attribute string as a JSON object
        data_page_json = json.loads(data_page_attr)

        # Retrieve the value associated with the key "o"
        o_value = data_page_json["o"]

        if int(o_value) > max_o_value:
            max_o_value = int(o_value)
        else:
            break

        url_overview = f"https://www.otto.de/herren/sportmode/sportschuhe/fussballschuhe/?l=gq&o={o_value}"

    # Remove duplicates
    product_links = list(dict.fromkeys(product_links))
    return product_links


def create_db_tables():
    """Prepare PostgreSQL database"""
    
    # Connect to database
    secrets = hidden.secrets()
    conn = psycopg2.connect(host=secrets["host"],port=secrets["port"], dbname=secrets["dbname"], user=secrets["user"], password=secrets["pass"])
    cur = conn.cursor()

    # Create table "products"
    sql = """
    DROP TABLE IF EXISTS products CASCADE;
    CREATE TABLE products (
        id TEXT UNIQUE,
        name TEXT,
        brand TEXT,
        price NUMERIC,
        product_url TEXT UNIQUE,
        image_url TEXT,
        PRIMARY KEY(id)
    );
    """

    cur.execute(sql)

    # Create table "reviews"
    sql = """
    DROP TABLE IF EXISTS reviews;
    CREATE TABLE reviews (
        id TEXT UNIQUE,
        created_at TIMESTAMPTZ,
        location TEXT,
        product_id TEXT REFERENCES products(id),
        rating SMALLINT,
        title TEXT,
        text TEXT,
        polarity NUMERIC,
        subjectivity NUMERIC,
        PRIMARY KEY(id)
    );
    """

    cur.execute(sql)

    # Commit changes and close connection
    conn.commit()
    cur.close()
    conn.close()
    print("Tables successfully created.")

if __name__ == "__main__":
    main()