import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configura los detalles del servidor SMTP de Gmail
smtp_server = 'smtp.gmail.com'
smtp_port = 587  # Puerto estándar para TLS

# Tu dirección de correo y contraseña (reemplázalas por tus propias credenciales)
smtp_username = 'Josephfabrizizo@gmail.com'
smtp_password = 'uftr oavl byqr bvde'  # Reemplaza 'tu_contraseña' con tu contraseña real

# Crea el objeto MIMEMultipart
msg = MIMEMultipart()

# Detalles del correo
msg['From'] = 'Josephfabrizizo@gmail.com'
msg['To'] = 'Josephfabrizziocuentas@gmail.com'
msg['Subject'] = 'Asunto del Correo'

# Contenido HTML
html_content = """
<html>
<head></head>
<body>
<h1>PYTHONGOOD</h1>
<p>VUELVE</p>
</body>
</html>
"""

# Adjunta el contenido HTML al mensaje
msg.attach(MIMEText(html_content, 'html'))

# Inicia la conexión SMTP
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()  # Inicia una conexión TLS segura
    server.login(smtp_username, smtp_password)
    server.sendmail(smtp_username, msg['To'], msg.as_string())

print('Correo enviado exitosamente')
