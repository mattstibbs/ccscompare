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

    self.content_panel.clear()
    self.content_panel.add_component(CCSCompareForm(), full_width_row = True)
    

  def link_1_click (self, **event_args):
    # This method is called when the link is clicked
    self.content_panel.clear()
    self.content_panel.add_component(CCSCompareForm(), full_width_row = True)
