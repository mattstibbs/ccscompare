from anvil import *
import anvil.users
import tables
from tables import app_tables
import anvil.server

class ResultsList (ResultsListTemplate):
  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)

    # Any code you write here will run when the form opens.