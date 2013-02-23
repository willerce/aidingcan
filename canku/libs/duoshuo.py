#-*- coding:UTF-8-*-
import base64
import hashlib
import hmac

import json
import time


def remote_auth(user_id, name, email, url=None, avatar=None):
    data = json.dumps({
        'key': user_id,
        'name': name,
        'email': email,
        'url': url,
        'avatar': avatar,
        })
    message = base64.b64encode(data)
    timestamp = int(time.time())
    sig = hmac.HMAC('9cf53efb81606983958d7e0fd9bc7925', '%s %s' % (message, timestamp), hashlib.sha1).hexdigest()
    duoshuo_query = '%s %s %s' % (message, sig, timestamp)
    return duoshuo_query