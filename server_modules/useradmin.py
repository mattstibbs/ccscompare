import google.auth, google.drive, google.mail
from google.drive import app_files
import anvil.users
import tables
from tables import app_tables
import anvil.secrets
import anvil.server

@anvil.server.callable
def get_users_and_permissions():
  userpermissions = app_tables.userpermissions.search()
  return userpermissions


@anvil.server.callable
def get_users():
  return app_tables.users.search()
  