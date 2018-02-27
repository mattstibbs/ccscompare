import anvil.users
import tables
from tables import app_tables
import anvil.secrets
import anvil.server
import anvil.http
import payloads
import collections
import xmltodict
import json

def get_user():
  user = collections.namedtuple('User', ['username', 'password'])
  user.username = anvil.secrets.get_secret('dos_username')
  user.password = anvil.secrets.get_secret('dos_password')
  return user

def get_case(postcode, surgery, age_group, sg_code, sd_code, disposition, search_distance, sex):
                                        
  case = collections.namedtuple('Case', [
    'case_ref',
    'case_id',
    'postcode',
    'surgery',
    'age',
    'age_format',
    'disposition',
    'symptom_group',
    'symptom_discriminator',
    'search_distance',
    'sex'])
  
  case.case_ref = 'UAT'
  case.case_id = 'UAT'
  case.postcode = postcode
  case.surgery = surgery
  case.age = age_group
  case.age_format = 'AgeGroup'
  case.disposition = disposition
  case.symptom_group = sg_code
  case.symptom_discriminator = sd_code
  case.search_distance = search_distance
  case.sex = sex
  
  return case


def convert_xml_to_list(xml_string):
  result_dict = xmltodict.parse(xml_string)
  result_list = result_dict['env:Envelope']['env:Body']['ns1:CheckCapacitySummaryResponse']['ns1:CheckCapacitySummaryResult']['ns1:ServiceCareSummaryDestination']
  
  service = collections.namedtuple('Service', ['id', 'name', 'address', 'capacity_rag', 'service_type', 'order_number', 'distance'])
  
  service_list = []
  
  for r in result_list:
    distance = "{}km".format(r['ns1:distance'])
    s = service(r['ns1:id'], r['ns1:name'], r['ns1:address'], "", r['ns1:serviceType']['ns1:name'], (result_list.index(r) + 1), distance)
    service_list.append(s._asdict())
  
  print(service_list)
    
  return service_list


def get_services(postcode, surgery, age_group, sg_code, sd_code, disposition, search_distance, sex):
  user = get_user()
  case = get_case(postcode, surgery, age_group, sg_code, sd_code, disposition, search_distance, sex)
  
  payload = payloads.generate_ccs_payload(user, case)

  result = anvil.http.request(url='https://uat.pathwaysdos.nhs.uk/app/api/webservices', 
                              data=payload,
                              headers={"content-type": "application/xml"},
                              method="POST")
  print(result.content_type)
  print(result.get_bytes())
  
  result_list = convert_xml_to_list(result.get_bytes())
 
  return result_list

