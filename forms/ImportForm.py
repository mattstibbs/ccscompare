from anvil import *
import google.auth, google.drive
from google.drive import app_files
import anvil.users
import anvil.server
import tables
from tables import app_tables

class ImportForm (ImportFormTemplate):
  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    
  def file_loader_1_change (self, files, **event_args):
    for f in files:
      print(f)
      print(f.get_bytes())
#       anvil.server.call('import_sgsd_csv',f)
    x = anvil.BlobMedia("text/plain", "foo")
    anvil.server.call('import_sgsd_csv',x)

  def file_loader_2_change (self, files, **event_args):
    for f in files:
      anvil.server.call('import_dispositions',f)    

