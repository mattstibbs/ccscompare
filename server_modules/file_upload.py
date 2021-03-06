import anvil.email
import anvil.users
import tables
from tables import app_tables
import anvil.secrets
import anvil.server
import csv

@anvil.server.callable
def import_sgsd_csv(csv_object):
  # Get the data as bytes.
  csv_bytes=csv_object.get_bytes()
  # Convert bytes to a string.
  csv_string=str(csv_bytes,"utf-8")
  # Create a list of lines split on \n
  line_list=csv_string.split('\n')
  reader = csv.DictReader(line_list)
  
  for row in reader:
    app_tables.sg_sd.add_row(sg_code=row['SG'], sg_description=row['SGDescription'], sd_code=row['SD'], sd_description=row['SDDescription'])
  

@anvil.server.callable
def import_dispositions(csv_object):
  # Get the data as bytes.
  csv_bytes=csv_object.get_bytes()
  # Convert bytes to a string.
  csv_string=str(csv_bytes,"utf-8")
  # Create a list of lines split on \n
  line_list=csv_string.split('\n')
  reader = csv.DictReader(line_list)
  
  for row in reader:
    app_tables.dispositions.add_row(DispoCode=row['DispoCode'], DispoDescription=row['DispoDescription'], CMSGroup=row['CMSGroup'])


