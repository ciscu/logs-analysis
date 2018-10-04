#!/usr/bin/env python2

import psycopg2

 
# 1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.
# "Princess Shellfish Marries Prince Handsome" - 1201 views
# "Baltimore Ravens Defeat Rhode Island Shoggoths" - 915 views
# "Political Scandal Ends In Political Scandal" - 553 views


# 2. Who are the most popular article authors of all time? 

# 3. On which days did more than 1% of requests lead to errors? 


#Database Name
dbname = "news"

# Task 1
def mostPopularArticles():	
	# Connect to the database
	db = psycopg2.connect(dbname=dbname)
	c = db.cursor()

	#Query to be executed against the database
	query = """
	SELECT title, hits
	FROM articles, (SELECT count(path) as hits, path as ref FROM log GROUP BY path ORDER BY hits DESC LIMIT 3 OFFSET 1) as page_visit_count
	WHERE ref like '%' || slug || '%'
	ORDER BY hits DESC;
	"""

	#Run the query against the database
	c.execute(query)
	
	#Get the query results
	results = c.fetchall()

	#Loop over the results and print them out in the format specified
	print("The 3 most popular articles:")
	for title, hits in results:
		print("{} - {} views").format(title, hits)

	#Close the connection to the database	
	db.close()
	print

# Task 2
def mostPopularAuthors():
	# Connect to the database
	db = psycopg2.connect(dbname=dbname)
	c = db.cursor()
	
	#Query to be executed against the database
	query = """
	SELECT authors.name, sum(hits) as Total
	FROM articles, authors ,(SELECT count(path) as hits, path as ref FROM log GROUP BY path ORDER BY hits DESC LIMIT 4 OFFSET 1) as topThree
	WHERE authors.id = articles.author
	AND ref like '%' || slug || '%'
	GROUP BY authors.name
	ORDER BY Total DESC;
	"""
	#Run the query against the database
	c.execute(query)

	#Get the query results
	results = c.fetchall()
	
	#Loop over the results and print them out in the format specified
	print("The 4 most popular Authors:")
	for name, hits in results:
		print("{} - {} views").format(name, hits)
	
	#Close the connection to the database
	db.close()

	print

# Task 3
def failPercentage():
	# Connect to the database
	db = psycopg2.connect(dbname=dbname)
	c = db.cursor()

	#Query to be executed against the database
	query = """
	SELECT TO_CHAR(time::date, 'Mon dd, yyyy') as date, perc
	FROM error_stats
	WHERE perc > 1;
	"""

	#Run the query against the database
	c.execute(query)

	#get the result
	results = c.fetchall()
	
	#Print the result
	print("Days on which more than 1% of requests lead to errors:")
	for date, percetage in results:
		print("{} - {} % errors").format(date, percetage)

	#Close the connection to the database
	db.close()

def main():
	mostPopularArticles()
	mostPopularAuthors()
	failPercentage()

if __name__ == "__main__":
	main()