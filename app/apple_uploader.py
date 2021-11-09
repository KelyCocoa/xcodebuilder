"""
 Created by Geek on 2021/10/25 16:06.
"""
from app.config import config
import subprocess
import time
import webbrowser

__author__ = 'Geek'


class AppleUploader:
    def __init__(self, file_path):
        self.file_path = file_path

    def upload(self):
        self.__validate()
        self.__upload()
        self.__open_browser()

    def __validate(self, retry_count=3):
        """验证"""
        print('===========正在验证ipa包===========')
        if retry_count == 0:
            return
        start = time.time()
        validate_opt = 'xcrun altool --validate-app -f {file_path}' \
                       ' -t iOS -u {username} -p {password}'.format(
            file_path=self.file_path,
            username=config.APP_STORE_CONNECT_USER_NAME,
            password=config.APP_STORE_CONNECT_SPECIAL_PASSWORD)
        validate_opt_run = subprocess.Popen(validate_opt, shell=True)
        validate_opt_run.wait()
        end = time.time()
        validate_result_code = validate_opt_run.returncode
        if validate_result_code != 0:
            print("===========验证 ipa 失败,用时:%.2f秒===========" % (end - start))
            retry_count -= 1
            self.__validate(retry_count)
        else:
            print("===========验证 ipa 成功,用时:%.2f秒===========" % (end - start))

    def __upload(self, retry_count=3):
        """上传"""
        if retry_count == 0:
            return
        print('===========正在上传ipa包===========')
        start = time.time()
        upload_opt = 'xcrun altool --upload-app -f {file_path} ' \
                     '-u {username} -p {password}'.format(
            file_path=self.file_path,
            username=config.APP_STORE_CONNECT_USER_NAME,
            password=config.APP_STORE_CONNECT_SPECIAL_PASSWORD)
        upload_opt_run = subprocess.Popen(upload_opt, shell=True)
        upload_opt_run.wait()
        end = time.time()
        upload_result_code = upload_opt_run.returncode
        if upload_result_code != 0:
            print("===========上传 ipa 失败,用时:%.2f秒===========" % (end - start))
            retry_count -= 1
            self.__upload(retry_count)
        else:
            print("===========上传 ipa 成功,用时:%.2f秒===========" % (end - start))

    def __open_browser(self):
         webbrowser.open('https://appstoreconnect.apple.com/apps', new=1, autoraise=True)
