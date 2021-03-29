"""
공통처리 모듈 정의
"""
import os
import uuid
import logging
import hashlib
from urllib.parse import urlencode, quote_plus
import jwt
import requests
import telegram

access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']

telegram_access_token = os.environ['TELEGRAM_BOT_ACCESS_TOKEN']
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
telegram_bot = telegram.Bot(telegram_access_token)

CHAT_ID = '948219871'


def upbit_request(method, sub_url, query):
    """
    upbit 요청 URL 공통 모듈
    """
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    if query != {}:
        query_string = urlencode(query).encode()
        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()

        payload['query_hash'] = query_hash
        payload['query_hash_alg'] = 'SHA512'

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    if method.lower() == 'post':
        if query == {}:
            return requests.post(server_url + sub_url, headers=headers)
        return requests.post(server_url + sub_url, params=query_string, headers=headers)
    elif method.lower() == 'delete':
        if query == {}:
            return requests.delete(server_url + sub_url, headers=headers)
        return requests.delete(server_url + sub_url, params=query_string, headers=headers)
    else:
        if query == {}:
            return requests.get(server_url + sub_url, headers=headers)
        return requests.get(server_url + sub_url, params=query_string, headers=headers)
