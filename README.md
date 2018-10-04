## VIEWS
### Error view
This view is to aggregate the "404 NOT FOUND" status codes per day 

```
CREATE VIEW errors AS
SELECT time::date, count(status) as not_found
FROM log
WHERE status = '404 NOT FOUND'
GROUP BY time::date
```

### Total views
Total hits per day
```
CREATE VIEW total_hits AS
SELECT time::date, count(status) as hits
FROM log
GROUP BY time::date;
```

### Hits per day
A table view of all the total hits on the website, including the amount of errors in number and percentage

```
CREATE VIEW error_stats AS
SELECT total_hits.time, total_hits.hits, errors.not_found, round(((not_found/hits::decimal)*100), 1) as perc
FROM total_hits, errors
WHERE total_hits.time = errors.time
ORDER BY not_found DESC;
```