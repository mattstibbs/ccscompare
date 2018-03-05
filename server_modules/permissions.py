import google.auth, google.drive, google.mail
from google.drive import app_files
import anvil.users
import tables
from tables import app_tables
import anvil.secrets
import anvil.server

@anvil.server.callable
def check_permissions(permission):
  if permission in get_permission_codes():
    return True
  else:
    return False

@anvil.server.callable
def get_permission_codes():
  u = anvil.users.get_user()
  userpermissions = app_tables.userpermissions.get(user=u)
  permissions_list = [perm['code'] for perm in userpermissions['permissions']]
  return permissions_list