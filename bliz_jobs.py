#~/usr/bin/python

import requests
import re
import datetime
import pdfkit
import os
import smtplib
from email.mime.text import MIMEText

''' Output location '''
filePath = "/opt/scripts/utils/"

''' Blizzard Job Openings URL '''
url = "https://careers.blizzard.com/en-us/openings/partial?roles[]=%s&teams=&locations=&types=&search="
jobUrl = "https://careers.blizzard.com/en-us/openings/"

''' Nasty Regex '''
regexJobs = r'en-us\/openings\/([A-Za-z0-9]{8})\\" class=\\"Table-item Table-link is-link\\"><div class=\\"Table-column Table-headline is-wrapped is-firstMobile\\">([A-Za-z ,-]{0,100})<\/div>'
regexMetadata = r'Markup Markup--html">(.*)<\/div><div class="space-medium"><\/div><a href="https:\/\/app'
regexTitle = r'<title>(.*)<\/title>'

''' Job roles to search for '''
roles = ["security", "information-technology", "engineering"]

''' List used to save results '''
jobList = []

''' Today's date '''
foundDate = datetime.datetime.now()
date = foundDate.strftime("%Y-%m-%d")

''' Email variables '''
toAddr = "<mailbox>@<domain>"
fromAddr = "<mailbox>@<domain>"
smtpServer = "<smtpserver>"
username = "<username>"
password = "<password>"

def sendEmail(data):

	print "[+] Found data, sending email to %s" % (toAddr)

	''' Email body / subject '''
	emailBody = "Hi %s,\n\nThe following new jobs have opened at Blizzard:\n%s" % (toAddr, data)
	emailSubject = "Blizzard Job Openings %s" % (date)

	''' Email attributes '''
	msg = MIMEText(emailBody)
	msg["To"] = toAddr
	msg["From"] = fromAddr
	msg["Subject"] = emailSubject

        print msg
        
	s = smtplib.SMTP(smtpServer)
	''' Authenticate '''
	s.login(username, password)
	''' Send email '''
	s.sendmail(fromAddr, toAddr, msg.as_string())
	s.quit()	

if __name__ == '__main__':
	print "[!] Starting Blizzard Job Openings Download..."

	''' Perform the web request '''
        for role in roles:

            roleUrl = url % (role)

            r = requests.get(roleUrl)
            jobs = re.findall(regexJobs, r.text)

            ''' Check if see if directory exists '''
            if not os.path.exists(filePath + role):
                print "[!] Createing directory: %s" % (filePath + role)
                os.makedirs(filePath + role)
        
            for job in jobs:  
                path = filePath + role + "/" + job[0]
                if not os.path.exists(path + ".pdf"):
                    print "[*] Found new job, downloading info.. %s" % (job[1])

                    downloadUrl = jobUrl + job[0]

                    jobList.append([role, job[1], downloadUrl])

                    pdfkit.from_url(downloadUrl, path + ".pdf")

                    j = requests.get(downloadUrl)
                    metadata = re.findall(regexMetadata, j.text)
                    title = re.findall(regexTitle, j.text)
    
                    ''' Create / Open the html file '''
                    html = open(path + ".html", "w+")
                    html.write("<html><title>" + title[0] + "</title> <h2>" + title[0] + "</h2><body>" + metadata[0] + "</body></html>")
                    html.close()

                else:
                    print "[*] I've seen this job in the past.. skipping: %s" % (job[1])

        if jobList:
            role = ""
            message = ""

            ''' Get the data into a printable format '''
            for job in jobList:
                if job[0] != role:
                    message = message + "\n" + job[0].title()
                
                message = message + "\n\tDate: " + date
                message = message + "\n\tJob Opening: " +  job[1]
                message = message + "\n\tLink: " + job[2]
                message = message + "\n"

                role = job[0]

            ''' Send email '''
            sendEmail(message)

        else:
            print "[!] Blizzard job search didn't find anything new :("
