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

    

  def link_1_click (self, **event_args):
    if anvil.users.get_user():
      self.content_panel.clear()
      self.content_panel.add_component(CCSCompareForm(), full_width_row = True)
    else:  
      if anvil.users.login_with_form():
        app_tables.log_logins.add_row(timestamp=datetime.datetime.now(), user=anvil.users.get_user())
        self.content_panel.clear()
        self.content_panel.add_component(CCSCompareForm(), full_width_row = True)
      else:
        pass

  
  def lnk_logout_click (self, **event_args):
    if confirm("Are you sure you want to log out?"):
      anvil.users.logout()
      self.content_panel.clear()
      self.content_panel.add_component(HomeForm())

  def lnk_home_click (self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(HomeForm())




