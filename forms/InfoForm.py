from anvil import *
import google.auth, google.drive
from google.drive import app_files
import anvil.server
import anvil.users
import tables
from tables import app_tables

class InfoForm (InfoFormTemplate):
  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)

    # Any code you write here will run when the form opens.