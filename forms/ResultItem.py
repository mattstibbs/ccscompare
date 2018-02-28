from anvil import *
import anvil.users
import tables
from tables import app_tables
import anvil.server

class ResultItem (ResultItemTemplate):
  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)
    
  def get_bg_colour(self):
    if self.item['difference'] == 'Same':
      return ''
    elif self.item['difference'] == 'Higher':
      return '#ece3b1'
    elif self.item['difference'] == 'Lower':
      return '#ece3b1'
    elif self.item['difference'] == 'NoMatch':
      return ''
    
  def get_position(self):
    if self.item['difference'] == 'Same':
      return 'Same'
    elif self.item['difference'] == 'Higher':
      return 'Higher'
    elif self.item['difference'] == 'Lower':
      return 'Lower'
    elif self.item['difference'] == 'NoMatch':
      return 'Missing'    