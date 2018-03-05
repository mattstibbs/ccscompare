from anvil import *
import google.auth, google.drive
from google.drive import app_files
import anvil.server
import anvil.users
import tables
from tables import app_tables

class HomeForm_LoggedIn (HomeForm_LoggedInTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def load_ccs_compare_form (self, **event_args):
    get_open_form().load_ccs_compare_form()

  def button_2_click (self, **event_args):
    get_open_form().lnk_logout_click()

