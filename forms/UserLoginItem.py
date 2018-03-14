from anvil import *
import anvil.server
import anvil.users
import tables
from tables import app_tables

class UserLoginItem (UserLoginItemTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
