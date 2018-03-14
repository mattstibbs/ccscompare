import anvil.users
import tables
from tables import app_tables
import anvil.secrets
import anvil.server
import anvil.http

@anvil.server.callable
def get_postcode_whitelist(postcode):
  url = 'https://int3-ccgservice.staging.111.service.nhs.uk/api/ccg/details/{}'.format(postcode)

  try:
    result = anvil.http.request(url, json=True)
    return result
  except anvil.http.HttpError as e:
    if e.status == 404:
      return None
