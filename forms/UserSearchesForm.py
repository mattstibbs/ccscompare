from anvil import *
import anvil.server
import google.auth, google.drive
from google.drive import app_files
import anvil.users
import tables
from tables import app_tables

class UserSearchesForm (UserSearchesFormTemplate):
  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)

    # Ensure user is logged in to use this form
    while not anvil.users.get_user():
      anvil.users.login_with_form()
    
    if not anvil.server.call('check_permissions', 'MENU_USER_ADMIN'):
      get_open_form().content_panel.clear()
      get_open_form().lnk_home_click
    
    self.get_searches()
    
  def get_users(self):
    
    results = anvil.server.call('get_users')
    
    users_list = []
    
    users_list.append((' All Users',''))
    
    for result in results:
      users_list.append((result['email'],result['email']))
      
    return users_list
  
  def get_searches(self, email=None):
    if email:
      u = anvil.server.call('get_user_by_email', email)
      logins = app_tables.log_searches.search(tables.order_by("timestamp", ascending=False), user=u)[:100]  
    else:
      logins = app_tables.log_searches.search(tables.order_by("timestamp", ascending=False))[:100]
    
    self.pnl_user_searches_list.items = logins

  def filter_search_list(self, **properties):
    if self.dd_user.selected_value == '':
      self.get_searches()
    else:
      self.get_searches(self.dd_user.selected_value)