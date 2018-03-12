import google.auth, google.drive, google.mail
from google.drive import app_files
import anvil.users
import tables
from tables import app_tables
import anvil.secrets
import anvil.server
import anvil.http

from mailgun_email import send_mailgun_email

@anvil.server.callable
def get_user_by_email(email):
  return app_tables.users.search(email=email)[0]

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
    
  send_mailgun_email(to=anvil.users.get_user()['email'],
                     subject="User activated",
                     body="User {} has been activated and they have been notified".format(u['email'])
                    )

  send_mailgun_email(to=u['email'],
                   subject="DoS Compare Tool account activated",
                   body="Account for {} has been activated".format(u['email'])
                  )
  
  return True
