from anvil import *
import anvil.users
import anvil.server
import tables
from tables import app_tables

class ImportForm (ImportFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    print(len(app_tables.sg_sd.search()))
    print(len(app_tables.dispositions.search()))
    
  def file_loader_1_change (self, file, **event_args):
    print(file)
    print(file.get_bytes())
    anvil.server.call('import_sgsd_csv',file)

  def file_loader_2_change (self, files, **event_args):
    for f in files:
      anvil.server.call('import_dispositions',f)    

