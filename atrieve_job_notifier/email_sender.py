import smtplib

def _message_maker(jobs):
    message = ""
    for _, value in jobs.items():
        message += f"Subject: {value['subject']}\n"
        message += f"Role: {value['role']}\n"
        message += f"Location: {value['location']}\n"
        message += f"Time: {value['starttime']} - {value['endtime']}\n"
        message += f"Date: {value['startdate']} - {value['enddate']}\n"
        message += f"Link: {value['link']}\n\n"
    return message


def send_email(jobs, email_to, email_from, email_from_password, email_cc=''):
    message = _message_maker(jobs)

    subject = f"{len(jobs.keys())} New Teaching Job(s) Available On Atrieve"
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(email_from, email_from_password)
        
        header = 'To:' + email_to + '\n' + 'Cc:' + email_cc + '\n' + 'Subject:' + subject + '\n'
        msg = header + '\n' + message + '\n\n'
        server.sendmail(email_from, [email_to, email_cc], msg)
        print("Email sent successfully!")
    except Exception as e:
        print("An error occurred while sending the email:", e)
    finally:
        server.quit()

