import DatabaseConnector
import NewsNow
import ThreatPost
import mysql.connector.errors
import time
import multiprocessing

# inputs - will need to update to pull from configuration file
host = "seitux2.adfa.unsw.edu.au"  # Database host
user = "z5109589"  # Username
password = "mysqlpass"  # Password
db = "project"  # Database Name


def run(keyword):

    # Initialise the database connector.
    Database = DatabaseConnector.DatabaseConnector(host, user, password, db).connect()
    # Initialise a cursor for interaction with the MYSQL database
    cursor = Database.cursor()

    # Initialise the scraper for NewsNow.
    NewsNowScraper = NewsNow.NewsNowScraper(keyword)
    # Initialise the scraper for ThreatPost
    ThreatPostScraper = ThreatPost.ThreatPostScraper(keyword)

    # Run NewsNow scraper to return stories
    NewsNow_stories = NewsNowScraper.run()
    # Run ThreatPost scraper to return stories
    ThreatPost_stories = ThreatPostScraper.run()

    # concatenate lists into one for insertion into database
    stories = NewsNow_stories + ThreatPost_stories

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
        # - if the source and content are the same but the keyword is different -> add the keyword to the existing
        # entries list of keywords
        except mysql.connector.errors.IntegrityError:
            try:
                like_clause = "%" + keyword + "%"  # Used to check if the keyword is already in the list of keywords.
                # SQL update statement
                sql_update = "UPDATE Scrape_Data " \
                             "SET keywords = CONCAT(keywords, \", \", %s) " \
                             "WHERE content = %s && " \
                             "source = %s && " \
                             "keywords NOT LIKE %s;"
                update_vals = (story[4], story[1], story[0], like_clause)  # Values to be used in the update statement.
                cursor.execute(sql_update, update_vals)  # Execute the update.
            except mysql.connector.errors.InternalError:
                print("FATAL ERROR: cannot resolve issue... moving on")
                continue

        except mysql.connector.errors.DatabaseError:
            print('Database Error. disgarded story: ', story)
            continue

    print(total, " entries added to the Database.")  # Print total entries added to the database.
    print(len(stories) - total, " duplicate(s) discarded.")  # Prints the total duplicates that have been discarded.

    Database.close()


keywords = ['Thailand', 'Vietnam', 'Japan', 'China', 'UK', 'France', 'Asia']


if __name__ == '__main__':
    start = time.time()

    pool = multiprocessing.Pool()
    pool.map(run, keywords)

    end = time.time()
    print(f"Time taken: {end-start:.2f} seconds")

'''
a = time.time()

for x in keywords:
    run(x)

b = time.time()

print(f'Time taken: {b-a:.2f} seconds')
'''