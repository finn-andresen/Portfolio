# Bundesliga Analysis Seasons 05/06 to 22/23

## Tools
- <b>Microsoft Excel</b>: Data Cleaning and Transformation (with PowerQuery)
- <b>Python (Pandas)</b>: Webscraping/Data Collection
- <b>Tableau</b>: Exploratory Analysis and Data Visualization

## Dataset
This project uses a CSV file from [Kaggle](https://www.kaggle.com/datasets/oles04/bundesliga-seasons?resource=download) about all football matches of the Bundesliga seasons 2005/2006 to 2022/2023 (see [bulidata.csv](bulidata.csv)).

## Goal
Bundesliga is the first German football division. At the end of the 22/23 season, FC Bayern Munich won the eleventh championship in a row. This raises the question of whether Bayern is just an "outlier" or whether the Bundesliga as a whole is becoming less and less exciting. Other interesting insights gained during the exploratory analysis should also be presented.

Two <b>main questions</b> should be addressed:
1. How have the results (wins, draws, losses) developed in the Bundesliga in recent years?
1. Is there a (noticeable) advantage for the home team?

The results should be presented in a <b>Tableau dashboard</b>. It should be suitable for three different kinds of users with different needs:
1. <u>General football enthusiast</u>: Wants to see interesting facts about football at a quick glance
1. <u>Bundesliga fan</u>: Wants to get details about the Bundesliga and likes to explore data on their own
1. <u>Fan of a specific club</u>: Is interested in his favorite Bundesliga team and would like to focus on them

## Files
Here is a list of all project files:
- [bulidata.csv](bulidata.csv): Raw data from Kaggle
- [Data Cleaning Steps v3.pdf](<Data Cleaning Steps v3.pdf>): PDF about all cleaning steps in Excel
- [Webscraping Bundesliga.ipynb](<Webscraping Bundesliga.ipynb>): Jupyter Notebook with Python script to scrape missing data and store it in an Excel file
- [Bundesliga - Data Transformation.xlsx](<Bundesliga - Data Transformation.xlsx>): Excel file containing multiple sheets showing the respective state of the data cleaning and transformation process
- [Bundesliga.xlsx](<Bundesliga.xlsx>): Excel file containing two sheets ("Matches" and "Teams") which are used as a data source in Tableau
- [Bundesliga Data Story.twbx](<Bundesliga Data Story.twbx>): Packaged Tableau Workbook with all sheets, dashboards and story
- [Bundesliga Data Story.pdf](<Bundesliga Data Story.pdf>): PDF of all Tableau data story points


## Preview
The project is available on Tableau Public in two different versions:
- [Annotated Data Story](https://public.tableau.com/app/profile/finn.andresen/viz/BundesligaDataStory/Multi-FrameDataStory)
- [Dashboards without annotations](https://public.tableau.com/app/profile/finn.andresen/viz/Bundesliga_16887328196010/BundesligaOverview)
