from anvil import *
import anvil.server
import google.auth, google.drive
from google.drive import app_files
import anvil.users
import tables
from tables import app_tables

class UserItem (UserItemTemplate):
  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)

    self.has_ccs_compare_permission()
    
  def has_ccs_compare_permission(self):
    permissions = self.item['permissions']
    print(permissions)