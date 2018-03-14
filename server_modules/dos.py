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
    'odscode': result['odsCode'],
    'distance': result['patientDistance']
  }
  return new_result


@anvil.server.callable
def search_by_service_type(postcode):
  result = anvil.http.request(url='https://www.pathwaysdos.nhs.uk/app/controllers/api/v1.0/services/byServiceType/TEST/{}/100/0/0/0/0/131/10'.format(postcode), 
                              username=anvil.secrets.get_secret('dos_username_pathways_live'),
                              password=anvil.secrets.get_secret('dos_password_pathways_live'), 
                              json=True)
  results = result['success']['services']
  
  new_result_list = [extract_result(r) for r in results]

  return new_result_list


@anvil.server.callable
def check_capacity_summary(postcode, surgery, age_group, sex, sg_code, sd_code, dispo_code, search_distance, instance1, instance2, instance1_referral_role, instance2_referral_role, instance1_creds=None, instance2_creds=None):
  
  result = ccs.get_services(
    postcode, 
    surgery, 
    age_group, 
    sg_code, 
    sd_code, 
    dispo_code, 
    search_distance, 
    sex, 
    instance1, 
    instance2, 
    instance1_referral_role, 
    instance2_referral_role, 
    instance1_creds, 
    instance2_creds)
  
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
                                  left_referral_role=instance1_referral_role,
                                  right_referral_role=instance2_referral_role,
                                  results=json.dumps(result)
                                 )
  
  return result


@anvil.server.callable
def search_surgeries(postcode):
  try:
    result = anvil.http.request(url='https://www.pathwaysdos.nhs.uk/app/controllers/api/v1.0/services/byServiceType/TEST/{}/50/0/0/0/0/100/100'.format(postcode), 
                                username=anvil.secrets.get_secret('dos_username_pathways_live'),
                                password=anvil.secrets.get_secret('dos_password_pathways_live'), 
                                json=True)
    results = result['success']['services']
    
  except anvil.http.HttpError as e:
    if e.status == 400:
      print("Bad postcode")
      results = []

  new_result_list = [extract_result(r) for r in results]
  return new_result_list


@anvil.server.callable
def validate_postcode(postcode):
  try:
    result = anvil.http.request(url='https://www.pathwaysdos.nhs.uk/app/controllers/api/v1.0/services/byServiceType/TEST/{}/1/0/0/0/0/-1/1'.format(postcode),
                                username=anvil.secrets.get_secret('dos_username_pathways_live'),
                                password=anvil.secrets.get_secret('dos_password_pathways_live'), 
                                json=True)
    print(result)
  
  except:
    pass