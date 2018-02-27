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


def convert_xml_to_dict(xml_string):
  result_dict = xmltodict.parse(xml_string)
#   print(result_dict)
  result_list = result_dict['env:Envelope']['env:Body']['ns1:CheckCapacitySummaryResponse']['ns1:CheckCapacitySummaryResult']['ns1:ServiceCareSummaryDestination']
#   result_list = result_dict['env:Envelope']['env:Body']
#   ['ns1:CheckCapacitySummaryResponse']['ns1:CheckCapacitySummaryResult']
#   ['ns1:ServiceCareSummaryDestination']
  
  print(result_list)
  
  service = collections.namedtuple('Service', ['id', 'name', 'address', 'capacity_rag', 'service_type'])
  
  service_list = []
  
  for r in result_list:
    s = service()
    s.id = r['ns1:id']
    s.name = r['ns1:name']
    s.address = ""
    s.capacity_rag = ""
    s.service_type = ""
    print(s)
    service_list.append(s)


def get_services(postcode, surgery, age_group, sg_code, sd_code, disposition, search_distance, sex):
  user = get_user()
  case = get_case(postcode, surgery, age_group, sg_code, sd_code, disposition, search_distance, sex)
  
  payload = payloads.generate_ccs_payload(user, case)
#   print(payload)

  result = anvil.http.request(url='https://uat.pathwaysdos.nhs.uk/app/api/webservices', 
                              data=payload,
                              headers={"content-type": "application/xml"},
                              method="POST")
  print(result.content_type)
  print(result.get_bytes())
  
  json_result = convert_xml_to_dict(result.get_bytes())
 
  return result

# # Parse the returned XML into an object representing the XML structure
# document = untangle.parse(result.text)

# # Define the contents of the <feed> element as its own object
# feed = document.feed
