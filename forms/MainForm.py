from anvil import *
import anvil.server
import anvil.users
import tables
from tables import app_tables

from CCSCompareForm import CCSCompareForm
from HomeForm import HomeForm

class MainForm (MainFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    self.content_panel.clear()
    self.content_panel.add_component(HomeForm())
    

  def link_1_click (self, **event_args):
    if not anvil.users.get_user():
      if anvil.users.login_with_form():
        self.content_panel.clear()
        self.content_panel.add_component(CCSCompareForm(), full_width_row = True)
      else:
        pass
    else:
      self.content_panel.clear()
      self.content_panel.add_component(CCSCompareForm(), full_width_row = True)
  
  def lnk_logout_click (self, **event_args):
    if confirm("Are you sure you want to log out?"):
      anvil.users.logout()
      self.content_panel.clear()
      self.content_panel.add_component(HomeForm())

  def lnk_home_click (self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(HomeForm())


