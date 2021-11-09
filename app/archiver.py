"""
 Created by Geek on 2021/10/25 16:02.
"""
import os
import time
import subprocess
from .config import config

__author__ = 'Geek'


class Archiver:

    def __init__(self):
        self.archive_file_path = None
        self.export_dir_path = None
        self.export_file_path = None

    def clean(self):
        print("\n\n===========clean...===========")
        start = time.time()
        clean_opt = 'xcodebuild clean -workspace {project_path}/{project_name}.xcworkspace ' \
                    '-scheme {scheme_name} -configuration {compiling_mode}'.format(
            project_path=config.PROJECT_PATH, project_name=config.PROJECT_NAME,
            scheme_name=config.SCHEME, compiling_mode=config.COMPILING_MODE)
        clean_opt_run = subprocess.Popen(clean_opt, shell=True)
        clean_opt_run.wait()
        end = time.time()
        # clean 结果
        clean_result_code = clean_opt_run.returncode
        if clean_result_code != 0:
            print("===========clean失败,用时:%.2f秒===========" % (end - start))
            raise Exception('clean failure')
        else:
            print("===========clean成功,用时:%.2f秒===========" % (end - start))
        return self

    def archive(self):
        print("\n\n===========开始archive操作===========")

        subprocess.call(['rm', '-rf', '{archive_path}/{archive_folder}'.format(
            archive_path=os.getcwd(), archive_folder=config.ARCHIVE_FOLDER)])
        time.sleep(1)
        subprocess.call(['mkdir', '-p', '{archive_path}/{archive_folder}'.format(
            archive_path=os.getcwd(), archive_folder=config.ARCHIVE_FOLDER)])
        time.sleep(1)

        start = time.time()
        workspace_path = '{project_path}/{project_name}.xcworkspace'.format(
            project_path=config.PROJECT_PATH, project_name=config.PROJECT_NAME)
        archive_path = '{archive_path}/{archive_folder}/{archive_file_name}'.format(
            archive_path=os.getcwd(), archive_folder=config.ARCHIVE_FOLDER, archive_file_name=config.SCHEME+time.strftime('%Y-%m-%d_%H.%M.%S'))
        archive_opt = 'xcodebuild archive -workspace {workspace_path}' \
                      ' -scheme {scheme_name} -configuration {compiling_mode} ' \
                      '-archivePath {archive_path}'.format(
            workspace_path=workspace_path, scheme_name=config.SCHEME, compiling_mode=config.COMPILING_MODE, archive_path=archive_path)
        archive_opt_run = subprocess.Popen(archive_opt, shell=True)
        archive_opt_run.wait()
        end = time.time()

        # archive 结果
        archive_result_code = archive_opt_run.returncode
        if archive_result_code != 0:
            print("===========archive失败,用时:%.2f秒===========" % (end - start))
            raise Exception('archive failure')
        else:
            print("===========archive成功,用时:%.2f秒===========" % (end - start))
        self.archive_file_path = archive_path + '.xcarchive'
        return self

    def export(self, profile='dev'):
        """导出IPA
            profile: dev
                     prod
        """

        print("\n\n===========开始export操作===========")
        export_dir_path = os.getcwd() + '/' + config.EXPORT_FOLDER
        subprocess.call(['rm', '-rf', export_dir_path])
        time.sleep(1)
        subprocess.call(['mkdir', '-p', export_dir_path])
        time.sleep(1)

        start = time.time()
        export_opt = 'xcodebuild -exportArchive -archivePath {archive_path} -exportPath {export_dir_path}' \
                     ' -exportOptionsPlist {plist_path}'.format(
            archive_path=self.archive_file_path, export_dir_path=export_dir_path,
            plist_path=os.getcwd()+'/app/config/ExportOptions_'+profile+'.plist')
        print(export_opt)
        export_opt_run = subprocess.Popen(export_opt, shell=True)
        export_opt_run.wait()
        end = time.time()

        # ipa导出结果
        export_result_code = export_opt_run.returncode
        if export_result_code != 0:
            print("===========导出IPA失败,用时:%.2f秒===========" % (end - start))
            raise Exception('export failure')
        else:
            print("===========导出IPA成功,用时:%.2f秒===========" % (end - start))
        self.export_dir_path = export_dir_path
        self.export_file_path = export_dir_path + '/' + config.EXPORT_IPA_NAME + '.ipa'
        return self.export_file_path
