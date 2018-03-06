import google.auth, google.drive, google.mail
from google.drive import app_files
import anvil.users
import tables
from tables import app_tables
import anvil.secrets
import anvil.server
from anvil.server import http_endpoint, request

@http_endpoint('/check_pending_users', require_credentials=True)
def check_pending():
  if request.username == anvil.secrets.get_secret('endpoint_username') and request.password == anvil.secrets.get_secret('endpoint_password'):
    print("Checking for unauthorised users")
    for u in app_tables.users.search(confirmed_email=True, enabled=False):
      print(u['admin_notified'])
    waiting_users = app_tables.users.search(confirmed_email=True, enabled=False, admin_notified=False)
     
    if len(waiting_users) > 0:
      for user in waiting_users:   
        print("{} is waiting".format(user['email']))
        google.mail.send(to = 'mattstibbs@gmail.com',
                          subject = "User waiting for authorisation",
                          text = "{} is waiting for you to enable their account".format(user['email'])
                        )
        
        user['admin_notified'] = True
        print("Sent admin notification email for {}".format(user['email']))
      response = anvil.server.HttpResponse(200, "Request successful")
      return response
    else:
      response = anvil.server.HttpResponse(200, "No users waiting")
      return response
  
  else:
    
    response = anvil.server.HttpResponse(401, "Invalid credentials")
    return response
