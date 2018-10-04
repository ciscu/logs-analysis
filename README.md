<!-- What steps need to be taken -->
<!-- What should the user already have installed -->
<!-- What might they have a hard time understanding -->
# Logs Analysis

Logs Anlysisis (**logs-analysis.py**) is a python2 script that runs three queries and displays the result directly to the standard output.

## Output

Based on the data in the __news__ database it will output following analytics:
1. The 3 most popular articles.
2. The 4 most popular authors.
3. Days on which more than 1% of requests lead to errors.

Output can be found in the **output.txt** file.

## Prerequisits

In order to run the queries, 3 views must be created in the __news__ database before running the **logs-analysis.py** file

### 1. Log into the database

```
$ psql news
```

### 2. Creating the views

#### 2.1. **errors** view

This view aggregates the "404 NOT FOUND" status codes per day from the log table.

RUN THIS IN THE TERMINAL: 
```
$ CREATE VIEW errors AS
$ SELECT time::date, count(status) as not_found
$ FROM log
$ WHERE status = '404 NOT FOUND'
$ GROUP BY time::date
```

#### 2.2. **total_hits** views

This view aggregates all the hits on a day per day basis.

RUN THIS IN THE TERMINAL: 
```
$ CREATE VIEW total_hits AS
$ SELECT time::date, count(status) as hits
$ FROM log
$ GROUP BY time::date;
```

#### 2.3. **error_stats** view

This view combines the previous views (errors and total_hits) to calculate the percentage of failed attempts to reach a page.

RUN THIS IN THE TERMINAL:
```
$ CREATE VIEW error_stats AS
$ SELECT total_hits.time, total_hits.hits, errors.not_found, round(((not_found/hits::decimal)*100), 1) as perc
$ FROM total_hits, errors
$ WHERE total_hits.time = errors.time
$ ORDER BY not_found DESC;
```

## Running the script

When all the prerequisite are fulfilled you can simply run the script like so:
```
$ python logs-analysis.py 
```

## Under the hood

If you look into the script you will see that the 3 queries are run in seperate functions

Namely:
1. mostPopularArticles()
2. mostPopularAuthors()
3. failPercentage()

Each of these functions consits of the same steps.
1. Connecting to the database
2. Storing the SQL query in a variable named: ```query```
3. Execute the query against the connected database
4. Store the result in the variable ```results```
5. A for loop iterates over the results printing to the screen the result formatted as defined.


