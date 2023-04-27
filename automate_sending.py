import smtplib
import os
import schedule
import time
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from decouple import config


logging.basicConfig(filename='email_report.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


def send_email(recipient, subject, body, attachment):
    try:
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(config('EMAIL_FROM'), config('EMAIL_PASS'))
        
        
        msg = MIMEMultipart()
        msg['From'] = config('EMAIL_FROM')
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        
        with open(attachment, 'rb') as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(attachment))
        part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(attachment)
        msg.attach(part)
        
        
        server.sendmail(config('EMAIL_FROM'), recipient, msg.as_string())
        logging.info(f"Email sent to {recipient}")
        print(f"Email sent to {recipient}")
        server.quit()
        
    except Exception as e:
        logging.error(f"Error sending email to {recipient}: {str(e)}")
        
        
def send_daily_reports():
    
    recipients = [config('EMAIL_TO')]
    
    report_file = 'report.pdf'
    
    for recipient in recipients:
        subject = 'Daily Report'
        body = 'Your daily report.'
        attachment = report_file
        send_email(recipient, subject, body, attachment)


schedule.every().day.at("09:00").do(send_daily_reports)
# schedule.every(300).seconds.do(send_daily_reports)

while True:
    schedule.run_pending()
    time.sleep(1)