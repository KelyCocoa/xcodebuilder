"""
 Created by Geek on 2021/10/25 15:45.
"""
import getopt
import sys

from app.archiver import Archiver
from app.config import config
from app.fir_downloader import FirDownloader
from app.fir_uploader import FirUploader
from app.apple_uploader import AppleUploader

__author__ = 'Geek'


def print_help_info():
    print('\n\n********oprations********')
    print('--deploy=dev或者prod或者prod&dev: dev:上传fir.im，prod:上传苹果开发者中心 prod&dev同时上传fir和appstore')
    print('\n\n********app配置********')
    print('--bundle_id=xx: 配置bundle_id')
    print('--project_path=xx: 项目所在的目录路径')
    print('--project_name=xx: 项目名称，不包括后缀')
    print('--scheme=xx: 配置scheme名称')
    print('--compiling_mode=Release或者Debug: 配置编译模式')
    print('\n\n********打包配置********')
    print('--archive_folder=xx: 打包的.xcarchive文件所在的文件夹名，默认organizer')
    print('--export_ipa_name=xx: 导出的IPA文件名(APP显示在桌面上的名字)')
    print('--export_folder=xx: 打包文件的输出文件夹名，默认dist')
    print('\n\n********fir.im上传配置********')
    print('--fir_api_token=xx: 上传fir的token')
    print('--app_name=xx: app名称')
    print('--app_version=xx: 版本号')
    print('--app_build=xx: 构建版本号')
    print('--app_release_type=xx: 打包类型，只针对 iOS (Adhoc, Inhouse)')
    print('--app_change_log=xx: 版本更新日志')


def reset_config(opt_name, opt_value):
    if opt_name == '--bundle_id' and opt_value is not None and len(opt_value) > 0:
        config.BUNDLE_ID = opt_value
    elif opt_name == '--project_path' and opt_value is not None and len(opt_value) > 0:
        config.PROJECT_PATH = opt_value
    elif opt_name == '--project_name' and opt_value is not None and len(opt_value) > 0:
        config.PROJECT_NAME = opt_value
    elif opt_name == '--scheme' and opt_value is not None and len(opt_value) > 0:
        config.SCHEME = opt_value
    elif opt_name == '--compiling_mode' and opt_value is not None and len(opt_value) > 0:
        config.COMPILING_MODE = opt_value
    elif opt_name == '--archive_folder' and opt_value is not None and len(opt_value) > 0:
        config.ARCHIVE_FOLDER = opt_value
    elif opt_name == '--export_ipa_name' and opt_value is not None and len(opt_value) > 0:
        config.EXPORT_IPA_NAME = opt_value
    elif opt_name == '--export_folder' and opt_value is not None and len(opt_value) > 0:
        config.EXPORT_FOLDER = opt_value
    elif opt_name == '--fir_api_token' and opt_value is not None and len(opt_value) > 0:
        config.FIR_API_TOKEN = opt_value
    elif opt_name == '--app_name' and opt_value is not None and len(opt_value) > 0:
        config.APP_NAME = opt_value
    elif opt_name == '--app_version' and opt_value is not None and len(opt_value) > 0:
        config.APP_VERSION = opt_value
    elif opt_name == '--app_build' and opt_value is not None and len(opt_value) > 0:
        config.APP_BUILD = opt_value
    elif opt_name == '--app_release_type' and opt_value is not None and len(opt_value) > 0:
        config.APP_RELEASE_TYPE = opt_value
    elif opt_name == '--app_change_log' and opt_value is not None and len(opt_value) > 0:
        config.APP_CHANGE_LOG = opt_value


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], 'h', ['help', 'export=', 'deploy=', 'bundle_id=', 'project_path=', 'project_name=', 'scheme=',
                                                   'compiling_mode=', 'archive_folder=', 'export_ipa_name=',
                                                   'export_folder=', 'fir_api_token=', 'app_name=', 'app_version=',
                                                   'app_build=', 'app_release_type=', 'app_change_log='])
    for opt_name, opt_value in opts:
        if opt_name in ('-h', '--help'):
            print_help_info()
            exit()
        reset_config(opt_name, opt_value)
    for opt_name, opt_value in opts:
        archiver = Archiver()
        if opt_name == '--deploy':
            if opt_value is not None and opt_value == 'prod':
                file_path = archiver.clean().archive().export(profile='prod')
                AppleUploader(file_path).upload()
            elif opt_value is not None and opt_value in ('prod&dev', 'dev&prod'):
                dev_file_path = archiver.clean().archive().export(profile='dev')
                FirUploader(dev_file_path).upload()
                FirDownloader().download()
                prod_file_path = archiver.clean().archive().export(profile='prod')
                AppleUploader(prod_file_path).upload()
            else:
                file_path = archiver.clean().archive().export(profile='dev')
                FirUploader(file_path).upload()
                FirDownloader().download()
