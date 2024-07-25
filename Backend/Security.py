# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: Backend\Security.py
# Bytecode version: 3.10.0rc2 (3439)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

from datetime import datetime
from Backend.TTS import TTS
from pathlib import Path
from time import sleep
import hashlib
import os
import requests as rq

def ClientAPIKey():
    folder_path = Path(f'C:/Users/{os.getlogin()}')
    creation_time = folder_path.stat().st_ctime
    creation_time_readable = datetime.fromtimestamp(creation_time)

    def sha256_hash(data: str):
        data = data.encode('utf-8')
        return hashlib.sha256(data).hexdigest()
    hashed_data = sha256_hash(str(creation_time_readable))
    return hashed_data

def Keys():
    keys = rq.get('https://raw.githubusercontent.com/Divy0The0Fire/J4E/main/keys').text.strip()
    keys.splitlines()
    return keys

if ClientAPIKey() not in Keys():
    TTS('Your AI Assistant is not activated, Kindly send us your activated key.')
    sleep(1000)
    exit()
