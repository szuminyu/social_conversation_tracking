import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from datetime import  date, datetime, timedelta
import time
import subprocess




class covid_email_alert:


    def send_email():

        #auth

        smtp_server = 'smtp-mail.outlook.com'
        smtp_port = 587
        smtp_username = your_username
        smtp_password = your_password

        email_to = email_to_people
        email_from = email_from_person
        email_subject = 'Coronavirus Monitoring Report, ' + str(date.today())


        email_space = ', '

        # send email
        msg = MIMEMultipart()
        msg['Subject'] = email_subject
        msg['TO'] = email_space.join(email_to)
        msg['From'] = email_from

        #body
        words = 'Coronavirus Media and Social Conversation Tracking Report'
        msg.attach(MIMEText(words, 'plain'))

        #file
        filename = 'COVID-19 Monitoring Report ' + str(date.today()) + '.pdf'
        attachment = open(filename, 'rb')
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        # Encode to base64
        encoders.encode_base64(part)
        # Add header
        part.add_header("Content-Disposition", f"attachment; filename= {filename}")
        #Add attachment to your message and convert it to string
        msg.attach(part)
        text = msg.as_string()

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(email_from, email_to, text)


if __name__ == '__main__':
    while True: 
        try: 
            t = datetime.today()
            
            #run the program at 9:15 during weekdays
            if t.hour == 9 and t.minute == 15 and t.weekday() != 5 and t.weekday() != 6:
                exec(open('prep_data.py').read())
                print('Read data')
                subprocess.call (['Rscript', '--vanilla', 'state_dma.r'])
                print('Read R and get the state map')
                exec(open('ppt.py').read())
                print('PPT is done. Now go adjust the subtitle and export to pdf in 5 minutes!')
                time.sleep(300) # 5 mins
                covid_email_alert.send_email()
                print('Email sent with pdf attached')
                future = datetime(t.year, t.month, t.day, 9, 15) + timedelta(days = 1)
                time.sleep((future-t).seconds)

            #before 9:15
            elif (t.hour < 9 or (t.hour == 9 and t.minute < 15)) and t.weekday() != 5 and t.weekday() != 6:
                print("Haven't 9:15 a.m.")
                future = datetime(t.year, t.month, t.day, 9, 15)
                time.sleep((future - t).seconds)

            else:
                print('Already pass 9:15 a.m. or not weekdays')
                future = datetime(t.year, t.month, t.day, 9, 15) + timedelta(days = 1)
                time.sleep((future - t).seconds)

        except: print('You just kill the program.')
