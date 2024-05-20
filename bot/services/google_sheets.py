from aiogoogle import Aiogoogle
from googleapiclient.http import MediaFileUpload
from aiogoogle.auth.creds import ServiceAccountCreds

from bot.utils.google_auth import creds_auth

async def upload_photo_to_drive(save_path, folder_id='1KE-y3zQAl6gxWv6RIPKRyuykFHS9ofcq'):
    async with Aiogoogle(service_account_creds=creds_auth) as aiogoogle:
        disk = await aiogoogle.discover("drive", "v3")
        media = MediaFileUpload(save_path, mimetype="image/jpeg")
        file_metadata = {
            "name": save_path,
            "parents": [folder_id],
            "mimeType": "image/jpeg"
        }
        file = disk.files.create(json=file_metadata, upload_file=save_path, fields="webViewLink, id")
        upload_res = await aiogoogle.as_service_account(file)
        return upload_res.get("webViewLink")

async def append_to_sheet(sheet_id, data, sheet_range="Лист1!A1", flag=True):
    async with Aiogoogle(service_account_creds=creds_auth) as aiogoogle:
        sheets = await aiogoogle.discover("sheets", "v4")
        file = sheets.spreadsheets.values.append(
            spreadsheetId=sheet_id,
            range=sheet_range,
            json=data,
            valueInputOption='USER_ENTERED'
        )
        res = await aiogoogle.as_service_account(file)
        return res
