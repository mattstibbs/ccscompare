from anvil import *
import segment.client as analytics
import google.auth, google.drive
from google.drive import app_files
import anvil.server
import anvil.users
import tables
from tables import app_tables

class HomeForm_LoggedOut (HomeForm_LoggedOutTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def button_1_click (self, **event_args):
    get_open_form().lnk_login_click()

