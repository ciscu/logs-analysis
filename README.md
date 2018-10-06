
# Logs Analysis

## introduction

Based on the data in the __news__ database it will output following analytics:
1. The 3 most popular articles.
2. The 4 most popular authors.
3. Days on which more than 1% of requests lead to errors.

Output can be found in the **output.txt** file.

## Usage

There are 2 ways to run this program:
1. Running the script using the Vagrant VM.
2. Installing all the dependencies locally.

### 1. Running the script using the Vagrant VM.

After satisfying all the prerequisites addressed below, you can follow these steps:

#### 1.1 Logging into the VM

##### 1.1.1 Start up the VM
by going into the `/vagrant` directory of the vm folder
and type following command:
```
Vagrant up
```
If this is the first time you run this command it can take some time.

##### 1.1.2 Connect to the VM
By typing the following command in the same `/vagrant`subdirectory:
```
Vagrant ssh
```
This will log your terminal in the running VM
It should look like this and your in your terminal:
```
vagrant@vagrant:~$
```
#### 1.2 Running the script

When logged in the VM run change directory to `/vagrant` and run:
```
python log-analysis.py
```
This will print the output as described above.


## Prerequisites

### 2.1 Downloading the nessecary files
2.1.1. Download and install [Vagrant](https://www.Vagrantup.com/downloads.html)          
2.1.2. Download and install [Virtualbox](https://www.virtualbox.org/wiki/Downloads)      
2.1.3 Download and unzip the Vagrant configuration files.

### 2.2 Setting up the VM
Like discribed in step 1.1.2.
In the terminal navigate to  `/vagrant` subdirectory of the VM folder
and type following command:
```
Vagrant up
```
This will download and install all the nessecary dependencies.

### 2.3 Connect to the VM
By typing the following command in the same `/vagrant`subdirectory:
```
Vagrant ssh
```

It should look like this and your in your terminal:
```
vagrant@vagrant:~$
```
### 2.4 Configuring the database

Before running the script we have to populate the database tables with some entries.

To do this run the following command:
```
vagrant@vagrant:~$ psql -d news -f newsdata.sql
```
### 2.3 Views

In order to run some of the queries we need to create 3 views.

#### 2.3.1 **errors** view

This view aggregates the "404 NOT FOUND" status codes per day from the log table.

RUN THIS IN THE TERMINAL:
```
CREATE VIEW errors AS
SELECT time::date, count(status) as not_found
FROM log
WHERE status = '404 NOT FOUND'
GROUP BY time::date
```

#### 2.3.2 **total_hits** views

This view aggregates all the hits on a day per day basis.

RUN THIS IN THE TERMINAL:
```
CREATE VIEW total_hits AS
SELECT time::date, count(status) as hits
FROM log
GROUP BY time::date;
```

#### 2.3.3 **error_stats** view

This view combines the previous views (errors and total_hits) to calculate the percentage of failed attempts to reach a page.

RUN THIS IN THE TERMINAL:
```
CREATE VIEW error_stats AS
SELECT total_hits.time, total_hits.hits, errors.not_found, round(((not_found/hits::decimal)*100), 1) as perc
FROM total_hits, errors
WHERE total_hits.time = errors.time
ORDER BY not_found DESC;
```
