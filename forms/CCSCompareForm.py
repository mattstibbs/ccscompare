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
    self.btn_search.enabled = False
    self.btn_repeat_search.enabled = False
    self.btn_find_surgeries.enabled = False
    self.btn_search.text = 'Comparing...'
    self.do_search()
    self.btn_search.enabled = True
    self.btn_repeat_search.enabled = True
    self.btn_find_surgeries.enabled = True
    self.btn_search.text = 'Compare Search Results'
    
  def do_search(self):
    self.clear_results_lists()
    
    results1_instance = self.rb_res1_uat1.get_group_value()
    results2_instance = self.rb_res2_uat1.get_group_value()
    
    def get_instance1_creds():
      if self.txt_instance1_user.text != '' and self.txt_instance1_pass.text != '' and self.chk_instance1_owncreds.checked == True:
        return (self.txt_instance1_user.text, self.txt_instance1_pass.text)
      else:
        return None
      
    def get_instance2_creds():
      if self.txt_instance2_user.text != '' and self.txt_instance2_pass.text != '' and self.chk_instance2_owncreds.checked == True:
        return (self.txt_instance2_user.text, self.txt_instance2_pass.text)
      else:
        return None
    
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
                                    instance1_creds=get_instance1_creds(),
                                    instance2_creds=get_instance2_creds()
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
    self.dd_sd.items = anvil.server.call('get_sd_list', self.dd_sg.selected_value)

  def txt_postcode_has_changed (self, **event_args):
    if self.txt_postcode.text != '':
      results = anvil.server.call_s('get_surgeries', self.txt_postcode.text.replace(' ',''))
      if len(results) > 1:
        self.lbl_bad_postcode.visible = False
        self.btn_find_surgeries.visible = False
        self.dd_surgery.items = results
        self.dd_surgery.visible = True
      else:
        self.dd_surgery.visible = False
        self.lbl_bad_postcode.visible = True
        self.txt_postcode.text = ''
        self.txt_surgery_code.text = ''
        self.txt_postcode.focus()

    else:
      self.lbl_bad_postcode.visible = True
      self.txt_postcode.focus()

  def dd_surgery_change (self, **event_args):
    self.txt_surgery_code.text = self.dd_surgery.selected_value

  def txt_surgery_code_change (self, **event_args):
    surgeries_in_dropdown = [s[1] for s in self.dd_surgery.items]
    if self.txt_surgery_code.text in surgeries_in_dropdown:
      self.dd_surgery.selected_value = self.txt_surgery_code.text
    else:
      self.dd_surgery.selected_value = 'UNK'

  def label_8_show (self, **event_args):
    # This method is called when the Label is shown on the screen
    self.refresh_data_bindings()

  def label_9_show (self, **event_args):
    # This method is called when the Label is shown on the screen
    self.refresh_data_bindings()

  def rb_res2_clicked (self, **event_args):
    # This method is called when this radio button is selected
    self.label_9.text = self.rb_res2_uat1.get_group_value()
    self.clear_results_lists()

  def rb_res1_clicked (self, **event_args):
    # This method is called when this radio button is selected
    self.label_8.text = self.rb_res1_uat1.get_group_value()
    self.clear_results_lists()

  def clear_results_lists(self):
    self.results_list_1.list_items = []
    self.results_list_1.refresh_data_bindings()
    self.results_list_2.list_items = []
    self.results_list_2.refresh_data_bindings()

  def check_box_1_change (self, **event_args):
    if self.chk_instance1_owncreds.checked == True:
      self.txt_instance1_user.visible = True
      self.txt_instance1_pass.visible = True
      self.lbl_instance1_user.visible = True
      self.lbl_instance1_pass.visible = True
    else:
      self.txt_instance1_user.visible = False
      self.txt_instance1_pass.visible = False   
      self.lbl_instance1_user.visible = False
      self.lbl_instance1_pass.visible = False

  def check_box_2_change (self, **event_args):
    if self.chk_instance2_owncreds.checked == True:
      self.txt_instance2_user.visible = True
      self.txt_instance2_pass.visible = True
      self.lbl_instance2_user.visible = True
      self.lbl_instance2_pass.visible = True
    else:
      self.txt_instance2_user.visible = False
      self.txt_instance2_pass.visible = False
      self.lbl_instance2_user.visible = False
      self.lbl_instance2_pass.visible = False


  def button_1_click (self, **event_args):
    alert("Type a GP surgery code into the text box, or select a nearby GP surgery from the drop-down. Leave both blank for 'Unknown Surgery'")

  def btn_repeat_search_click (self, **event_args):
    self.btn_search.enabled = False
    self.btn_repeat_search.enabled = False
    self.btn_search.text = 'Comparing...'
    self.btn_repeat_search.text = 'Repeating previous comparison...'
    previous_search = anvil.server.call('get_previous_search')
    self.populate_previous_search_values(previous_search)
    self.do_search()
    self.btn_search.enabled = True
    self.btn_repeat_search.enabled = True
    self.btn_search.text = 'Compare Results'
    self.btn_repeat_search.text = 'Repeat my most recent comparison'
    
  
  def populate_previous_search_values(self, previous_search):
    self.txt_postcode.text = previous_search['postcode']
    self.txt_surgery_code.text = previous_search['surgery']
    self.dd_sg.selected_value = previous_search['sg_code']
    self.dd_sd.items = anvil.server.call_s('get_sd_list', self.dd_sg.selected_value)
    self.dd_sd.selected_value = previous_search['sd_code']
    self.dd_age_group.selected_value = previous_search['age_group']
    self.dd_sex.selected_value = previous_search['sex']
    self.dd_disposition.selected_value = previous_search['disposition']
    
    prev_instance_1 = previous_search['left_instance']
    print(prev_instance_1)
    if prev_instance_1 == 'uat1':
      self.rb_res1_uat1.selected = True
    elif prev_instance_1 == 'www':
      self.rb_res1_live.selected = True
    elif prev_instance_1 == 'uat2':
      self.rb_res1_uat2.selected = True
    elif prev_instance_1 == 'uat3':
      self.rb_res1_uat3.selected = True
      
    prev_instance_2 = previous_search['right_instance']
    print(prev_instance_2)
    if prev_instance_2 == 'www':
      self.rb_res2_live.selected = True
    elif prev_instance_2 == 'uat1':
      self.rb_res2_uat1.selected = True
    elif prev_instance_2 == 'uat2':
      self.rb_res2_uat2.selected = True
    elif prev_instance_2 == 'uat3':
      self.rb_res2_uat3.selected = True

    prev_dist = previous_search['search_distance']
    print(prev_dist)
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
    if self.txt_postcode.text != '':      
      results = anvil.server.call_s('get_surgeries', self.txt_postcode.text.replace(' ',''))
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
      self.txt_postcode.focus()
      self.lbl_bad_postcode.visible = True
    self.btn_find_surgeries.enabled = True
    
