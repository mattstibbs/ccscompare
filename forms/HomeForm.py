from anvil import *
import anvil.server
import anvil.users
import tables
from tables import app_tables

class HomeForm (HomeFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    if anvil.users.get_user():
      self.pnl_logged_in.visible = True
      self.pnl_not_logged_in.visible = False
    else:
      self.pnl_not_logged_in.visible = True
      self.pnl_logged_in.visible = False
      