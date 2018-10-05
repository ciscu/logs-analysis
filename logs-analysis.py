#!/usr/bin/env python2.7

import psycopg2

# Database Name
DBNAME = "news"


def connect():
    """
    Create a connection to the database, defined by DBNAME,
    and return the database connection and cursor.

    Returns:
    db, c - a tuple. The first element is a connection to the database.
    The second element is a cursor for the database.
    """
    try:
        db = psycopg2.connect(dbname=DBNAME)  # Connect to database
        c = db.cursor()  # Create cursor
        return db, c
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


# Task 1
def mostPopularArticles((db, c)):
    '''
    Queries the database for the 3 most popular articles.
    Prints line by line, formating: title and views.
    '''

    # Query to be executed against the database
    query = """
    SELECT title, hits
    FROM articles,
        (SELECT count(path) as hits, path as ref
        FROM log
        GROUP BY path
        ORDER BY hits DESC
        LIMIT 3
        OFFSET 1) as page_visit_count
    WHERE ref like '%' || slug || '%'
    ORDER BY hits DESC;
    """

    # Run the query against the database
    c.execute(query)

    # Get the query results
    results = c.fetchall()

    # Loop over the results and print them out in the format specified
    print("The 3 most popular articles:")
    for title, hits in results:
        print("{} - {} views").format(title, hits)

    # Close the connection to the database
    db.close()
    print


# Task 2
def mostPopularAuthors((db, c)):
    '''
    Queries the database for the 4 most popular authors.
    Prints line by line, formating: author, views.
    '''
    # Query to be executed against the database
    query = """
    SELECT authors.name, sum(hits) as Total
    FROM articles, authors,
        (SELECT count(path) as hits, path as ref
        FROM log
        WHERE status = '200 OK' --  Only query succesfull connections
        GROUP BY path
        ORDER BY hits DESC
        OFFSET 1) as topAricles
    WHERE authors.id = articles.author
    AND ref like '%' || slug || '%'
    GROUP BY authors.name
    ORDER BY Total DESC
    LIMIT 4;
    """
    # Run the query against the database
    c.execute(query)

    # Get the query results
    results = c.fetchall()

    # Loop over the results and print them out in the format specified
    print("The 4 most popular Authors:")
    for name, hits in results:
        print("{} - {} views").format(name, hits)

    # Close the connection to the database
    db.close()
    print


# Task 3
def failPercentage((db, c)):
    '''
    Queries the database for dates where the error percentrange above 1.
    Prints line by line, formating: date, percentage.
    '''

    # Query to be executed against the database
    query = """
    SELECT TO_CHAR(time::date, 'Mon dd, yyyy') as date, perc
    FROM error_stats
    WHERE perc > 1;
    """

    # Run the query against the database
    c.execute(query)

    # Get the result
    results = c.fetchall()

    # Print the result
    print("Days on which more than 1% of requests lead to errors:")
    for date, percetage in results:
        print("{} - {}% errors").format(date, percetage)

    # Close the connection to the database
    db.close()


def main():
    mostPopularArticles(connect())
    mostPopularAuthors(connect())
    failPercentage(connect())


if __name__ == "__main__":
    main()
