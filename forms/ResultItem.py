from anvil import *
import segment.client as analytics
import google.auth, google.drive
from google.drive import app_files
import anvil.users
import tables
from tables import app_tables
import anvil.server

class ResultItem (ResultItemTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    
  def get_bg_colour(self):
    if self.item['difference'] == 'Same':
      return ''
    elif self.item['difference'] == 'Higher':
      return '#c9efee'
    elif self.item['difference'] == 'Lower':
      return '#ece3b1'
    elif self.item['difference'] == 'NoMatch':
      return '#d5d5d5'
    
  def get_position(self):
    if self.item['difference'] == 'Same':
      return 'Same ranking as other results'
    elif self.item['difference'] == 'Higher':
      return 'Ranked higher in these results'
    elif self.item['difference'] == 'Lower':
      return 'Ranked lower in these results'
    elif self.item['difference'] == 'NoMatch':
      return 'Not returned in the other results'    
    
  def get_icon(self):
    if self.item['difference'] == 'Same':
      return 'fa:arrows-h'
    elif self.item['difference'] == 'Higher':
      return 'fa:arrow-up'
    elif self.item['difference'] == 'Lower':
      return 'fa:arrow-down'
    elif self.item['difference'] == 'NoMatch':
      return 'fa:ban'
    
  def get_distance(self):
    return '{} mi'.format(self.item['distance'])