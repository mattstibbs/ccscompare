import google.auth, google.drive, google.mail
from google.drive import app_files
import anvil.users
import tables
from tables import app_tables
import anvil.secrets
import anvil.server
import anvil.http

def get_postcode_info(postcode):
  url = 'https://int3-ccgservice.staging.111.service.nhs.uk/api/ccg/{}'.format(postcode)
  result = anvil.http.request(url, json=True)
  if result:
    print(result)

get_postcode_info('ME13DX')