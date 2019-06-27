import smtplib, ssl
from email.mime.text import MIMEText
port = 465
fromEmail = "siimhackathonemail@gmail.com"
password = "SIIMHackathon2019"
MESSAGE = "AGGHGHH"
SERVER = "smtp.gmail.com"

def sendEmail(email,message,title = "Subject"):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SERVER,port,context=context) as server:
        server.login(fromEmail,password)
        message['Subject'] = title
        message["From"] = fromEmail
        message["To"] = email
        #server.sendmail(fromEmail,[email],message)
        server.send_message(message)
        print("Email complete!")
        
#sendEmail("peter1moras@gmail.com",MESSAGE)


# FROM = "sender@example.com"
# TO = ["peter1moras@gmail.com"] # must be a list

# SUBJECT = "Hello!"

# TEXT = "This message was sent with Python's smtplib."

# # Prepare actual message

# message = """\
# From: %s
# To: %s
# Subject: %s

# %s
# """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

# # Send the mail

# server = smtplib.SMTP(SERVER)
# server.sendmail(FROM, TO, message)
# #server.quit()