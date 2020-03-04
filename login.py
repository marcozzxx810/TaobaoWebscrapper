import re
import os
import json

import requests



s = requests.Session()

COOKIES_FILE_PATH = 'taobao_login_cookies.txt'


class TaoBaoLogin:

    def __init__(self, session):
        """
        Login system
        :param username: 
        :param ua: user-agent 
        :param TPL_password2: 
        """
       
        self.user_check_url = 'https://login.taobao.com/member/request_nick_check.do?_input_charset=utf-8'
        
        self.verify_password_url = "https://login.taobao.com/member/login.jhtml"
        
        self.vst_url = 'https://login.taobao.com/member/vst.htm?st={}'
       
        self.my_taobao_url = 'http://i.taobao.com/my_taobao.htm'

       
        self.username = 'marcozzxx810'
        
        self.ua = '122#HBm+8D+kEE+BKEpZMEpJEJponDJE7SNEEP7rEJ+/f9t/2oQLpo7iEDpWnDEeK51HpyGZp9hBuDEEJFOPpC76EJponDJL7gNpEPXZpJRgu4Ep+FQLpoGUEJLWn4yP7SQEEyuLpEROsIRcprZCnaRx9kb/Ff+ycfhutz7TwnkTTTDO0KQhRlNbLjqlRr0YSUy4UWSdtvJJg/LeEvj447uScpUs2Hc6rvM69WHa1tgcXxLcbY5DwI7Qt7vqhGAdlTpPOl/++VK4q4faw5EpsmADqMfpTanHhgx51ynEELXAOkTWrzsqHovD7W3bEEpxngR4eN/Yi+mr8Cp6+DPEyFfOefMOwzVanSbWuO5EELGA8oL6JNEEyBfDqMfbDEpCnSL1ul0EDLVr8CpUJzbEyF3mqW32E5pamMp1uOZWELXr8ytKaPYEmtWqhWbUmEMmp3WWJcffjCaji8b+VSykV5MgIfUEinNKrcI23GLJ6/lGWFkdYfz8M/jpBMJ7QQ7Q96AnkDmGshjmh6NKQSIWt2w1Tin2DPpqUZERxZBntx9k1LaAgNNqYoOi9C3JHuVsZXIqW0jKXvpdy9kqnT1rHqmjbgciMgi45zcHWOGlMbsLoUcQ1uFQIzvXWCYiJg42P6WiCpDmhMr48xB2gaC/hdxl0+RhPv8j6lh2P/xNVvq9gsTS1HCxuo7T2NyFGHblN26MfNukcmd1GHJ8inhVgSCr/vrXtDLSSv/r1NzFWFKqcFcnnxPlNHadfkiGsRu9gNEK35oLJJ/GsiAP7rDlYzrv6XHo24K0EPA0SUxLA8HPxqqOn0JBU9jMN3H3bDAs2+TN+tOFCmKbO8mvzW9Xw5D8LPOzyvpOh44QBqIOpaoXH1kp/VgBJLJt5Btalgxg6JYdh3r8PCRi7nxCEaNryn487BjaM0nuHPIfeVxnyGgyQsxvbupa4M28qyFV5MN5YZb9K9QWHLDFp5b0ZjIjLLN3CyxpL9QemezjPpNluM4U2/wPF5B7YS9vTigFphChCb1PiLAkb8QhXRxWcfnKwXjPJM8QZQFs3TYdvGaA6pLvpduoGZ4Byz8DjGfmVtsyHE8WTIlW3dtwPonjV5OYUPL8ZclqGstaO1xUWwyfEdRi0propLIl6Imrp4qKD0j9tO9wzfeOCx7m4NAVgkIRhwmg0inQMByWG4IVXLrehSYO/lkpUlE7itS866O5cOgRcyYRANKFnUdqpBCF3CTZZNZLENojF25JvKga95AQwE/Qvd8Z4C01rzoW84P+zLoz5rk76kdI1rDmB6MbOjYhHgNP7BTo29aFiIeib+j8zbRTfV43Km0ghNf4bZ9mXdVc8NO/wdIxcle+r2KCCKPanEUwZcFDMeaWTbm25jyqHRjXiCInolzJyIpTVG05JORQ4vXVr3toejil7o0yNQjIS3NilN5mfOfIHRrsetBc/0r2cSy1LcSNBA0UnaJOZWzssNSi8rISjwvZdZ3Wp5auipkJHTLGjKtGgwjfPLc1u3pC8J=='
        
        self.TPL_password2 = '10bdfbfd4184bb8bf4f542262bb8cf18ea71fc39b9f10e0068f51f66758c1fc449e0e9ad4cb2ec3436f4d6d2c1b57c424fe126948a15608b1784d676a9a85c772d934dfcfc55b13306a05c54b1fbf61ed02e737123cd5a7ab91de00a69a11aa10ab8aa86c32138d9affe1399891367f90d58896d9423748072528a03ca59e80c'

       
        self.timeout = 3
        
        self.session = session

        if not self.username:
            raise RuntimeError('请填写你的淘宝用户名')

    def _user_check(self):
        """
        detect validation is needed or not
        :return:
        """
        data = {
            'username': self.username,
            'ua': self.ua
        }
        try:
            response = self.session.post(self.user_check_url, data=data, timeout=self.timeout)
            response.raise_for_status()
        except Exception as e:
            print('检测是否需要验证码请求失败，原因：')
            raise e
        needcode = response.json()['needcode']
        print('是否需要滑块验证：{}'.format(needcode))
        return needcode

    def _verify_password(self):
        """
        verify password
        :return: st passcode webiste
        """
        verify_password_headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': 'https://login.taobao.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://login.taobao.com/member/login.jhtml?from=taobaoindex&f=top&style=&sub=true&redirect_url=https%3A%2F%2Fi.taobao.com%2Fmy_taobao.htm',
        }
        
        verify_password_data = {
            'TPL_username': self.username,
            'ncoToken': '78401cd0eb1602fc1bbf9b423a57e91953e735a5',
            'slideCodeShow': 'false',
            'useMobile': 'false',
            'lang': 'zh_CN',
            'loginsite': 0,
            'newlogin': 0,
            'TPL_redirect_url': 'https://s.taobao.com/search?q=%E9%80%9F%E5%BA%A6%E9%80%9F%E5%BA%A6&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306',
            'from': 'tb',
            'fc': 'default',
            'style': 'default',
            'keyLogin': 'false',
            'qrLogin': 'true',
            'newMini': 'false',
            'newMini2': 'false',
            'loginType': '3',
            'gvfdcname': '10',
            # 'gvfdcre': '68747470733A2F2F6C6F67696E2E74616F62616F2E636F6D2F6D656D6265722F6C6F676F75742E6A68746D6C3F73706D3D61323330722E312E3735343839343433372E372E33353836363032633279704A767526663D746F70266F75743D7472756526726564697265637455524C3D6874747073253341253246253246732E74616F62616F2E636F6D25324673656172636825334671253344253235453925323538302532353946253235453525323542412532354136253235453925323538302532353946253235453525323542412532354136253236696D6766696C65253344253236636F6D6D656E64253344616C6C2532367373696425334473352D652532367365617263685F747970652533446974656D253236736F75726365496425334474622E696E64657825323673706D253344613231626F2E323031372E3230313835362D74616F62616F2D6974656D2E31253236696525334475746638253236696E69746961746976655F69642533447462696E6465787A5F3230313730333036',
            'TPL_password_2': self.TPL_password2,
            'loginASR': '1',
            'loginASRSuc': '1',
            'oslanguage': 'zh-CN',
            'sr': '1440*900',
            'osVer': 'macos|10.145',
            'naviVer': 'chrome|76.038091',
            'osACN': 'Mozilla',
            'osAV': '5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'osPF': 'MacIntel',
            'appkey': '00000000',
            'mobileLoginLink': 'https://login.taobao.com/member/login.jhtml?redirectURL=https://s.taobao.com/search?q=%E9%80%9F%E5%BA%A6%E9%80%9F%E5%BA%A6&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&useMobile=true',
            'showAssistantLink': '',
            'um_token': 'TD0789BC99BFBBF893B3C8C0E1729CCA3CB0469EA11FF6D196BA826C8EB',
            'ua': self.ua
        }
        try:
            response = self.session.post(self.verify_password_url, headers=verify_password_headers, data=verify_password_data,
                              timeout=self.timeout)
            response.raise_for_status()
            
        except Exception as e:
            print('验证用户名和密码请求失败，原因：')
            raise e
        
        apply_st_url_match = re.search(r'<script src="(.*?)"></script>', response.text)
        
        if apply_st_url_match:
            print('验证用户名密码成功，st码申请地址：{}'.format(apply_st_url_match.group(1)))
            return apply_st_url_match.group(1)
        else:
            raise RuntimeError('用户名密码验证失败！response：{}'.format(response.text))

    def _apply_st(self):
        """
        register st code
        :return: st code
        """
        apply_st_url = self._verify_password()
        try:
            response = self.session.get(apply_st_url)
            response.raise_for_status()
        except Exception as e:
            print('申请st码请求失败，原因：')
            raise e
        st_match = re.search(r'"data":{"st":"(.*?)"}', response.text)
        if st_match:
            print('获取st码成功，st码：{}'.format(st_match.group(1)))
            return st_match.group(1)
        else:
            raise RuntimeError('获取st码失败！response：{}'.format(response.text))

    def login(self):
        """
        use st code to login
        :return:
        """
        # 加载cookies文件
        if self._load_cookies():
            return True
        
        self._user_check()
        st = self._apply_st()
        headers = {
            'Host': 'login.taobao.com',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        try:
            response = self.session.get(self.vst_url.format(st), headers=headers)
            response.raise_for_status()
        except Exception as e:
            print('st码登录请求，原因：')
            raise e
       
        my_taobao_match = re.search(r'top.location.href = "(.*?)"', response.text)
        if my_taobao_match:
            print('登录淘宝成功，跳转链接：{}'.format(my_taobao_match.group(1)))
            self._serialization_cookies()
            return True
        else:
            raise RuntimeError('登录失败！response：{}'.format(response.text))

    def _load_cookies(self):
       
        if not os.path.exists(COOKIES_FILE_PATH):
            return False
       
        self.session.cookies = self._deserialization_cookies()
        
        try:
            self.get_taobao_nick_name()
        except Exception as e:
            os.remove(COOKIES_FILE_PATH)
            print('cookies过期，删除cookies文件！')
            return False
        print('加载淘宝登录cookies成功!!!')
        return True

    def _serialization_cookies(self):
        """
        serialize cookies
        :return:
        """
        cookies_dict = requests.utils.dict_from_cookiejar(self.session.cookies)
        with open(COOKIES_FILE_PATH, 'w+', encoding='utf-8') as file:
            json.dump(cookies_dict, file)
            print('保存cookies文件成功！')

    def _deserialization_cookies(self):
        """
        deserialize cookies
        :return:
        """
        with open(COOKIES_FILE_PATH, 'r+', encoding='utf-8') as file:
            cookies_dict = json.load(file)
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
            return cookies

    def get_taobao_nick_name(self):
        """
        get taobao nice name
        :return: taobao nicename
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        try:
            response = self.session.get(self.my_taobao_url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            print('获取淘宝主页请求失败！原因：')
            raise e
        
        nick_name_match = re.search(r'<input id="mtb-nickname" type="hidden" value="(.*?)"/>', response.text)
        if nick_name_match:
            print('登录淘宝成功，你的用户名是：{}'.format(nick_name_match.group(1)))
            return nick_name_match.group(1)
        else:
            raise RuntimeError('获取淘宝昵称失败！response：{}'.format(response.text))


if __name__ == '__main__':
    ul = TaoBaoLogin(s)
    ul.login()
    ul.get_taobao_nick_name()