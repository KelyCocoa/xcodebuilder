"""
 Created by Geek on 2021/10/25 16:05.
"""
import requests
from app.config import config
import webbrowser

__author__ = 'Geek'


class FirUploader:

    def __init__(self, file_path):
        self.file_path = file_path

    def upload(self):
        """
        :return: 下载ipa包的链接
        """
        print('===========正在上传Fir.im===========')
        token_data = self.__get_upload_token()
        if token_data == None:
            raise Exception('获取上传凭证失败')
        binary = token_data.get('cert', {}).get('binary', {})
        upload_data = self.__upload_file(binary.get('key', ''), binary.get('token', ''), binary.get('upload_url', ''))
        if upload_data is None:
            raise Exception('上传文件失败')
        print('===========上传完成===========')
        self.open_browser()

    def __get_upload_token(self, retry_count=3):
        """发布应用获取上传凭证"""
        if retry_count == 0:
            return None
        url = 'http://api.bq04.com/apps'
        result = requests.post(url=url, data={'type': 'ios', 'bundle_id': config.BUNDLE_ID, 'api_token': config.FIR_API_TOKEN})
        if result.status_code != 201:
            retry_count -= 1
            return self.__get_upload_token(retry_count)
        return result.json()

    def __upload_file(self, key, token, upload_url, retry_count=3):
        """
        上传文件
        key	String	    是	七牛上传 key
        token	String	是	七牛上传 token
        upload_url      是   上传七牛云的URL
        """
        if retry_count == 0:
            return None
        data = {
            'key': key,
            'token': token,
            'x:name': config.APP_NAME,
            'x:version': config.APP_VERSION,
            'x:build': config.APP_BUILD,
            'x:release_type': config.APP_RELEASE_TYPE,
            'x:changelog': config.APP_CHANGE_LOG
        }
        files = {'file': open(self.file_path, 'rb')}  # 文件
        result = requests.post(url=upload_url, data=data, files=files)
        if result.status_code != 200:
            retry_count -= 1
            return self.__upload_file(key, token, upload_url, retry_count)
        return result.json()

    def open_browser(self):
        webbrowser.open('https://www.betaqr.com/apps/{app_id}'.format(app_id=config.FIR_APP_ID), new=1, autoraise=True)
