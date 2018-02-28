from anvil import *
import anvil.server
import anvil.users
import tables
from tables import app_tables

from CCSCompareForm import CCSCompareForm

class MainForm (MainFormTemplate):
  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    

  def link_1_click (self, **event_args):
    # This method is called when the link is clicked
    self.content_panel.clear()
    self.content_panel.add_component(CCSCompareForm())

