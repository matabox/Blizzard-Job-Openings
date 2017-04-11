# Blizzard-Job-Openings
## bliz_jobs.py
Downloads all information about new Blizzard Job Openings and sends an email notification

Usage
```
python bliz_jobs.py
```

This creates foders for the corresponding roles (e.g. security). If the script finds a new job it will download all information associated with the job and create a .html and .pdf file in this directory. It will then email the details. Example output below:
```
To: <mailbox>@<domain>
From: <mailbox>@<domain>
Subject: Blizzard Job Openings 2017-04-09

Hi <mailbox>@<domain>,

The following new jobs have opened at Blizzard:

Security
	Date: 2017-04-09
	Job Opening: Manager, Event Security
	Link: https://careers.blizzard.com/en-us/openings/o1lS4fw2

	Date: 2017-04-09
	Job Opening: Manager, Incident Response
	Link: https://careers.blizzard.com/en-us/openings/oyE14fw1
```
