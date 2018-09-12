import DatabaseConnector
import NewsNow
import ThreatPost
import mysql.connector.errors
from sys import argv

# inputs - will need to update to pull from configuration file
host = "seitux2.adfa.unsw.edu.au"  # Database host
user = "z5109589"  # Username
password = "mysqlpass"  # Password
db = "project"  # Database Name

# Initialise the database connector.
Database = DatabaseConnector.DatabaseConnector(host, user, password, db).connect()
# Initialise a cursor for interaction with the MYSQL database
cursor = Database.cursor()

# Initialise the scraper for NewsNow.
NewsNowScraper = NewsNow.NewsNowScraper(argv[1])
# Initialise the scraper for ThreatPost
ThreatPostScraper = ThreatPost.ThreatPostScraper(argv[1])

stories = NewsNowScraper.run()

# SQL query used to insert the stories into the database.
sql_query = "INSERT INTO Scrape_Data (source, content, date_time, link, keywords) " \
            "VALUES (%s, %s, %s, %s, %s)"

total = 0  # total stories added to the database.

# Iterates through the list of stories, processing each story and inserting it into the database.
for story in stories:
    try:
        cursor.execute(sql_query, story)  # Add the story to the database using the query and list of inputs
        Database.commit()  # commit the changes to the database.
        total += 1  # increase total stories added to the database.

    # In the case where the story content is not unique:
    # - if the source, content and keyword are the same -> discard
    # - if the source and content are the same but the keyword is different -> add the keyword to the existing entries
    #   list of keywords
    except mysql.connector.errors.IntegrityError:
        like_clause = "%" + argv[1] + "%"  # Used to check if the keyword is already in the list of keywords.
        # SQL update statement
        sql_update = "UPDATE Scrape_Data " \
                     "SET keywords = CONCAT(keywords, \", \", %s) " \
                     "WHERE content = %s && " \
                     "source = %s && " \
                     "keywords NOT LIKE %s;"
        update_vals = (story[4], story[1], story[0], like_clause)  # Values to be used in the update statement.
        cursor.execute(sql_update, update_vals)  # Execute the update.

print(total, " entries added to the Database.")  # Print total entries added to the database.
print(len(stories) - total, " duplicate(s) discarded.")  # Prints the total duplicates that have been discarded.



