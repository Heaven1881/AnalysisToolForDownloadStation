# encoding:utf8
import requests


class DownloadStationAPI:

    def __init__(self, ip, port=5000):
        self.ip = ip
        self.port = port
        self.sid = None

    def login(self, account, passwd):
        if self.sid:
            return self.sid

        try:
            result = requests.get(
                'http://%s:%d/webapi/auth.cgi' % (self.ip, self.port),
                params={
                    'api': 'SYNO.API.Auth',
                    'version': 2,
                    'method': 'login',
                    'account': account,
                    'passwd': passwd,
                    'session': 'DownloadStation',
                    'format': 'sid'
                }
            ).json()

            if result['success']:
                self.sid = result['data']['sid']
                print '[DS] login! sid: %s' % self.sid

        except Exception as e:
            print e.message
        finally:
            return self.sid

    def logout(self):
        if not self.sid:
            return True

        try:
            result = requests.get(
                'http://%s:%d/webapi/auth.cgi' % (self.ip, self.port),
                params={
                    'api': 'SYNO.API.Auth',
                    'version': 1,
                    'method': 'logout',
                    'session': 'DownloadStation',
                    'sid': self.sid
                }
            ).json()

            if result['success']:
                print '[DS] logout!'
                self.sid = None

        except Exception as e:
            print e.message
        finally:
            self.sid = None
            return True

    def get_download_task(self):
        try:
            result = requests.get(
                'http://%s:%d/webapi/DownloadStation/task.cgi' % (self.ip, self.port),
                params={
                    'api': 'SYNO.DownloadStation.Task',
                    'version': 1,
                    'method': 'list',
                    'additional': 'detail,transfer',
                    '_sid': self.sid
                }
            ).json()

            if result['success']:
                return result['data']['tasks']
            else:
                print '[DS] get download task failed', result

        except Exception as e:
            print e.message
        return []
