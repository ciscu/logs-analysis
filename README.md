# Logs Analysis

## introduction

Based on the data in the __news__ database it will output following analytics:
1. The 3 most popular articles.
2. The 4 most popular authors.
3. Days on which more than 1% of requests lead to errors.

Output can be found in the **output.txt** file.

## Prerequisites

Here is a list of what is needed in order to run log-analysis.py.

### Software

#### Using the Vagrant VM

#### Manual setup

The script requires following software to be installed:
* Python 2.7
* PostgreSQL

### Importing the database

If you have not imported the database in PostgreSQL run this code in your terminal:
```
psql -d newsdata.sql
```

### Connecting to the database
```
 psql news
```
### Connecting to the database

### Views

In order to run some of the queries 3 views must be created.

#### **errors** view

This view aggregates the "404 NOT FOUND" status codes per day from the log table.

RUN THIS IN THE TERMINAL: 
```
CREATE VIEW errors AS
SELECT time::date, count(status) as not_found
FROM log
WHERE status = '404 NOT FOUND'
GROUP BY time::date
```

#### **total_hits** views

This view aggregates all the hits on a day per day basis.

RUN THIS IN THE TERMINAL: 
```
CREATE VIEW total_hits AS
SELECT time::date, count(status) as hits
FROM log
GROUP BY time::date;
```

#### **error_stats** view

This view combines the previous views (errors and total_hits) to calculate the percentage of failed attempts to reach a page.

RUN THIS IN THE TERMINAL:
```
CREATE VIEW error_stats AS
SELECT total_hits.time, total_hits.hits, errors.not_found, round(((not_found/hits::decimal)*100), 1) as perc
FROM total_hits, errors
WHERE total_hits.time = errors.time
ORDER BY not_found DESC;
```


