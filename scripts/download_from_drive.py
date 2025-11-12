import os, json, google.auth
from google.oauth2 import service_account

creds_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
creds = service_account.Credentials.from_service_account_info(creds_info)