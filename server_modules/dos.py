import tables
from tables import app_tables
import anvil.secrets
import anvil.server


def extract_result(result):
  new_result = {
    'name': result['name'],
    'address': "".join(result['address']),
    'odscode': result['odsCode']
  }
  return new_result


@anvil.server.callable
def get_results(postcode):
  result = anvil.http.request(url=f'https://uat.pathwaysdos.nhs.uk/app/controllers/api/v1.0/services/byServiceType/TEST/{postcode}/100/0/0/0/0/131/10', 
                              username=anvil.secrets.get_secret('dos_username'),
                              password=anvil.secrets.get_secret('dos_password'), 
                              json=True)
  results = result['success']['services']
  
  new_result_list = [extract_result(r) for r in results]
  print(new_result_list)
  return new_result_list
