# correo.py
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()

EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")
DESTINO = os.getenv("EMAIL_DESTINO")

def send_email(asunto, cuerpo):
    try:
        msg = MIMEText(cuerpo)
        msg["Subject"] = asunto
        msg["From"] = EMAIL
        msg["To"] = DESTINO

        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(EMAIL, PASSWORD)
        servidor.sendmail(EMAIL, DESTINO, msg.as_string())
        servidor.quit()
        return True

    except Exception as e:
        print("ERROR enviando correo:", e)
        return False
