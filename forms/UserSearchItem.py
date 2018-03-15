from anvil import *
import anvil.server
import anvil.users
import tables
from tables import app_tables
import json

class UserSearchItem (UserSearchItemTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def link_1_click (self, **event_args):
    if self.pnl_details.visible == True:
      self.pnl_details.visible = False
    else:
      self.pnl_details.visible = True

  def button_1_click (self, **event_args):
    # This method is called when the button is clicked
    row = self.item
    previous_search = dict(list(row))
    previous_search['sg_code'] = "{}{}".format("SG", previous_search['sgsd'].split(':')[0])
    previous_search['sd_code'] = "{}{}".format("SD", previous_search['sgsd'].split(':')[1])
    get_open_form().load_ccs_compare_form(previous_search=self.item)

  def label_5_show (self, **event_args):
    # This method is called when the Label is shown on the screen
    pass

