import time
import requests


class SessionMgr(requests.Session):

    def __init__(self):
        requests.Session.__init__(self)

        self._logged_in        = False
        self._last_status_code = None

        self.xsrf_token  = None
        self.osu_session = None


    def login(self, username, password):
        if self._logged_in: return

        # While being told there are too many login requests, attempt to log in
        while True:
            try:
                login_data = { 'username': username, 'password' : password }
                response = self.post('https://osu.ppy.sh/session', data=login_data) 
            except Exception as e:
                raise Exception('Unable to log in')

            self.validate_response(response)
            
            if response.status_code != 200:            
                if response.status_code == 429: 
                    raise Exception('Unable to log in; Too many requests')
                else:
                    raise Exception('Unable to log in; Status code: ' + str(response.status_code))
            
            break

        # Validate log in
        response = self.fetch_web_data('https://osu.ppy.sh')
        if not 'XSRF-TOKEN' in response.cookies:
            raise Exception('Unable to log in; Cookies indicate login failed!')

        self.xsrf_token  = response.cookies['XSRF-TOKEN']
        self.osu_session = response.cookies['osu_session']

        self._logged_in = True


    def fetch_web_data(self, url):
        try:
            response = self.get(url, timeout=60*5)
            self.validate_response(response)
        
            return response
        except requests.exceptions.Timeout as e:
            error_msg = 'Timed out while fetching url: ' + str(url) + '\n' + str(e)
            raise Exception(error_msg)
        except requests.exceptions.ConnectionError as e:
            error_msg = 'Unable to fetch url: ' + str(url) + '\n' + str(e)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = 'Unable to fetch url: ' + str(url) + '\n' + str(e)
            raise Exception(error_msg)


    def get_xsrf_token(self):
        return self.xsrf_token


    def get_osu_session(self):
        return self.osu_session


    def get_last_status_code(self):
        return self._last_status_code


    def validate_response(self, response):
        self._last_status_code = response.status_code

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


