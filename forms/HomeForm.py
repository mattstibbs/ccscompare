from anvil import *
import segment.client as analytics
import google.auth, google.drive
from google.drive import app_files
import anvil.server
import anvil.users
import tables
from tables import app_tables

from HomeForm_LoggedIn import HomeForm_LoggedIn
from HomeForm_LoggedOut import HomeForm_LoggedOut

class HomeForm (HomeFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    
    if anvil.users.get_user():
      self.add_component(HomeForm_LoggedIn())
    if not anvil.users.get_user():
      self.add_component(HomeForm_LoggedOut())

