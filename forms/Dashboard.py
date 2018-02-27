from anvil import *
import anvil.users
import tables
from tables import app_tables
import anvil.server
import ResultsList

class Dashboard (DashboardTemplate):
  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)

    self.dd_sg.items = anvil.server.call('get_sg_list')
    self.dd_age_group.items = [('Adult', 1), ('Child', 2), ('Infant', 3), ('Neonate', 4)]
    self.dd_sex.items = [('Female', 'F'), ('Male', 'M'), ('Unknown', 'I')]
    self.dd_disposition.items = anvil.server.call('get_dispositions')
    

  def btn_search_click (self, **event_args):
    results = anvil.server.call('check_capacity_summary', 
                      postcode=self.txt_postcode.text,
                      age_group=self.dd_age_group.selected_value,
                      sex=self.dd_sex.selected_value,
                      sg_code=self.dd_sg.selected_value.replace('SG', ''),
                      sd_code=self.dd_sd.selected_value.replace('SD', ''),
                      dispo_code=self.dd_disposition.selected_value,
                      search_distance=60,
                      surgery=self.dd_surgery.selected_value)
    
    print(results)
    
    self.results_list_1.list_items = results
    self.results_list_1.refresh_data_bindings()

  def dd_sg_change (self, **event_args):
    self.dd_sd.items = anvil.server.call('get_sd_list', self.dd_sg.selected_value)

  def txt_postcode_pressed_enter (self, **event_args):
     self.dd_surgery.items = anvil.server.call('get_surgeries', self.txt_postcode.text)

  def txt_postcode_lost_focus (self, **event_args):
     self.dd_surgery.items = anvil.server.call('get_surgeries', self.txt_postcode.text)







