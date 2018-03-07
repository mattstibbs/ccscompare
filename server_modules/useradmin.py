import google.auth, google.drive, google.mail
from google.drive import app_files
import anvil.users
import tables
from tables import app_tables
import anvil.secrets
import anvil.server
import anvil.http


@anvil.server.callable
def get_users():
  return app_tables.users.search()

@anvil.server.callable
def trigger_user_activation(user_email):
  u = app_tables.users.get(email=user_email)
  
  if u['enabled'] == True:
    return deactivate_user(u)
  elif u['enabled'] == False:
    return activate_user(u)

def deactivate_user(u):
  u['enabled'] = False
  return False
  
def activate_user(u):
  u['enabled'] = True
  if not app_tables.userpermissions.get(user=u):
    app_tables.userpermissions.add_row(
      user=u, 
      permissions=[app_tables.permissions.get(code='MENU_CCS_COMPARE')]
    )
    
  resp = anvil.http.request(
      url="https://api.mailgun.net/v3/mg.dos-tools.tech/messages",
      method="POST",
      data={"from": "DoS Tools <admin@mg.dos-tools.tech>",
              "to": "Matt Stibbs <m.stibbs@nhs.net>",
              "subject": "User activated",
              "text": "User {} has been activated".format(u['email'])
           },
      username="api",
      password=anvil.secrets.get_secret('mailgun_key'))
  
  resp = anvil.http.request(
      url="https://api.mailgun.net/v3/mg.dos-tools.tech/messages",
      method="POST",
      data={"from": "DoS Tools <admin@mg.dos-tools.tech>",
              "to": u['email'],
              "subject": "DoS Compare Tool account activated",
              "text": "Account for {} has been activated".format(u['email'])
           },
      username="api",
      password=anvil.secrets.get_secret('mailgun_key'))  
  
  return True
