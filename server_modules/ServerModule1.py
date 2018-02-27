import anvil.users
import tables
from tables import app_tables
import anvil.secrets
import anvil.server
import anvil.http
import untangle
import payloads

payload = payloads.
result = anvil.http.post(url='', data=payload)

# Parse the returned XML into an object representing the XML structure
document = untangle.parse(result.text)

# Define the contents of the <feed> element as its own object
feed = document.feed

