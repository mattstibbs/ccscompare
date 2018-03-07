from anvil import *
import segment.client as analytics
import anvil.server
import google.auth, google.drive
from google.drive import app_files
import anvil.users
import tables
from tables import app_tables

class UserSearchItem (UserSearchItemTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
