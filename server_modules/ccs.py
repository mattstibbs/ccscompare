import google.auth, google.drive, google.mail
from google.drive import app_files
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
import online_api

class CCSError(Exception):
  pass

def get_user(instance=None, referral_role=None, username=None, password=None):
  if instance and referral_role == 'pathways':
    user = collections.namedtuple('User', ['username', 'password'])
    user.username = anvil.secrets.get_secret('dos_username_{}_{}'.format(referral_role, instance))
    user.password = anvil.secrets.get_secret('dos_password_{}_{}'.format(referral_role, instance))
  elif instance and referral_role == 'digital':
    user = collections.namedtuple('User', ['username', 'password'])
    user.username = anvil.secrets.get_secret('dos_username_{}_{}'.format(referral_role, instance))
    user.password = anvil.secrets.get_secret('dos_password_{}_{}'.format(referral_role, instance))
  elif referral_role == 'own' and username and password:
    user = collections.namedtuple('User', ['username', 'password'])
    user.username = username
    user.password = password
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
  
  case.case_ref = 'TEST'
  case.case_id = 'TEST'
  case.postcode = postcode
  case.surgery = surgery if surgery != '' else 'UNK'
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
    distance = float(r['ns1:distance'])
    s = service(r['ns1:id'], r['ns1:name'], r['ns1:address'], "", r['ns1:serviceType']['ns1:name'], (result_list.index(r) + 1), distance)
    service_list.append(s._asdict())
    
  return service_list


def extract_http_error(content):
  error = content.get_bytes()
  result_dict = xmltodict.parse(error)
  error_code = result_dict['env:Envelope']['env:Body']['env:Fault']['env:Code']['env:Value']
  error_text = result_dict['env:Envelope']['env:Body']['env:Fault']['env:Reason']['env:Text']
  return error_code, error_text 

def do_ccs_request(instance, payload, username):
  urls = {
    'live': 'https://www.pathwaysdos.nhs.uk/app/api/webservices',
    'uat1': 'https://uat.pathwaysdos.nhs.uk/app/api/webservices',
    'uat2': 'https://uat2.pathwaysdos.nhs.uk/app/api/webservices',
    'uat3': 'https://uat3.pathwaysdos.nhs.uk/app/api/webservices'
  }
  
  try:
    result = anvil.http.request(url=urls[instance], 
                                data=payload,
                                headers={"content-type": "application/xml"},
                                method="POST")  
    
    print("Performing CCS for {} using {}".format(instance, username))
    
    return result
  
  except anvil.http.HttpError as e:
    if e.status == 500:
      error_code, error_message = extract_http_error(e.content)
      raise CCSError("{} ({})".format(error_message, error_code))

  return None

def get_services(postcode, surgery, age_group, sg_code, sd_code, disposition, search_distance, sex, instance1, instance2, instance1_referral_role, instance2_referral_role, instance1_creds, instance2_creds):

  if instance1_creds and instance1_referral_role == 'own':
    user1 = get_user(referral_role=instance1_referral_role, 
                     username=instance1_creds[0], 
                     password=instance1_creds[1])
  else:
    user1 = get_user(instance1, instance1_referral_role)

  if instance2_creds and instance2_referral_role == 'own':
    user2 = get_user(referral_role=instance2_referral_role, 
                     username=instance2_creds[0], 
                     password=instance2_creds[1])
  else:
    user2 = get_user(instance2, instance2_referral_role)

  case = get_case(postcode, surgery, age_group, sg_code, sd_code, disposition, search_distance, sex)
  
  try:
    whitelist = online_api.get_postcode_whitelist(postcode)['serviceIdWhitelist']
  except:
    print("Failed getting whitelist")
  
  try:
    # do left-hand search  
    payload = payloads.generate_ccs_payload(user1, case)
      
    result = do_ccs_request(instance1, payload, user1.username)
      
    result_list_1 = convert_xml_to_list(result.get_bytes())
    
    # do right-hand search
    payload = payloads.generate_ccs_payload(user2, case)
    
    result = do_ccs_request(instance2, payload, user2.username)
    
    result_list_2 = convert_xml_to_list(result.get_bytes())
  
    result_map_1 = collections.OrderedDict()
    result_map_2 = collections.OrderedDict()
    
    for idx, r in enumerate(result_list_1):
      result_map_1[r['id']] = r
    
    for idx, r in enumerate(result_list_2):
      result_map_2[r['id']] = r 
    
    print(result_list_1)
    print('----------------')
    for key, res2 in result_map_2.items():
      try:
        res1 = result_map_1[res2['id']]
        if res1['order_number'] > res2['order_number']:
          res1['difference'] = 'Lower'
          res2['difference'] = 'Higher'
        elif res1['order_number'] < res2['order_number']:
          res1['difference'] = 'Higher'
          res2['difference'] = 'Lower'  
        elif res1['order_number'] == res2['order_number']:
          res1['difference'] = 'Same'
          res2['difference'] = 'Same'
      except KeyError:
        res2['difference'] = 'NoMatch'
        
      for key, res2 in result_map_1.items():
        try:
          if res2['difference']:
            pass
        except KeyError:
          res2['difference'] = 'NoMatch'
  
    print(result_list_1)
    print('----------------')
    whitelist = ['1338216856']
    if instance1_referral_role == 'digital':
      for r in result_list_1:
        r['inWhitelist'] = r['id'] in whitelist
        print(r['id'] in whitelist)
    else:
      for r in result_list_1:
        r['inWhitelist'] = False      
        
    if instance2_referral_role == 'digital':
      for r in result_list_2:
        r['inWhitelist'] = r['id'] in whitelist
        print(r['id'] in whitelist)
      else:
        for r in result_list_2:
          r['inWhitelist'] = False   
    
    print(result_list_1)
    print('----------------')   
    
    return {'results1': result_list_1, 'results2': result_list_2}
    
  except CCSError as e:
      return {'error': str(e)}
