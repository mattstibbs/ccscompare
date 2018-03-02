from anvil import *
import anvil.server
import anvil.users
import tables
import datetime
from tables import app_tables

from CCSCompareForm import CCSCompareForm
from HomeForm import HomeForm

class MainForm (MainFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
      
    self.content_panel.clear()
    self.content_panel.add_component(HomeForm())
    
    self.logout_button = Link(text="Logout")
    self.logout_button.set_event_handler("click", self.lnk_logout_click)
    
    self.login_button = Link(text="Login")
    self.login_button.set_event_handler("click", self.lnk_login_click)
    
    if anvil.users.get_user():
      self.add_component(self.logout_button, slot="sidebar")
    else:
      self.add_component(self.login_button, slot="sidebar")
      

  def lnk_ccs_compare_click(self, **event_args):
    if self.do_login():
      self.content_panel.clear()
      self.content_panel.add_component(CCSCompareForm(), full_width_row = True)
    else:  
      pass
 
  def do_login(self):
    if not anvil.users.get_user():
      if anvil.users.login_with_form():
        app_tables.log_logins.add_row(timestamp=datetime.datetime.now(), user=anvil.users.get_user())
        self.login_button.remove_from_parent()
        self.add_component(self.logout_button, slot="sidebar")
        self.__init__()
        return True
      else:
        return False
    elif anvil.users.get_user():
      return True
  
  def logout(self):
    if anvil.users.get_user():
      anvil.users.logout()
      self.logout_button.remove_from_parent()
      self.add_component(self.login_button, slot="sidebar")
      
  def lnk_login_click (self, **event_args):
    self.do_login()
    
  def lnk_logout_click (self, **event_args):
    if confirm("Are you sure you want to log out?"):
      anvil.users.logout()
      self.logout_button.remove_from_parent()
      self.add_component(self.login_button, slot="sidebar")
      self.content_panel.clear()
      self.content_panel.add_component(HomeForm())

  def lnk_home_click (self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(HomeForm())




