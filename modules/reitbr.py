# %%
import pandas as pd
import numpy as np
import datetime as dt

# %%
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials


# %%
def reitbrData (reitbrfile, reitbr_ticker):
    '''
    function to read BR reit file from excel file
    args:
    reitbr_ticker - [type]: list
    reitbrfile - [type]: excel file name
    returns
    [type]: [pandas.core.frame.DataFrame]
    '''
    # check reitbrfile file name and path
    # create reitbrfile from Funds Explorer Table in https://www.fundsexplorer.com.br/ranking
    # manually select all columns in web page copy and paste all data AS VALUES ONLY in a excel file sheet

    # scopes and paths
    scope = ['https://www.googleapis.com/auth/drive']

    # credentials json path
    jasonpath = '/home/maber/keys/googlekey.json'

    # Autenticação centralizada para os dois serviços
    credentials = Credentials.from_service_account_file(jasonpath, scopes=scope)
   
    # Google Drive access
    drive_service = build('drive', 'v3', credentials=credentials)

    # Busca um arquivo pelo nome exato dentro do Drive
    # Busca um arquivo pelo nome exato dentro do Drive (Corrigido)
    answer_excel = drive_service.files().list(q=f"name = '{reitbrfile}'", fields="files(id, name)").execute()
    excel_id = answer_excel.get('files', [])[0]['id']
    file = answer_excel.get('files', [])
    print("File found:", file[0]['name'], "ID:", file[0]['id'])

    # Baixar arquivo do Drive e carregar no Pandas
    request = drive_service.files().get_media(fileId=excel_id)
    file_stream = io.BytesIO()
    downloader = MediaIoBaseDownload(file_stream, request)

    done = False
    while not done:
        _, done = downloader.next_chunk()

    file_stream.seek(0)
    df = pd.read_excel(file_stream)

    return df


