import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from Application.config import SMTPConfig


def sendMail(receiver_address, message_type='html',file_name='',html_message=''):
  try:
    sender_address = SMTPConfig.SENDER_ADDRESS
    sender_pass = SMTPConfig.SENDER_PASSWORD
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = "Monthly Report"
    
    
    if message_type=='html':
      message.attach(MIMEText("Please find the attached report for your purchases","plain"))
      message.attach(MIMEText(html_message,"html"))
    elif message_type=='pdf':
      message.attach(MIMEText("Please find the attached report for your purchases","plain"))
      
      with open(file_name, "rb") as f:
        attachment = MIMEApplication(
          f.read(),
          _subtype="pdf"
        )
      attachment.add_header('Content-Disposition','attachment',filename=str(file_name))
      # message.attach(MIMEApplication(open(file_name,"rb").read()))
      message.attach(attachment)
    
    else:
      message.attach(MIMEText("No purchases for this month","plain"))  
    
    
    session = smtplib.SMTP(
      host=SMTPConfig.SMPTP_SERVER_HOST,
      port=SMTPConfig.SMPTP_SERVER_PORT
    )
    
    session.login(
      SMTPConfig.SENDER_ADDRESS,
      SMTPConfig.SENDER_PASSWORD
    )
    
    session.send_message(message)
    session.quit()
    return True
  except Exception as e:
    print(e)
    return False
      
      
    
