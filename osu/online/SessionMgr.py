import time
import logging
import requests
import json

from bs4 import BeautifulSoup

from osu.online.login import username, password



class SessionMgr():

    _logger           = None
    _init             = False
    _session          = None
    _last_status_code = None
    _logged_in        = False

    @staticmethod
    def init():
        SessionMgr._logger  = logging.getLogger(__class__.__name__)
        SessionMgr._session = requests.session()
        SessionMgr._init = True


    @staticmethod
    def close():
        if not SessionMgr._init: 
            SessionMgr._logger.warn('Session Manager already shut down')
            return

        SessionMgr._session   = None
        SessionMgr._logged_in = False
        SessionMgr._init      = False

    
    @staticmethod
    def login():
        if SessionMgr._logged_in: return

        # While being told there are too many login requests, attempt to log in
        while True:
            # For some reason web now needs a token for login
            response = SessionMgr.fetch_web_data('https://osu.ppy.sh')
            SessionMgr.validate_response(response)

            root = BeautifulSoup(response.text, "lxml")
            token = root.find('input', {'name' : '_token'})['value']

            login_data = { '_token' : token, 'username': username, 'password' : password }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
                'Referer' : 'https://osu.ppy.sh/home'
            }

            try: response = SessionMgr._session.post('https://osu.ppy.sh/session', data=login_data, headers=headers)
            except Exception:
                raise Exception('Unable to log in')

            SessionMgr.validate_response(response)
            
            if response.status_code != 200:            
                if response.status_code == 429: 
                    SessionMgr._logger.warning('Too many login requests; Taking a 5 min nap . . . ')
                    time.sleep(5*60)  # Too many requests; Take 5 min nap
                    continue
                else:
                    raise Exception('Unable to log in; Status code: ' + str(response.status_code))
            
            break

        # Validate log in
        response = SessionMgr.fetch_web_data('https://osu.ppy.sh')
        if not 'XSRF-TOKEN' in response.cookies:
            SessionMgr._logger.warning('Cookies indicate login failed; Going to try again in one hour . . . ')
            time.sleep(60*60)  # Sleep for an hour
            raise Exception('Unable to log in; Cookies indicate login failed!')
        
        SessionMgr.check_account_verification(response)
        SessionMgr._logged_in = True


    @staticmethod
    def check_account_verification(response):
        check = False
        while True:
            if response.text.find("Account Verification") == -1: break
            if not check:
                print('Need response to verification email before continuing')
                check = True

            response = SessionMgr.fetch_web_data('https://osu.ppy.sh')
            time.sleep(5) # Check every minute until responded to email


    @staticmethod
    def is_logged_in():
        return SessionMgr._logged_in


    @staticmethod
    def fetch_web_data(url):
        try:
            response = SessionMgr._session.get(url, timeout=60*5)
            SessionMgr.validate_response(response)
        
            return response
        except requests.exceptions.Timeout as e:
            error_msg = 'Timed out while fetching url: ' + str(url) + '\n' + str(e)
            raise Exception(error_msg, show_traceback=False)
        except requests.exceptions.ConnectionError as e:
            error_msg = 'Unable to fetch url: ' + str(url) + '\n' + str(e)
            raise Exception(error_msg, show_traceback=False)
        except Exception as e:
            error_msg = 'Unable to fetch url: ' + str(url) + '\n' + str(e)
            raise Exception(error_msg)


    @staticmethod
    def get_last_status_code():
        return SessionMgr._last_status_code


    @staticmethod
    def validate_response(response):
        SessionMgr._last_status_code = response.status_code

        if response.status_code == 200: return 200  # Ok
        if response.status_code == 400: raise Exception('Error 400: Unable to process request')
        if response.status_code == 401: return 401  # Need to log in
        if response.status_code == 403: return 403  # Forbidden
        if response.status_code == 404: return 404  # Resource not found
        if response.status_code == 405: raise Exception('Error 405: Method not allowed')
        if response.status_code == 407: raise Exception('Error 407: Proxy authentication required')
        if response.status_code == 408: raise Exception('Error 408: Request timeout')
        if response.status_code == 429: return 429  # Too many requests
        if response.status_code == 500: raise Exception('Error 500: Internal server error')
        if response.status_code == 502: raise Exception('Error 502: Bad Gateway')
        if response.status_code == 503: raise Exception('Error 503: Service unavailable')
        if response.status_code == 504: raise Exception('Error 504: Gateway timeout')

SessionMgr.init()

