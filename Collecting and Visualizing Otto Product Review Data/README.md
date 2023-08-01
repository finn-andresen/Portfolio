# Collecting and Visualizing Otto Product Review Data


## Tools
- <b>PostgreSQL</b>: Database with two tables ("products" and "reviews")
- <b>Python (BeautifulSoup, psycopg2, TextBlob)</b>: Webscraping/Data Collection and Inserting into database
- <b>Power BI</b>: Data Import (PowerQuery) and Dashboard Creation


## Dataset
Using a Python program, product review data was read from the OTTO online shop and written to two tables ("products" and "reviews" ) of a PostgreSQL database via psycopg2 connector. The tables were exported from PostgreSQL as csv files and then imported into Power BI, where the original 1:n cardinality between "products" and "reviews" was restored in the Power BI data model. With this procedure, the Power BI file including the data model can be made available and viewed. The data contains information about all available men's football boots ([https://www.otto.de/herren/sportmode/sportschuhe/fussballschuhe/](https://www.otto.de/herren/sportmode/sportschuhe/fussballschuhe/)) and was collected on 30 July 2023.

### Table: "products"
- id: Product ID (<b>Primary Key</b>)
- name: Product name
- brand: Product brand name
- price: Product price as decimal value
- product_url: URL of the product page
- image_url: URL of the first image on the product page

### Table: "reviews"
- id: Review ID (<b>Primary Key</b>)
- created_at: Date and time of review creation
- location: Location of review author
- product_id: Product ID (<u>Foreign Key</u>)
- rating: Star rating (1 to 5)
- title: Review title, NULL if no written review
- text: Review text, NULL if no written review
- *polarity: Polarity score calculated with TextBlob, values between -1 (very negative sentiment) and 1 (very positive sentiment), NULL if no written review
- *subjectivity: Subjectivity score calculated with TextBlob, values between 0 (very objective) and 1 (very subjective), NULL if no written review

\*The polarity and subjectivity scores calculated with TextBlob consider both the review title and the review text, which are written in German language. Nonetheless the German extension TextBlobDE was not used, because it does not support subjectiity calculation. Therefore, the title and text were translated into English and then the scores were calculated.


## Goals
The dataset is intended to be used in a Power BI dashboard to allow users to interactively explore and analyze product and review data on offered football boots.

Users should ultimately be able to gain insights on questions like:
- Which brands are there? How many products do they have? How are they rated?
- How many ratings/reviews are there? Where do the reviewers live? Does the product price have an impact on the average ratiing?
- What is the connection between polarity and subjectivity score in terms of rating in reviews? Which keywords are most common in written reviews and might therefore be a valuable indicator for the rating?


## Results
The dashboard/Power BI file can be downloaded from the Files section of this README.

The final dashboard consists of three pages:
1. Brands and Products
1. Ratings
1. Reviews

### Brands and Products

![](<img/1 Brands and Products.png>)

Elements on this page:
- 3 <b>Cards</b> showing the number of brands, products and ratings
- <b>Bar chart</b> showing the number of products from each brand
- <b>Column chart</b> showing the number of ratings from all brands that have received at least 1 rating
- <b>Column chart</b> showing the average rating by brand. Only the 3 brands that have received more than 1 rating are shown. The red horizontal line shows the overall average rating (all brands, all products, all ratings) for comparison, regardless of the filter selected.

Clicking on one of the bars/columns will filter the page by the selected brand, showing the total number of ratings for this brand in the top right card. All other elements display information that has already been displayed without filtering.

### Ratings

![](<img/2-1 Ratings.png>)

Elements on this page:
- <b>Column chart</b> showing the number of each possible rating (1 to 5)
- <b>Column chart</b> showing the percentages of ratings that include a written review
- <b>Scatter chart</b> showing all products plotted by price and average rating. The bubble size is determined by the number of ratings. The brands in the legend can be used to filter the products by brand. Hovering over a bubble shows a custom tooltip depicting an image of the product, product id, price, number of ratings and average rating. ![](<img/2-2 Ratings Tooltip.png>)
- <b>Map</b> showing cities in Germany where the reviewers are located. The bubble size is determined by the number of ratings. It is colored blue if the average rating of the location is equal to or greater than the overall average rating that was already shown as the red horizontal line on the "Brands and Products" page. Otherwise, the bubble is colored orange. The location, number of ratings, average rating and overall average rating are displayed in the tooltip.

Clicking on one of the elements filters all other visuals on this page as well, e.g. filtering by brand "PUMA":
![](<img/2-3 Ratings Interactivity Brand.png>)

### Reviews
![](<img/3-1 Reviews.png>)

Elements on this page:
- <b>Scatter chart</b> showing all reviews plotted by polarity and subjectivity scores. All bubbles are colored by rating from 1 to 5. For each rating category there is also a trend line showing possible correlations between subjectivity and polarity.
- <b>Word cloud</b> of keywords that are most common in review titles.
- <b>Word cloud</b> of keywords that are most common in review texts.

Clicking on one of the elements filters all other visuals on this page as well, e.g. filtering by rating category "1":
![](<img/3-2 Reviews Interactivity Rating.png>)


## Files
Here is a list of all project files:
- [Otto Reviews.pbix](<Otto Reviews.pbix>): Power BI file including the dashboard pages and data model
- [otto-reviews.py](otto-reviews.py): Python script for collecting data and storing it in a PostgreSQL database
- [products.csv](products.csv): CSV file of the "products" table exported from PostgreSQL database
- [reviews.csv](reviews.csv): CSV file of the "reviews" table exported from PostgreSQL database