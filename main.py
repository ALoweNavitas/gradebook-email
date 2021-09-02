from selenium import webdriver
import smtplib
import zipfile
import glob
import os
import time
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from datetime import datetime
import logevent

# Sets the default directory for the batch file.
dir = os.chdir(r'C:\Users\adam_\Documents\GitHub\Navitas\gradebook-email')

# Datetime for email subject
date = datetime.now()
d = date.strftime('%d/%m/%Y')
t = date.strftime('%H:%M:%S')

# Variables
globbedFiles = glob.glob('*.xlsx')
NAV_USER = os.environ.get('NAV_USER')
NAV_PASS = os.environ.get('NAV_PASS')
emailAddress = os.environ.get('EMAIL_USER')
emailPassword = os.environ.get('EMAIL_PASS')

try:
    os.remove('gradebookExports.zip')
    for files in globbedFiles:
        os.remove(files)
except:
    pass

# Call the web browser
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : r'C:\Users\adam_\Documents\GitHub\Navitas\gradebook-email'} # Changes the download directory
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument("--window-size=1920, 1080")
chrome_options.add_argument("--headless")
path = r'C:\Users\adam_\Documents\GitHub\Navitas\gradebook-email\chromedriver.exe'
browser = webdriver.Chrome(path, options=chrome_options)

# Create Zip
gradebookZip = zipfile.ZipFile('gradebookExports.zip', 'w') # Creates a zip

# URL list
with open('URLs.txt') as x:
    urls = x.read().splitlines()

# Login
try:
    browser.get('https://campusonline.uk.sae.edu')
    browser.find_element_by_css_selector('#username').send_keys(NAV_USER)
    browser.find_element_by_css_selector('#password').send_keys(NAV_PASS)
    browser.find_element_by_css_selector('#submit').click()
    for x in urls:
        browser.get(x)
        browser.find_element_by_id('id_submitbutton').click()
except Exception as error: 
    logevent.logEvent.failLog(error)
    browser.quit()
    sys.exit()

time.sleep(10) # Allow time for all the files to download

# Create list of the downloaded files & zip them
gradebookFiles = [x for x in glob.glob('*.xlsx')]
for x in gradebookFiles: 
    gradebookZip.write(x)
    os.remove(x)

gradebookZip.close()
browser.quit()

# Email bit
msg = MIMEMultipart()
body_part = MIMEText('Hi both,\n\nPlease note this is an automated message.\n\nHere are the latest gradebook exports, downloaded at %s on %s.\n\nThanks,' % (t, d), 'plain')
msg['Subject'] = '%s %s : Latest Gradebook Export' % (d, t)
msg['From'] = emailAddress
recipients = ['a.lowe@sae.edu','d.ashman@sae.edu', 'eb.hill@sae.edu']
msg['To'] = ", ".join(recipients)
msg.attach(body_part)

with open('gradebookExports.zip', 'rb') as zip:
    msg.attach(MIMEApplication(zip.read(), name='gradebookExports.zip'))

# Send the email
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(emailAddress, emailPassword)
        smtp.send_message(msg)
except Exception as error:
    logevent.logEvent.failLog(error)
    sys.exit()

logevent.logEvent.successLog()
sys.exit()
