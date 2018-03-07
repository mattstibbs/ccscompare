from anvil import *
import segment.client as analytics
import anvil.server
import google.auth, google.drive
from google.drive import app_files
import anvil.users
import tables
from tables import app_tables

class UserItem (UserItemTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def reset_password_click (self, **event_args):
      anvil.users.send_password_reset_email(self.item['email'])

