# correo.py
import smtplib
from email.mime.text import MIMEText

EMAIL = "villarealailton@gmail.com"
PASSWORD = "mcmg aewv dvst zulu"
DESTINO = "181760@upslp.edu.mx"


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
