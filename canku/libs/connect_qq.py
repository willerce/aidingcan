# coding=utf-8
__author__ = 'Xulu(email:xulu@xulu.cc)'
__version__ = '0.1.0'

import json
import time
import urllib, urllib2, urlparse


def _obj_hook(pairs):
    o = JsonObject()
    for k, v in pairs.iteritems():
        o[str(k)] = v
    return o


class JsonObject(dict):
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value


def _encode_params(params):
    """
        将dict转换为url请求的参数形式:a=b&c=d
    """
    args = []
    for (k, v) in params.iteritems():
        qv = v.encode('utf-8') if isinstance(v, unicode) else str(v)
        args.append('%s=%s' % (k, urllib.quote(qv)))
    return '&'.join(args)

_HTTP_GET = 0
_HTTP_POST = 1
_HTTP_UPLOAD = 2

def _http_request(url, method, params, authorization):
    """
    执行http请求,目前两种格式,GET,POST
    """
    boundary = None
    args = _encode_params(params)

    http_url = '%s?%s' % (url, args) if method == _HTTP_GET else url
    http_params = None if method == _HTTP_GET else args

    req = urllib2.Request(http_url, http_params)

    if method == _HTTP_POST:
        req.add_header('POST %s HTTP/1.1')
    resp = urllib2.urlopen(req)
    body = str(resp.read())
    #body = body[9:-3]
    print body
    v_json = json.loads(body, object_hook=_obj_hook)
    if hasattr(v_json, 'error'):
        raise OpenQQError(v_json.error, v_json.error_description)

    if int(v_json['ret']) > 0:
        raise OpenQQError(v_json['ret'], v_json['msg'])

    return v_json


class OpenQQError(StandardError):
    def __init__(self, error, error_description):
        self.error = error
        self.error_description = error_description
        StandardError.__init__(self, error)

    def __str__(self):
        return 'OpenQQError: %s: %s' % (self.error, self.error_description)


class QQAPIClient(object):
    def __init__(self, client_id, client_secret, redirect_uri=None, response_type='code', scope='get_user_info',
                 domain='graph.qq.com', version='oauth2.0', display='default'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.domain = domain
        self.version = version
        self.response_type = response_type
        self.scope = scope
        self.display = display
        self.access_token = None
        self.openid = None
        self.expires = 0.0
        self.base_url = 'https://%s/' % domain
        # QQ空间 url
        self.user_api_url = 'https://%s/%s/' % (domain, 'user')
        # QQ微博 url
        self.t_api_url = 'https://%s/%s/' % (domain, 't')


    def set_access_token(self, access_token, expires_in):
        """
            设置access_token
        """
        self.access_token = access_token
        self.expires = expires_in


    def set_openid(self, openid):
        self.openid = openid


    def get_auth_url(self, redirect_uri=None):
        """
            获取登录的url,需要跳转至该url进行QQ登录
        """
        redirect = redirect_uri if redirect_uri else self.redirect_uri
        params = {'client_id': self.client_id,
                  'response_type': self.response_type,
                  'redirect_uri': redirect,
                  'scope': self.scope}
        return '%s%s/%s?%s' % (self.base_url, self.version, 'authorize', _encode_params(params))

    def request_access_token(self, code, redirect_uri=None):
        """
            获得access_token,(腾讯返回access_token,openid及普通api的返回,这3个居然格式不一致.不会全部都返回JSON啊,哎......)
        """
        redirect = redirect_uri if redirect_uri else self.redirect_uri

        #参数
        params = {'grant_type': 'authorization_code',
                  'client_id': self.client_id,
                  'client_secret': self.client_secret,
                  'code': code,
                  'redirect_uri': redirect,
                  'state': 'xulu'}
        url = '%s%s/%s?%s' % (self.base_url, self.version, 'token', _encode_params(params))
        resp = urllib2.urlopen(url)
        result = urlparse.parse_qs(resp.read(), True)
        access_token = str(result['access_token'][0])
        expires_in = float(int(result['expires_in'][0]) + int(time.time()))

        return {'access_token': access_token, 'expires_in': expires_in}

    def request_openid(self):
        """
            获得openid,(腾讯返回access_token,openid及普通api的返回,这3个居然格式不一致.不会全部都返回JSON啊,哎......)
        """
        params = {'access_token': self.access_token}
        url = '%s%s/%s?%s' % (self.base_url, self.version, 'me', _encode_params(params))
        resp = urllib2.urlopen(url)
        v_str = str(resp.read())
        v_str = v_str[9:-3]
        v_json = json.loads(v_str)
        openid = v_json['openid']

        return openid

    def is_expires(self):
        return not self.access_token or time.time() > self.expires

    def request_api(self, api, method=_HTTP_GET, params={'format': 'json'}):
        """
            普通api请求,需要传入api的调用名,如'user/get_user_info',以及在params指定返回格式{'format': 'json'}
            默认执行GET请求,只需要传入api就可以了.如执行POST请求 则需要传入method和相应的参数.
        """

        #以下为默认的必传的公共参数
        params.update({'access_token': self.access_token,
                       'oauth_consumer_key': self.client_id,
                       'openid': self.openid})
        print '%s%s' % (self.base_url, api)
        if self.is_expires():
            raise OpenQQError('21327', 'expired_token')
        return _http_request('%s%s' % (self.base_url, api), method, params, self.access_token)


