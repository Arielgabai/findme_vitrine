import os
import ssl
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs


BASE_DIR = Path(__file__).resolve().parent
CONTACT_TO_EMAIL = os.getenv("CONTACT_TO_EMAIL", "ariel.gabai@hotmail.fr")
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", SMTP_USERNAME or CONTACT_TO_EMAIL)
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "FindMe")
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() in {"1", "true", "yes", "on"}
SMTP_USE_SSL = os.getenv("SMTP_USE_SSL", "false").lower() in {"1", "true", "yes", "on"}
PORT = int(os.getenv("PORT", "10000"))


def get_first_value(form_data, key):
    return form_data.get(key, [""])[0].strip()


def smtp_is_configured():
    return all([SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD, SMTP_FROM_EMAIL, CONTACT_TO_EMAIL])


def build_email_content(payload):
    return "\n".join(
        [
            "Nouvelle demande depuis la landing page FindMe",
            "",
            f"Nom : {payload['name']}",
            f"E-mail : {payload['email']}",
            f"Profil : {payload['profil']}",
            f"Type d'evenement : {payload['evenement'] or 'Non precise'}",
            "",
            "Message :",
            payload["message"],
        ]
    )


def send_contact_email(payload):
    message = EmailMessage()
    message["Subject"] = f"Nouvelle demande FindMe - {payload['profil']}"
    message["From"] = formataddr((SMTP_FROM_NAME, SMTP_FROM_EMAIL))
    message["To"] = CONTACT_TO_EMAIL
    message["Reply-To"] = payload["email"]
    message.set_content(build_email_content(payload))

    if SMTP_USE_SSL:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=20) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(message)
        return

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as server:
        server.ehlo()
        if SMTP_USE_TLS:
            server.starttls(context=ssl.create_default_context())
            server.ehlo()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(message)


class LandingPageHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def redirect(self, location):
        self.send_response(303)
        self.send_header("Location", location)
        self.end_headers()

    def do_POST(self):
        if self.path != "/contact":
            self.send_error(404, "Not found")
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length).decode("utf-8")
        form_data = parse_qs(raw_body, keep_blank_values=True)

        if get_first_value(form_data, "_honey"):
            self.redirect("/index.html?contact=success#contact-form")
            return

        payload = {
            "name": get_first_value(form_data, "name"),
            "email": get_first_value(form_data, "email"),
            "profil": get_first_value(form_data, "profil"),
            "evenement": get_first_value(form_data, "evenement"),
            "message": get_first_value(form_data, "message"),
        }

        if not payload["name"] or not payload["email"] or not payload["profil"] or not payload["message"]:
            self.redirect("/index.html?contact=invalid#contact-form")
            return

        if not smtp_is_configured():
            self.redirect("/index.html?contact=config#contact-form")
            return

        try:
            send_contact_email(payload)
        except Exception:
            self.redirect("/index.html?contact=error#contact-form")
            return

        self.redirect("/index.html?contact=success#contact-form")


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", PORT), LandingPageHandler)
    print(f"FindMe landing page server running on http://0.0.0.0:{PORT}")
    server.serve_forever()
