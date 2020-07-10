from creds_wrapper import CredentialWrapper
from azure.mgmt.resource import SubscriptionClient
import os

# Get configuration
clientId = "7bd893a7-9990-4097-b8a6-ac8b4ce18af1"
tenantId = "6005dfb1-84f6-4005-8ae1-77f26eb7aac7"
subscriptionId = "da05ac29-8f4c-4a13-8c3e-43b5a925aba3"
adtInstanceUrl = "https://myazdtph300620.api.neu.digitaltwins.azure.net"

# Set env variables for authentication
os.environ["AZURE_CLIENT_ID"] = clientId
os.environ["AZURE_TENANT_ID"] = tenantId
os.environ["AZURE_CLIENT_SECRET"] = "2p1e.~DCzYOnE6dPQKu7B0slHlh~6k_ih2"

credential = CredentialWrapper()
subscription_client = SubscriptionClient(credential)
subscription = next(subscription_client.subscriptions.list())
print(subscription.subscription_id)