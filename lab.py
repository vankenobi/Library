import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys

message= MIMEMultipart()   

message["From"] = "musa.kucuk99@gmail.com"  #Mail'i gönderen kişi

message["To"] = "musa.kucuk99@gmail.com"    #Mail'i alan kişi

message["Subject"] = "Python Smtp ile Mail Gönderme" #Mail'in konusu


body= """

Python üzerinde smtp modülü
kullanarak mail gönderiyorum.

"""   #Mail içerisinde yazacak içerik

body_text = MIMEText(body,"plain") #

message.attach(body_text)

#Gmail serverlerine bağlanma işlemi.

try:
    mail = smtplib.SMTP("smtp.gmail.com",587)

    mail.ehlo()
    
    mail.starttls()

    mail.login("musakucuk99@gmail.com","KIBEmJ6i")

    mail.sendmail(message["From"],message["To"],message.as_string())

    print("Mail Başarılı bir şekilde gönderildi.")

    mail.close()

#Eğer mesaj gönderirken hata ile karşılaşırsak except çalışır.

except:

    sys.stderr.write("Bir hata oluştu. Tekrar deneyin...")
    sys.stderr.flush()