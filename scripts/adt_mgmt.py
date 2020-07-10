import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import digitaltwins as adt
import logging
from azure.common.credentials import ServicePrincipalCredentials
import json

# Load Config file
with open(r"settings.json") as f:
  config = json.load(f)
# Get configuration
clientId = config["clientId"]
tenantId = config["tenantId"]
subscriptionId = config["subscriptionId"]
adtInstanceUrl = config["adtInstanceUrl"]
clientSecret = config["clientSecret"]

logging.info("Hello ADT!")

# Obtain the credential object. When run locally, DefaultAzureCredential relies
# on environment variables named AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, and AZURE_TENANT_ID.
credentials = ServicePrincipalCredentials(
    client_id = clientId,
    secret = clientSecret,
    tenant = tenantId
)

try:
    client = adt.AzureDigitalTwinsManagementClient(credentials = credentials, subscription_id = subscriptionId , base_url = adtInstanceUrl)
    logging.info("Service client created – ready to go")
except ValueError as err:
    print('Client creation failed with error: {0}'.format(err))

# List digital twins in a subscription
result = client.digital_twins.list()
for r in result:
    print(json.dumps(r.as_dict(), indent=4))

# List instances of a digital twin
instances = client.digital_twins.get(resource_group_name = 'azdtpreview', resource_name = 'myazdtph300620')
print(json.dumps(instances.as_dict(), indent=4))
#for i in instances:
#    print(json.dumps(i.as_dict(), indent=4))
