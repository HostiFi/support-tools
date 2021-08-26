import requests
import logging
import time
import json

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

    def create_manual_backup(self):
        logging.info("Running cmd")
        params = {"cmd": 'backup'}
        params = json.dumps(params)
        url = self.url + "api/s/default/cmd/backup"
        r = self.s.post(url=url, data=params, verify=self.verify_ssl, timeout=120)
        return json.loads(r.text)["data"][0]["url"]

    def logout(self):
        logging.info("Logging out of " + self.hostname)
        url = self.url + "logout"
        r = self.s.get(url=url, verify=self.verify_ssl, timeout=30)
        self.s.close()
        logging.info("Logged out")
        logging.debug(r.status_code)