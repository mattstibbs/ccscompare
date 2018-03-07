from anvil import *
import segment.client as analytics
import anvil.server
import google.auth, google.drive
from google.drive import app_files
import anvil.users
import tables
from tables import app_tables

class UserLoginsForm (UserLoginsFormTemplate):
  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)

    # Ensure user is logged in to use this form
    while not anvil.users.get_user():
      anvil.users.login_with_form()
    
    if not anvil.server.call('check_permissions', 'MENU_USER_ADMIN'):
      get_open_form().content_panel.clear()
      get_open_form().lnk_home_click
    
    logins = app_tables.log_logins.search(tables.order_by("timestamp", ascending=False))[:10]

    self.pnl_user_logins_list.items = logins
    