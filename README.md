
# Logs Analysis

## Introduction

This program runs some analysis queries from data in the fictional **news** database and prints it out to the terminal.

Based on the data in the __news__ database it will output following analytics:
1. The 3 most popular articles.
2. The 4 most popular authors.
3. Days on which more than 1% of requests lead to errors.

Output can be found in the **output.txt** file.

## Usage

In order to run the script you need to download and do some database configuration
first.
These steps are described in the **prerequisites** section.

Once all the prerequisites are satisfied you can run the script by following
these steps:

##### Starting up the VM
by going into the `/vagrant` directory of the vm folder
and type following command:
```
Vagrant up
```

##### Connect to the VM
Logging in the to the vm is really straight forward.
Type the following command in the  `/vagrant`subdirectory:
```
Vagrant ssh
```
This will log you in the VM.  
Your terminal prompt should look a this:
```
vagrant@vagrant:~$
```
#### Running the script

When logged in the VM run change directory to `/vagrant` and run:
```
python log-analysis.py
```
This will print the output as in the **output.txt** file.


## Prerequisites

### Downloading the nessecary files
Download and install [Vagrant](https://www.Vagrantup.com/downloads.html)          
Download and install [Virtualbox](https://www.virtualbox.org/wiki/Downloads)      
Download and unzip the Vagrant configuration files.

### Setting up the VM the for first time

In the terminal navigate to  `/vagrant` subdirectory of the VM folder
and type following command:
```
Vagrant up
```
This will download and install all the necessary dependencies.
It can take a couple of minutes.

### Connect to the VM
By typing the following command in the same `/vagrant` subdirectory:
```
Vagrant ssh
```

It should look like this and your in your terminal:
```
vagrant@vagrant:~$
```
### Configuring the database

Before running the script we have to populate the database tables with some entries.
To do this run the following command in the VM:
```
vagrant@vagrant:~$ psql -d news -f newsdata.sql
```
### Views

In order to run some of the queries we need to create 3 views.

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
