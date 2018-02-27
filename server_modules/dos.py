import anvil.users
import tables
from tables import app_tables
import anvil.secrets
import anvil.server
import anvil.http


def extract_result(result):
  new_result = {
    'name': result['name'],
    'address': "".join(result['address']),
    'odscode': result['odsCode']
  }
  return new_result


@anvil.server.callable
def search_by_service_type(postcode):
  result = anvil.http.request(url='https://uat.pathwaysdos.nhs.uk/app/controllers/api/v1.0/services/byServiceType/TEST/{}/100/0/0/0/0/131/10'.format(postcode), 
                              username=anvil.secrets.get_secret('dos_username'),
                              password=anvil.secrets.get_secret('dos_password'), 
                              json=True)
  results = result['success']['services']
  
  new_result_list = [extract_result(r) for r in results]
  print(new_result_list)
  return new_result_list


@anvil.server.callable
def check_capacity_summary(postcode, age_group, sex, sg_code, sd_code, dispo_code, search_distance):
  for arg in locals():
    print(arg)


@anvil.server.callable
def search_surgeries(postcode):
  result = anvil.http.request(url='https://uat.pathwaysdos.nhs.uk/app/controllers/api/v1.0/services/byServiceType/TEST/{}/100/0/0/0/0/100/100'.format(postcode), 
                              username=anvil.secrets.get_secret('dos_username'),
                              password=anvil.secrets.get_secret('dos_password'), 
                              json=True)
  results = result['success']['services']
  
  new_result_list = [extract_result(r) for r in results]
  print(new_result_list)
  return new_result_list