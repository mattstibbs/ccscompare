import anvil.users
import tables
from tables import app_tables
import anvil.secrets
import anvil.server
import dos

@anvil.server.callable
def get_dispositions():
  all_results = app_tables.dispositions.search()
  results = [("{} ({})".format(result['DispoDescription'],result['DispoCode']), result['CMSGroup']) for result in all_results]
  results.append(("",0))
  results = set(results)
  results = sorted(list(results))
  print(results)
  return results

@anvil.server.callable
def get_sg_list():
  all_results = app_tables.sg_sd.search()
  results = [("{} ({})".format(result['sg_description'],result['sg_code']), result['sg_code']) for result in all_results]
  results.append(("",0))
  results = set(results)
  results = sorted(list(results))
  print(results)
  return results

@anvil.server.callable
def get_sd_list(sg_code):
  all_results = app_tables.sg_sd.search(sg_code=sg_code)
  results = [("{} ({})".format(result['sd_description'],result['sd_code']), result['sd_code']) for result in all_results]
  results = set(results)
  results = sorted(list(results))
  print(results)
  return results

@anvil.server.callable
def get_surgeries(postcode):
  all_results = dos.search_surgeries(postcode)
  results = [("{} ({})".format(result['name'],result['odscode']), result['odscode']) for result in all_results]
  results.append(("", "UNK"))
  results = set(results)
  results = sorted(list(results))
  print(results)
  return results