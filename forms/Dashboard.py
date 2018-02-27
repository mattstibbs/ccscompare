from anvil import *
import anvil.users
import tables
from tables import app_tables
import anvil.server

class Dashboard (DashboardTemplate):
  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)

    self.dd_sg.items = anvil.server.call('get_sg_list')
    self.dd_age_group.items = [('Adult', 1), ('Child', 2), ('Infant', 3), ('Neonate', 4)]
    self.dd_disposition.items = anvil.server.call('get_dispositions')
    

  def btn_search_click (self, **event_args):
    anvil.server.call('check_capacity_summary', 
                      postcode=self.txt_postcode.text,
                      age_group=self.dd_age_group.selected_value,
                      sex=self.dd_sex.selected_value,
                      sg_code=self.dd_sg.selected_value,
                      sd_code=self.dd_sd.selected_value,
                      dispo_code=self.drop_down_1.selected_value,
                      search_distance=60)

  def dd_sg_change (self, **event_args):
    self.dd_sd.items = anvil.server.call('get_sd_list', self.dd_sg.selected_value)
    print(self.dd_sg.selected_value.replace('SG', ''))

  def txt_postcode_pressed_enter (self, **event_args):
     self.dd_surgery.items = anvil.server.call('get_surgeries', self.txt_postcode.text)

  def txt_postcode_lost_focus (self, **event_args):
     self.dd_surgery.items = anvil.server.call('get_surgeries', self.txt_postcode.text)

  def dd_sd_change (self, **event_args):
    print(self.dd_sd.selected_value.replace('SD', ''))

  def dd_age_group_change (self, **event_args):
    # This method is called when an item is selected
    pass






