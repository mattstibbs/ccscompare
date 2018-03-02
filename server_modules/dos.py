import anvil.users
import tables
from tables import app_tables
import anvil.secrets
import anvil.server
import anvil.http
import anvil.users
import ccs
import datetime
import json


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
                              username=anvil.secrets.get_secret('dos_username_uat1'),
                              password=anvil.secrets.get_secret('dos_password_uat1'), 
                              json=True)
  results = result['success']['services']
  
  new_result_list = [extract_result(r) for r in results]

  return new_result_list


@anvil.server.callable
def check_capacity_summary(postcode, surgery, age_group, sex, sg_code, sd_code, dispo_code, search_distance, instance1, instance2, instance1_creds=None, instance2_creds=None):
  
  result = ccs.get_services(postcode, surgery, age_group, sg_code, sd_code, dispo_code, search_distance, sex, instance1, instance2, instance1_creds, instance2_creds)
  
  app_tables.log_searches.add_row(timestamp=datetime.datetime.now(),
                                user=anvil.users.get_user(),
                                postcode=postcode,
                                surgery=surgery,
                                age_group=age_group,
                                sex=sex, 
                                disposition=dispo_code, 
                                sgsd="{}:{}".format(sg_code, sd_code),
                                search_distance=int(search_distance),
                                left_instance=instance1,
                                right_instance=instance2,
                                results=json.dumps(result))
  
  return result


@anvil.server.callable
def search_surgeries(postcode):
  try:
    result = anvil.http.request(url='https://uat.pathwaysdos.nhs.uk/app/controllers/api/v1.0/services/byServiceType/TEST/{}/20/0/0/0/0/100/100'.format(postcode), 
                                username=anvil.secrets.get_secret('dos_username_uat1'),
                                password=anvil.secrets.get_secret('dos_password_uat1'), 
                                json=True)
    results = result['success']['services']
    
  except anvil.http.HttpError as e:
    if e.status == 400:
      print("Bad postcode")
      results = []

  new_result_list = [extract_result(r) for r in results]
  return new_result_list