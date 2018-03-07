import google.auth, google.drive, google.mail
from google.drive import app_files
import anvil.users
import tables
from tables import app_tables
import anvil.secrets
import anvil.server


@anvil.server.callable
def get_users():
  return app_tables.users.search()

@anvil.server.callable
def trigger_user_activation(user_email):
  u = app_tables.users.get(email=user_email)
  
  if u['enabled'] == True:
    deactivate_user(u)
  elif u['enabled'] == False:
    activate_user(u)

def deactivate_user(u):
  u['enabled'] = False
  
def activate_user(u):
  u['enabled'] = True
  if not app_tables.userpermissions.get(user=u):
    app_tables.userpermissions.add_row(
      user=u, 
      permissions=[app_tables.permissions.get(code='MENU_CCS_COMPARE')]
    )