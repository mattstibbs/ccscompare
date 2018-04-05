import anvil.email
import anvil.users
import tables
from tables import app_tables
import anvil.secrets
import anvil.server
import anvil.http

@anvil.server.callable
def send_mailgun_email(to, subject, body):
  resp = anvil.http.request(
    url="https://api.mailgun.net/v3/mg.dos-tools.tech/messages",
    method="POST",
    data={"from": "DoS Tools <admin@mg.dos-tools.tech>",
            "to": to,
            "subject": subject,
            "text": body
          },
    username="api",
    password=anvil.secrets.get_secret('mailgun_key'))

