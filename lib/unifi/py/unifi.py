import requests
import logging
import time
import json
import random
import string

class UniFi(object):
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = 8443
        self.site_id = "default"
        self.url = "https://" + self.hostname + ":" + str(self.port) + "/"
        self.verify_ssl = False

    def login(self):
        logging.info("Logging in to " + self.hostname)
        attempts = 0
        while attempts < 25:
            attempts += 1
            url = self.url + "api/login"
            self.s = requests.Session()
            params = {'username': self.username, 'password': self.password}
            params = json.dumps(params)
            # Login
            r = self.s.post(url=url, data=params, verify=self.verify_ssl, timeout=30)
            logging.debug(r.text)
            logging.debug(r.status_code)
            if r.text != '{"meta":{"rc":"ok"},"data":[]}':
                logging.info("Login failed, trying again")
                time.sleep(1)
            else:
                logging.info('Logged in successfully')
                break

    def _set_wizard_default_admin(self, email):
        time_check = 0
        while time_check < 120:
            try:
                url = self.url + 'api/cmd/sitemgr'
                payload = {'cmd': 'add-default-admin', 'email': email, 'name': self.username,
                'x_password': self.password}
                r = requests.post(url, data=json.dumps(payload), verify=self.verify_ssl)
                if r.status_code == 200:
                    logging.info("Successfully set default admin")
                    logging.debug(r.text)
                    break
                else:
                    logging.info("Failed to set default admin")
                    logging.debug(r.text)
                    time.sleep(1)
                    time_check += 1
            except Exception as e:
                time_check += 1
                logging.info("Failed to set default admin")
                logging.debug(e)
                time.sleep(1)

    def _set_wizard_country(self):
        time_check = 0
        while time_check < 120:
            try:
                url = self.url + 'api/set/setting/country'
                payload = {'code': '840'}
                r = requests.post(url, data=json.dumps(payload), verify=self.verify_ssl)
                if r.status_code == 200:
                    logging.info("Successfully set default country")
                    logging.debug(r.text)
                    break
                else:
                    logging.info("Failed to set country")
                    time_check +=1
                    time.sleep(1)
            except Exception as e:
                logging.info("Failed to set country")
                logging.debug(e)
                time_check += 1
                time.sleep(1)

    def _check_if_running(self):
        logging.info("Checking if UniFi is running")
        unifi_status = 0
        time_check = 0
        while time_check < 120:
            try:
                url = self.url + "status"
                logging.info(url)
                r = requests.get(url, verify=self.verify_ssl)
                logging.info(r.text)
                logging.info(r.status_code)
                if r.status_code == 200:
                    if '"up":true' not in r.text:
                        logging.debug(r.text)
                        logging.debug(r.status_code)
                        unifi_status = 1
                        break
                    else:
                        logging.info("UniFi is running")
                        break
                else:
                    logging.info("waiting")
                    time_check += 1
                    time.sleep(1)
            except:
                logging.info("Failed to load")
                time.sleep(1)
        if unifi_status == 1:
            logging.info("UniFi installed successfully")
        else:
            logging.info("UniFi install failed")

    def _set_wizard_installed(self):
        time_check = 0
        while time_check < 120:
            time_check += 1
            try:
                url = self.url + 'api/cmd/system'
                payload = {'cmd': "set-installed"}
                r = requests.post(url, data=json.dumps(payload), verify=self.verify_ssl)
                if r.status_code == 200:
                    logging.info("Successfully set UniFi installed")
                    logging.debug(r.text)
                    break
                else:
                    logging.info("Failed to load set installed")
                    time.sleep(1)
                    time_check +=1
            except:
                logging.info("Failed to load set installed")
                time.sleep(1)
                time_check +=1
                
    def _set_wizard_locale(self):
        logging.info('Setting UniFi Wizard Locale')
        time_check = 0
        while time_check < 120:
            try:
                url = self.url + 'api/set/setting/locale'
                payload = {'timezone': 'America/New_York'}
                r = requests.post(url, data=json.dumps(payload), verify=self.verify_ssl)
                if r.status_code == 200:
                    logging.info("Successfully set locale")
                    logging.debug(r.text)
                    break
                else:
                    logging.info("Failed to load locale")
                    time.sleep(1)
                    time_check += 1
            except Exception as e:
                logging.info("Failed to load locale")
                logging.debug(e)
                time_check += 1
                time.sleep(1)

    def _set_wizard_device_ssh_creds(self):
        time_check = 0
        while time_check < 120:
            time_check += 1
            try:
                url = self.url + 'api/set/setting/mgmt'
                payload = {'x_ssh_username': self.username, 'x_ssh_password': ''.join(random.choice(string.ascii_letters) for i in range(8))}
                r = requests.post(url, data=json.dumps(payload), verify=self.verify_ssl)
                if r.status_code == 200:
                    logging.info("Successfully set device SSH creds")
                    logging.debug(r.text)
                    break
                else:
                    logging.debug(r.text)
                    logging.debug(r.status_code)
                    logging.info("Failed to load device ssh creds")
                    time.sleep(1)
                    time_check += 1
            except Exception as e:
                logging.debug(e)
                logging.info("Failed to load device ssh creds")
                time.sleep(1)
                time_check += 1     

    def _set_wizard_autobackups(self):
        logging.info("Setting wizard autobackup settings")
        time_check = 0
        while time_check < 120:
            time_check += 1
            try:
                url = self.url + 'api/set/setting/super_mgmt'
                payload = {"autobackup_enabled": 'true', "autobackup_cron_expr": "0 2 * * *", "autobackup_timezone": "America/New_York",
                "autobackup_days": '0'}
                r = requests.post(url, data=json.dumps(payload), verify=self.verify_ssl)
                if r.status_code == 200:
                    logging.info("Successfully set auto backups")
                    logging.debug(r.text)
                    break
                else:
                    logging.info("Failed to load auto backups")
                    time.sleep(1)
                    time_check += 1
            except:
                logging.info("Failed to load auto backups")
                time_check += 1
                time.sleep(1)

    def complete_unifi_wizard(self, email):
        logging.info('Killing the wizard')
        self._check_if_running()
        self._set_wizard_default_admin(email)
        self._set_wizard_country()
        self._set_wizard_locale()
        self._set_wizard_autobackups()
        self._set_wizard_device_ssh_creds()
        self._set_wizard_installed()
        logging.info('We killed the wizard!')

    def download_backup(self, storage_path, link):
        logging.info("Downloading backup")
        r = self.s.get(url=link, verify=self.verify_ssl, timeout=120)
        open(storage_path, 'wb').write(r.content)

    def create_manual_backup(self):
        logging.info("Creating settings only manual backup")
        params = {"cmd": "backup", "days": 0}
        params = json.dumps(params)
        url = self.url + "api/s/default/cmd/backup"
        r = self.s.post(url=url, data=params, verify=self.verify_ssl, timeout=120)
        return json.loads(r.text)["data"][0]["url"]

    def restore_backup(self, path_to_backup_file):
        print("Restoring backup")
        logging.info("Restoring backup: " + path_to_backup_file)
        unf_backup = open(path_to_backup_file, "rb")
        r = requests.post(test_url, files = {"file": unf_backup})
        logging.info(r)
        print(r)
        return r

    def logout(self):
        logging.info("Logging out of " + self.hostname)
        url = self.url + "logout"
        r = self.s.get(url=url, verify=self.verify_ssl, timeout=30)
        self.s.close()
        logging.info("Logged out")
        logging.debug(r.status_code)