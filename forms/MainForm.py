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
    
    if anvil.users.get_user():
      logout_button = Link(text="Logout")
      self.add_component(logout_button, slot="sidebar")
      logout_button.set_event_handler("click", self.lnk_logout_click())
    else:
      login_button = Link(text="Login")
      self.add_component(login_button, slot="sidebar")
      login_button.set_event_handler("click", self.lnk_login_click())

  def link_1_click (self, **event_args):
    if do_login():
      self.content_panel.clear()
      self.content_panel.add_component(CCSCompareForm(), full_width_row = True)
    else:  
      pass
 
  def do_login(self):
    if not anvil.users.get_user():
      if anvil.users.login_with_form():
        app_tables.log_logins.add_row(timestamp=datetime.datetime.now(), user=anvil.users.get_user())
        return True
      else:
        return False
    elif anvil.users.get_user():
      return True
        
      
  def lnk_login_click (self, **event_args):
    if confirm("Are you sure you want to log out?"):
      anvil.users.logout()
      self.content_panel.clear()
      self.content_panel.add_component(HomeForm())
  
  def lnk_logout_click (self, **event_args):
    if confirm("Are you sure you want to log out?"):
      anvil.users.logout()
      self.content_panel.clear()
      self.content_panel.add_component(HomeForm())

  def lnk_home_click (self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(HomeForm())




