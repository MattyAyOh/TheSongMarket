from apiCredentials import *
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import requests
import hmac
import hashlib
import base64

def tsmApiRequest(request_path, m_data={}, m_headers={}, method='get'):
    current_date = format_date_time(mktime(datetime.now().timetuple()))
    canonical_str = request_path + ':' + current_date
    digest_maker = hmac.new(tsmApiSecretKey, '', hashlib.sha1)
    digest_maker.update(canonical_str)
    digest = digest_maker.hexdigest() + '\n'
    auth_header = tsmApiAccessId + ':' + base64.b64encode(digest)
    m_headers['Authorization'] = auth_header
    m_headers['Date'] = current_date
    return getattr(requests, method)(tsmApiUrl + request_path, data=m_data, headers=m_headers)