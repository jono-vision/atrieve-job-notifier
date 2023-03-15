import smtplib, toml
from pathlib import Path
from email.mime.text import MIMEText

config_file_path = Path(__file__).resolve().parent.parent / "config.toml"
# Load school board information
with open(config_file_path, "r") as file:
    config_data = toml.load(file)

smtp_server = config_data['email']['smtp_server']
smtp_port = config_data['email']['smtp_port']
email_from = config_data['email']['emailfrom']
email_password = config_data['email']['password']
email_to = config_data['email']['emailto']
mobile_number = config_data['email']['mobile_number']

def _message_maker(jobs):
    message_str = ""
    sms_message_str = ""
    for _, value in jobs.items():
        message_str += f"{value['subject']} @ {value['location']} ({value['board']})\n"
        sms_message_str += f"{value['subject']} @ {value['location']} ({value['board']})\n"
        message_str += f"Time: {value['starttime']} - {value['endtime']}\n"
        sms_message_str += f"Time: {value['starttime']} - {value['endtime']}\n"
        message_str += f"Date: {value['startdate']} - {value['enddate']}\n"
        sms_message_str += f"Date: {value['startdate']} - {value['enddate']}\n\n"
        message_str += f"Link: {value['link']}\n\n"
    messages = {'email': MIMEText(message_str),
                'sms': MIMEText(sms_message_str)}
    return messages


def send_email(jobs, email_to=email_to, email_from=email_from, email_password=email_password, mobile_number=mobile_number):
    messages = _message_maker(jobs)
    messages['email']['Subject'] = f"{len(jobs.keys())} New Teaching Job(s) Available On Atrieve"
    messages['sms']['Subject'] = ''

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_from, email_password)
            server.sendmail(email_from, email_to, messages['email'].as_string())
            server.sendmail(email_from, mobile_number, messages['sms'].as_string())
            print("Messages sent successfully!")
            server.quit()
    except Exception as e:
        print("An error occurred while sending the email:", e)
