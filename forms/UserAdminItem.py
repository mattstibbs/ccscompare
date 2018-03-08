from anvil import *
import anvil.server
import google.auth, google.drive
from google.drive import app_files
import anvil.users
import tables
from tables import app_tables

class UserAdminItem (UserAdminItemTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def reset_password_click (self, **event_args):
      anvil.users.send_password_reset_email(self.item['email'])
      alert("Password reset email sent to user {}".format(self.item['email']))

  def get_user_activated_status(self, **event_args):
    if self.item['enabled'] == True:
      return "Deactivate User"
    elif self.item['enabled'] == False:
      return "Activate User"

  def get_user_background(self, **event_args):
    if self.item['enabled'] == True:
      return ""
    elif self.item['enabled'] == False:
      return "#FF9999"
    
  def button_1_click (self, **event_args):
    result = anvil.server.call('trigger_user_activation', self.item['email'])
    if result:
      alert("User activated and email notification sent to {}".format(self.item['email']))
    self.parent.items = anvil.server.call('get_users')