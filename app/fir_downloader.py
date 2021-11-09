"""
 Created by Geek on 2021/10/28 11:09.
"""
import requests
import time
import qrcode
from urllib.parse import quote
from app.config import config

__author__ = 'Geek'


class FirDownloader:
    def __init__(self):
        pass

    def download(self):
        print('===========正在获取download_token===========')
        download_token = self.__get_download_token()
        if download_token is None:
            raise Exception('获取download_token失败')
        print('===========生成二维码===========')
        install_url = self.__get_install_url(download_token)
        img = qrcode.make(install_url)
        img_name = '{app_name}-{date_time}.png'.format(app_name=config.APP_NAME,
                                                       date_time=time.strftime('%Y-%m-%d_%H.%M.%S'))
        with open(img_name, 'wb') as f:
            img.save(f)
        print('===========install success===========')
        return install_url

    def __get_download_token(self, retry_count=3):
        if retry_count == 0:
            return None
        url = 'http://api.bq04.com/apps/{app_id}/download_token?api_token={api_token}'.format(
            app_id=config.FIR_APP_ID, api_token=config.FIR_API_TOKEN)
        result = requests.get(url)
        if result.status_code != 200:
            retry_count -= 1
            return self.__get_download_token(retry_count)
        return result.json().get('download_token')

    def __get_install_url(self, download_token):
        url = 'https://download.bq04.com/apps/{app_id}/install?download_token={download_token}'.format(
            app_id=config.FIR_APP_ID, download_token=download_token)
        return 'itms-services://?action=download-manifest&url={url}'.format(
            url=quote(url))


