from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
import os  # untuk membaca environment variables

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send_email():
    # Ambil data dari form
    nombre = request.form.get("nombre")
    email = request.form.get("email")
    satisfaccion = request.form.get("satisfaccion")
    favorito = request.form.get("favorito")
    comentario = request.form.get("comentario")

    # Isi email
    mensaje = f"""
Resultados de la Encuesta de Fans - Josy Esteban

Nombre del fan: {nombre}
Email del fan: {email}
1. Nivel de satisfacción: {satisfaccion}
2. Contenido favorito: {favorito}
3. Comentario / sugerencia:
{comentario}

--------------------------------------
Este mensaje se envió automáticamente.
"""

    msg = MIMEText(mensaje)
    msg["Subject"] = f"Nuevo Resultado de Encuesta - Josy Esteban ({nombre})"
    msg["From"] = email  # From = email pengirim
    msg["To"] = os.environ.get("GMAIL_USER")  # Email tujuan dari environment variable

    # Kirim via SMTP Gmail
    try:
        gmail_user = os.environ.get("GMAIL_USER")
        gmail_app_password = os.environ.get("GMAIL_APP_PASSWORD")

        if not gmail_user or not gmail_app_password:
            return "Error: Gmail credentials not set in environment variables."

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_app_password)
            server.sendmail(
                email,
                gmail_user,
                msg.as_string()
            )
        return "OK"  # Frontend popup bisa membaca
    except Exception as e:
        return f"Error al enviar: {e}"

if __name__ == "__main__":
    app.run(debug=True)