from anvil import *
import tables
from tables import app_tables
import anvil.server

class Dashboard (DashboardTemplate):
  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)

    self.dd_sg.items = anvil.server.call('get_sg_list')
    self.dd_sg.selected_value = self.dd_sg.selected_value
    

  def btn_search_click (self, **event_args):
    print(self.dd_sex.selected_value)

  def dd_sg_change (self, **event_args):
    self.dd_sd.items = anvil.server.call('get_sd_list', self.dd_sg.selected_value)

  def txt_postcode_pressed_enter (self, **event_args):
     anvil.server.call('get_surgeries', self.txt_postcode.text)

  def txt_postcode_lost_focus (self, **event_args):
     anvil.server.call('get_surgeries', self.txt_postcode.text)




