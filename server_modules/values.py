import anvil.users
import tables
from tables import app_tables
import anvil.secrets
import anvil.server
import dos

@anvil.server.callable
def get_dispositions():
  all_results = app_tables.dispositions.search()
  results = [("{} ({})".format(result['DispoDescription'].replace('The disposition is:', ''),result['DispoCode']), result['CMSGroup']) for result in all_results]
  results.append(("",0))
  results = set(results)
  results = sorted(list(results))
  return results

@anvil.server.callable
def get_sg_list():
  all_results = app_tables.sg_sd.search()
  results = [("{} ({})".format(result['sg_description'],result['sg_code']), result['sg_code']) for result in all_results]
  results.append(("",0))
  results = set(results)
  results = sorted(list(results))
  return results

@anvil.server.callable
def get_sd_list(sg_code):
  all_results = app_tables.sg_sd.search(sg_code=sg_code)
  results = [("{} ({})".format(result['sd_description'],result['sd_code']), result['sd_code']) for result in all_results]
  results.append(("",0))
  results = set(results)
  results = sorted(list(results), reverse=True)
  return results

@anvil.server.callable
def get_surgeries(postcode):
  all_results = dos.search_surgeries(postcode)
  results = [("{} ({})".format(result['name'],result['odscode']), result['odscode']) for result in all_results]
  results.append(("", "UNK"))
  results = set(results)
  results = sorted(list(results))
  return results

@anvil.server.callable
def get_previous_search():
  me = anvil.users.get_user()
  if me:
    rows = app_tables.log_searches.client_readable(user=me).search(tables.order_by("timestamp", ascending=False))
    if len(rows) > 0:
      row = rows[0]
      new = dict(row)
      new.pop('results')
      new.pop('timestamp')
      new['sg_code'] = "{}{}".format("SG", new['sgsd'].split(':')[0])
      new['sd_code'] = "{}{}".format("SD", new['sgsd'].split(':')[1])
      return new
    else:
      return None
  
