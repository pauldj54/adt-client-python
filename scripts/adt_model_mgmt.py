import os, msal 
from msrest.authentication import OAuthTokenAuthentication 
from azure.core.credentials import AccessToken

import adtdataplane 
import logging
from azure.mgmt.consumption.models.error_response import ErrorResponseException
from azure.common.credentials import ServicePrincipalCredentials
#from msrestazure.azure_active_directory import ServicePrincipalCredentials
import json

# Load Config file
with open(r"settings.json") as f:
  config = json.load(f)

subscriptionId = config["subscriptionId"]
clientId = config["clientId"]
tenantId = config["tenantId"]
clientSecret = config['clientSecret']
baseUrl = config["baseUrl"]
adt_id = "/subscriptions/da05ac29-8f4c-4a13-8c3e-43b5a925aba3/resourceGroups/azdtpreview/providers/Microsoft.DigitalTwins/digitalTwinsInstances/myazdtph300620"
logging.info("Hello ADT!")
adtAppId = "https://digitaltwins.azure.net"
authority = "https://login.microsoftonline.com/" + config["tenantId"]

# Build service principal credentials
#credentials = ServicePrincipalCredentials(client_id = clientId, secret = clientSecret, tenant = tenantId) 
#credentials = ServicePrincipalCredentials(client_id = clientId, secret = clientSecret) 
app = msal.ConfidentialClientApplication(
    config["clientId"], authority=authority,
    client_credential=config['clientSecret'],
    # token_cache=...  # Default cache is in memory only.
                       # You can learn how to use SerializableTokenCache from
                       # https://msal-python.rtfd.io/en/latest/#msal.SerializableTokenCache
    )

# The pattern to acquire a token looks like this.
result = None

# Firstly, looks up a token from cache
# Since we are looking for token for the current app, NOT for an end user,
# notice we give account parameter as None.
result = app.acquire_token_silent(config["scope"], account=None)

if not result:
    logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
    result = app.acquire_token_for_client(scopes=config["scope"])

credentials = OAuthTokenAuthentication(config['clientId'],result['access_token'])

try:
    client = adtdataplane.AzureDigitalTwinsAPI(credentials = credentials, base_url = baseUrl)
    logging.info("Service client created – ready to go")
except ValueError as err:
    print('Client creation failed with error: {0}'.format(err))

# load models
# Load model file
with open(r"models\SampleModel.json") as f:
  dtdl = json.load(f)
dtdl_list = []
dtdl_list.append(dtdl)
try:
    client.digital_twin_models.add(dtdl_list)
except ValueError as err:
    print("Model upload failed with error: {0}".format(err))

# Get instances 
#result = client.digital_twin_models.list(raw=True)
#print(result)
#print(result.raw.response)
#while(result.next.values)
#for r in result:
#    print(json.dumps(r.as_dict(), indent=4))
