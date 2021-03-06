from anvil import *
import anvil.server
import anvil.users
import tables
import datetime
from tables import app_tables

from CCSCompareForm import CCSCompareForm
from HomeForm import HomeForm
from InfoForm import InfoForm
from UserAdminForm import UserAdminForm
from UserLoginsForm import UserLoginsForm
from HelpForm import HelpForm
from UserSearchesForm import UserSearchesForm
from ImportForm import ImportForm


class MainForm (MainFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    self.logout_button = Link(text="Logout", icon="fa:power-off")
    self.logout_button.set_event_handler("click", self.lnk_logout_click)
  
    self.login_button = Link(text="Login")
    self.login_button.set_event_handler("click", self.lnk_login_click)
    
    self.add_login_logout_links()
       
    self.content_panel.clear()
    self.content_panel.add_component(HomeForm())
    
    self.render_menu_items_from_permissions()
    
  def add_login_logout_links(self):
    if anvil.users.get_user():
      self.login_button.remove_from_parent()
      self.add_component(self.logout_button, slot="sidebar")
    else:
      self.logout_button.remove_from_parent()
      self.add_component(self.login_button, slot="sidebar")

  def load_ccs_compare_form(self, **event_args):
    if self.do_login():
      self.content_panel.clear()
      self.content_panel.add_component(CCSCompareForm(**event_args), full_width_row = True)
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
        self.render_menu_items_from_permissions()
        return True
      else:
        return False
  
  def lnk_login_click (self, **event_args):
#     analytics.track('Clicked Login Button', { 'location': 'sidebar', 'item': 'lnk_login' })
    if self.do_login():
      self.content_panel.clear()
      self.content_panel.add_component(HomeForm())
      
    
  def logout(self):
    if anvil.users.get_user():
      self.content_panel.clear()
      anvil.users.logout()
      self.logout_button.remove_from_parent()
      self.render_menu_items_from_permissions()
      self.add_component(self.login_button, slot="sidebar")
      self.content_panel.add_component(HomeForm())
 
  def lnk_logout_click (self, **event_args):
#     analytics.track('Clicked Logout Button', { 'location': 'sidebar', 'item': 'lnk_logout' })
    if confirm("Are you sure you want to log out?"):
      self.logout()

  def lnk_home_click (self, **event_args):
#     analytics.track('Clicked Home Button', { 'location': 'sidebar', 'item': 'lnk_home' })
    self.content_panel.clear()
    self.content_panel.add_component(HomeForm())
    
  def lnk_useradmin_click (self, **event_args):
#     analytics.track('Clicked User Admin Button', { 'location': 'sidebar', 'item': 'lnk_useradmin' })
    self.content_panel.clear()
    self.content_panel.add_component(UserAdminForm())
    
  def lnk_menu_logins_click (self, **event_args):
#     analytics.track('Clicked User Logins Button', { 'location': 'sidebar', 'item': 'lnk_userlogins' })
    self.content_panel.clear()
    self.content_panel.add_component(UserLoginsForm())
    
  def lnk_menu_searches_click (self, **event_args):
#     analytics.track('Clicked User Searches Button', { 'location': 'sidebar', 'item': 'lnk_usersearches' })
    self.content_panel.clear()
    self.content_panel.add_component(UserSearchesForm())

  def render_menu_items_from_permissions(self):
    if anvil.users.get_user():
      
      self.lnk_change_password.visible = True
      
      u_permissions = anvil.server.call('get_permission_codes')
    
      if 'MENU_CCS_COMPARE' in u_permissions:
        self.lnk_ccs_compare.visible = True
      else:
        self.lnk_ccs_compare.visible = False
      
      if 'MENU_USER_ADMIN' in u_permissions:
        self.lnk_menu_useradmin.visible = True
        self.lnk_menu_logins.visible = True
        self.lnk_menu_searches.visible = True
        self.lnk_import.visible = True
      else:
        self.lnk_menu_useradmin.visible = False
        self.lnk_menu_logins.visible = False
        self.lnk_menu_searches.visible = False
        self.lnk_import.visible = False

    else:
      self.lnk_ccs_compare.visible = False
      self.lnk_menu_useradmin.visible = False
      self.lnk_menu_logins.visible = False
      self.lnk_change_password.visible = False

  def link_change_password_clicked (self, **event_args):
#     analytics.track('Clicked Change Password Button', { 'location': 'sidebar', 'item': 'lnk_changepassword' })
    u = anvil.users.get_user()
    if u:
      print("Initiating password reset")
      anvil.users.send_password_reset_email(u['email'])
      alert("You will receive an email with instructions for resetting your password.")

  def lnk_help_click (self, **event_args):
#     analytics.track('Clicked Help Button', { 'location': 'sidebar', 'item': 'lnk_help' })
    self.content_panel.clear()
    self.content_panel.add_component(HelpForm())

  def lnk_import_click (self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(ImportForm())

