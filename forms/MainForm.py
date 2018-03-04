from anvil import *
import anvil.server
import anvil.users
import tables
import datetime
from tables import app_tables

from CCSCompareForm import CCSCompareForm
from HomeForm import HomeForm
from InfoForm import InfoForm
import UserManagement

class MainForm (MainFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    self.logout_button = Link(text="Logout")
    self.logout_button.set_event_handler("click", self.lnk_logout_click)
  
    self.login_button = Link(text="Login")
    self.login_button.set_event_handler("click", self.lnk_login_click)
    
    self.add_login_logout_links()
       
    self.content_panel.clear()
    self.content_panel.add_component(HomeForm())
    self.content_panel.add_component(UserManagement.UserList())

  def add_login_logout_links(self):
    if anvil.users.get_user():
      self.login_button.remove_from_parent()
      self.add_component(self.logout_button, slot="sidebar")
    else:
      print("Adding login button")
      self.logout_button.remove_from_parent()
      self.add_component(self.login_button, slot="sidebar")

  def load_ccs_compare_form(self, **event_args):
    if self.do_login():
      self.content_panel.clear()
      self.content_panel.add_component(CCSCompareForm(), full_width_row = True)
    else:  
      pass
    
  def load_info_form(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(InfoForm())
 
  def do_login(self):
    if anvil.users.get_user():
      return True
    elif not anvil.users.get_user():
      if anvil.users.login_with_form():
        self.content_panel.clear()
        app_tables.log_logins.add_row(timestamp=datetime.datetime.now(), user=anvil.users.get_user())
        self.add_login_logout_links()
        return True
      else:
        return False
  
  def lnk_login_click (self, **event_args):
    if self.do_login():
      self.content_panel.clear()
      self.content_panel.add_component(HomeForm())
      
    
  def logout(self):
    if anvil.users.get_user():
      self.content_panel.clear()
      anvil.users.logout()
      self.logout_button.remove_from_parent()
      self.add_component(self.login_button, slot="sidebar")
      self.content_panel.add_component(HomeForm())
 
  def lnk_logout_click (self, **event_args):
    if confirm("Are you sure you want to log out?"):
      self.logout()

  def lnk_home_click (self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(HomeForm())
