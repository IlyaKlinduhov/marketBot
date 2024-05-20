import json
from aiogoogle.auth.creds import ServiceAccountCreds
import os

cred_file_path = os.path.join('..', 'cred1.json')

with open(cred_file_path) as f:
    service_account_key = json.load(f)

creds_auth = ServiceAccountCreds(
    scopes=[
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file'
    ],
    **service_account_key
)
