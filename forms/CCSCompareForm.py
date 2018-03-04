from anvil import *
import anvil.server
import anvil.users
import tables
from tables import app_tables

class CCSCompareForm (CCSCompareFormTemplate):
  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)

    get_open_form().call_js('hideSidebar')
    
    # Ensure user is logged in to use this form
    while not anvil.users.get_user():
      anvil.users.login_with_form()
    
    self.full_width_row = True
    self.clear_results_lists()
    self.previous_search_results = None
    self.dd_age_group.items = [('Adult', 1), ('Child', 2), ('Infant', 3), ('Neonate', 4)]
    self.dd_sex.items = [('Female', 'F'), ('Male', 'M'), ('Unknown', 'I')]
    self.rb_60.selected = True
    self.dd_sg.items = anvil.server.call('get_sg_list')
    self.dd_disposition.items = anvil.server.call('get_dispositions')

  def btn_search_click (self, **event_args):
    
    if not self.ensure_fields_populated():
      return
    
    if self.rb_res1_own.selected == True:
      print("Checking credentials")
      if self.txt_instance1_user.text == '' or self.txt_instance1_pass.text == '':
        alert("Please provide username and password to use your own account")
        self.txt_instance1_user.focus()
        return
    
    if self.rb_res2_own.selected == True:
      if self.txt_instance2_user.text == '' or self.txt_instance2_pass.text == '':
        alert("Please provide username and password to use your own account")
        self.txt_instance2_user.focus()
        return
    
    self.btn_search.enabled = False
    self.btn_repeat_search.enabled = False
    self.btn_find_surgeries.enabled = False
    self.btn_search.text = 'Comparing...'
    try:
      self.do_search()
    except:
      raise
      
    self.btn_search.enabled = True
    self.btn_repeat_search.enabled = True
    self.btn_find_surgeries.enabled = True
    self.btn_search.text = 'Compare Search Results'
    
  def get_instance1_creds(self):
    if not self.rb_res1_own.selected == True:
      return None
    else:
      return (self.txt_instance1_user.text, self.txt_instance1_pass.text)
    
  def get_instance2_creds(self):
    if not self.rb_res2_own.selected == True:
      return None
    else:
      return (self.txt_instance2_user.text, self.txt_instance2_pass.text)
    
  def do_search(self):
    self.clear_results_lists()
    
    results1_instance = self.rb_res1_uat1.get_group_value()
    results2_instance = self.rb_res2_uat1.get_group_value()
    print(self.txt_postcode.text)
    result_dict = anvil.server.call('check_capacity_summary', 
                                    postcode=self.txt_postcode.text.replace(' ', ''),
                                    age_group=self.dd_age_group.selected_value,
                                    sex=self.dd_sex.selected_value,
                                    sg_code=self.dd_sg.selected_value.replace('SG', ''),
                                    sd_code=self.dd_sd.selected_value.replace('SD', ''),
                                    dispo_code=self.dd_disposition.selected_value,
                                    search_distance=self.rb_15.get_group_value(),
                                    surgery=self.txt_surgery_code.text,
                                    instance1=results1_instance,
                                    instance2=results2_instance,
                                    instance1_referral_role=self.rb_res1_pathways.get_group_value(),
                                    instance2_referral_role=self.rb_res2_pathways.get_group_value(),
                                    instance1_creds=self.get_instance1_creds(),
                                    instance2_creds=self.get_instance2_creds()
                                  )
    try:
      if result_dict['results1']:
        self.results_list_1.list_items = result_dict['results1']
        self.results_list_1.refresh_data_bindings()
        self.results_list_2.list_items = result_dict['results2']
        self.results_list_2.refresh_data_bindings()
    except KeyError:
      if result_dict['error']:
        alert(result_dict['error'])
      else:
        alert("Error encountered - please report")
    
    self.previous_search_results = result_dict
  
  def dd_sg_change (self, **event_args):
    if self.dd_sg.selected_value in [None, 0]:
        self.set_red_border(self.dd_sg)
    else:
      self.clear_red_border(self.dd_sg)
      self.dd_sd.items = anvil.server.call('get_sd_list', self.dd_sg.selected_value)
      self.dd_sd.selected_value = 0
      
  def dd_sd_change (self, **event_args):
    if self.dd_sd.selected_value in [None, 0]:
      self.set_red_border(self.dd_sd)
    else:
      self.clear_red_border(self.dd_sd)

  def dd_disposition_change (self, **event_args):
    if self.dd_disposition.selected_value in [None, 0]:
      self.set_red_border(self.dd_disposition)
    else:
      self.clear_red_border(self.dd_disposition)     

  def txt_postcode_change (self, **event_args):
    if self.txt_postcode.text != '':
      self.clear_red_border(self.txt_postcode)
      self.lbl_bad_postcode.visible = False
      self.load_local_surgeries()
      
#       if len(results) > 1:
#         self.btn_find_surgeries.visible = False
#         self.clear_red_border(self.txt_postcode)
#         self.dd_surgery.items = results
#         self.dd_surgery.visible = True
#       else:
#         self.dd_surgery.visible = False
#         self.lbl_bad_postcode.visible = True
#         self.set_red_border(self.txt_postcode)
#         self.txt_postcode.text = ''
#         self.txt_surgery_code.text = ''

    else:
      self.lbl_bad_postcode.visible = True
      self.set_red_border(self.txt_postcode)

  def dd_surgery_change (self, **event_args):
    self.txt_surgery_code.text = self.dd_surgery.selected_value

  def txt_surgery_code_change (self, **event_args):
    surgeries_in_dropdown = [s[1] for s in self.dd_surgery.items]
    if self.txt_surgery_code.text in surgeries_in_dropdown:
      self.dd_surgery.selected_value = self.txt_surgery_code.text
    else:
      self.dd_surgery.selected_value = 'UNK'

  def label_8_show (self, **event_args):
    self.refresh_data_bindings()

  def label_9_show (self, **event_args):
    self.refresh_data_bindings()

  def rb_res2_clicked (self, **event_args):
    self.label_9.text = self.rb_res2_uat1.get_group_value()
    self.clear_results_lists()

  def rb_res1_clicked (self, **event_args):
    self.label_8.text = self.rb_res1_uat1.get_group_value()    
    self.clear_results_lists()

  def rb_res1_role_clicked(self, **event_args):
    selected_option = self.rb_res1_own.get_group_value()
    if selected_option == 'own':
      self.pnl_creds1.visible = True
    elif selected_option == 'pathways':
      self.pnl_creds1.visible = False
    elif selected_option == 'digital':
      self.pnl_creds1.visible = False

  def rb_res2_role_clicked(self, **event_args):
    selected_option = self.rb_res2_own.get_group_value()
    if selected_option == 'own':
      self.pnl_creds2.visible = True
    elif selected_option == 'pathways':
      self.pnl_creds2.visible = False
    elif selected_option == 'digital':
      self.pnl_creds2.visible = False
      
  def clear_results_lists(self):
    self.results_list_1.list_items = []
    self.results_list_1.refresh_data_bindings()
    self.results_list_2.list_items = []
    self.results_list_2.refresh_data_bindings()


  def btn_surgery_help_click (self, **event_args):
    alert("Type a GP surgery code into the text box, or select a nearby GP surgery from the drop-down. Leave both blank for 'Unknown Surgery'")

  def btn_repeat_search_click (self, **event_args):
    self.btn_repeat_search.enabled = False
    previous_search = anvil.server.call('get_previous_search')
    if previous_search:
      self.populate_previous_search_values(previous_search)
    else:
      alert("No previous search found")
    self.btn_repeat_search.enabled = True
    
  def populate_previous_search_values(self, previous_search):
    
    # Populate all the fields
    self.txt_postcode.text = previous_search['postcode']
    self.txt_surgery_code.text = previous_search['surgery']
    self.dd_sg.selected_value = previous_search['sg_code']
    self.dd_sd.items = anvil.server.call_s('get_sd_list', self.dd_sg.selected_value)
    self.dd_sd.selected_value = previous_search['sd_code']
    self.dd_disposition.selected_value = previous_search['disposition']
    
    self.dd_age_group.selected_value = previous_search['age_group']
    self.dd_sex.selected_value = previous_search['sex']
    
    self.ensure_fields_populated()
    self.txt_postcode.raise_event('pressed_enter')
        
    prev_instance_1 = previous_search['left_instance']
    if prev_instance_1 == 'uat1':
      self.rb_res1_uat1.selected = True
    elif prev_instance_1 == 'live':
      self.rb_res1_live.selected = True
    elif prev_instance_1 == 'uat2':
      self.rb_res1_uat2.selected = True
    elif prev_instance_1 == 'uat3':
      self.rb_res1_uat3.selected = True
      
    prev_instance_2 = previous_search['right_instance']
    if prev_instance_2 == 'live':
      self.rb_res2_live.selected = True
    elif prev_instance_2 == 'uat1':
      self.rb_res2_uat1.selected = True
    elif prev_instance_2 == 'uat2':
      self.rb_res2_uat2.selected = True
    elif prev_instance_2 == 'uat3':
      self.rb_res2_uat3.selected = True
      
    prev_role_1 = previous_search['left_referral_role']
    if prev_role_1 == 'digital':
      self.rb_res1_digital.selected = True
      self.rb_res1_digital.raise_event('clicked')
    elif prev_role_1 == 'own':
      self.rb_res1_own.selected = True
      self.rb_res1_own.raise_event('clicked')
    else:
      self.rb_res1_pathways.selected = True
      
    prev_role_2 = previous_search['right_referral_role']
    if prev_role_2 == 'digital':
      self.rb_res2_digital.selected = True
      self.rb_res2_digital.raise_event('clicked')
    elif prev_role_2 == 'own':
      self.rb_res2_own.selected = True
      self.rb_res2_own.raise_event('clicked')
    else:
      self.rb_res1_pathways.selected = True

    prev_dist = previous_search['search_distance']
    if prev_dist == 15:
      self.rb_15.selected = True
    elif prev_dist == 30:
      self.rb_30.selected = True
    elif prev_dist == 45:
      self.rb_45.selected = True
    else:
      self.rb_60.selected = True

  def load_local_surgeries (self, **event_args):
    self.btn_find_surgeries.enabled = False
    self.btn_find_surgeries.text = 'Finding local surgeries...'
    
    if self.txt_postcode.text != '':      
      results = anvil.server.call('get_surgeries', self.txt_postcode.text.replace(' ',''))
      
      if len(results) > 1:
        self.lbl_bad_postcode.visible = False
        self.btn_find_surgeries.visible = False
        self.dd_surgery.items = results
        self.dd_surgery.visible = True
        
        surgeries_in_dropdown = [s[1] for s in self.dd_surgery.items]
        
        if self.txt_surgery_code.text in surgeries_in_dropdown:
          self.dd_surgery.selected_value = self.txt_surgery_code.text
        else:
          self.dd_surgery.selected_value = 'UNK'
       
      else:
        self.dd_surgery.visible = False
        self.btn_find_surgeries.visible = True
        self.lbl_bad_postcode.visible = True
        self.set_red_border(self.txt_postcode)
        self.txt_surgery_code.text = ''
        
    else:
      self.lbl_bad_postcode.visible = True
      
    self.btn_find_surgeries.enabled = True
    self.btn_find_surgeries.text = 'Find local surgeries'

  def ensure_fields_populated(self):
    empty_fields = False
    
    # For each of the inputs, check that they contain valid values, and add a red border if not
    if self.txt_postcode.text == '':
      self.txt_postcode.role = 'glowing-red-border'
      empty_fields = True
    if self.dd_sg.selected_value in [None, 0]:
      self.dd_sg.role = 'glowing-red-border'
      empty_fields = True
    if self.dd_sd.selected_value in [None, 0]:
      self.dd_sd.role = 'glowing-red-border'
      empty_fields = True
    if self.dd_disposition.selected_value in [None, 0]:
      self.dd_disposition.role = 'glowing-red-border'
      empty_fields = True
    
    # If any of the fields were marked as empty return False, otherwise remove red borders and return True
    if empty_fields:
      return False
    else:
      self.txt_postcode.role = None
      self.dd_sd.role = None
      self.dd_sg.role = None
      self.dd_disposition.role = None
      return True

  def set_red_border(self, thing):
    thing.role = 'glowing-red-border'

  def clear_red_border(self, thing):
    thing.role = None

  def form_refreshing_data_bindings (self, **event_args):
    self.ensure_fields_populated()




