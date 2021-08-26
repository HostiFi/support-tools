from pyzabbix import ZabbixAPI
import config
import sys
import logging
import argparse
from enum import Enum
import warnings
import time
import random
import string

class Zabbix(object):
    def __init__(self):
        self.zapi = ZabbixAPI(config.ZABBIX_URL)
        self.zapi.login(config.ZABBIX_API_USER, config.ZABBIX_API_KEY)

    def get_maintenance_ids_from_hostid(self, hostid):
        logging.info("Getting maintenance ids from hostid")
        maintenance_ids = []
        r = self.zapi.maintenance.get(selectHosts="extend")
        logging.info(r)
        for row in r:
            for host in row["hosts"]:
                if host["hostid"] == hostid:
                    logging.info(row["maintenanceid"])
                    maintenance_ids.append(row["maintenanceid"])
        return maintenance_ids

    def get_hostid_from_hostname(self, hostname):
        logging.info("Getting Zabbix hostid from hostname...")
        return self.zapi.host.get(filter={"host": [hostname]})[0]["hostid"]

    def delete_maintenance_period(self, maintenanceid):
        logging.info("Deleting maintenance period...")
        r = self.zapi.maintenance.delete(maintenanceid)
        logging.info(r)
        return r
    
    def get_random_string(self, size=5, chars=string.digits + string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))

    def create_maintenance_period(self, server):
        logging.info("Creating maintenance period...")
        r = self.zapi.maintenance.create({
            "name": server + " - temporary maintenance period " + self.get_random_string(),
            "active_since": 1358844540,
            "active_till": 2119446139,
            "groupids": [
                config.ZABBIX_EMPTY_HOSTGROUPID
            ],
            "hostids": [],
            "timeperiods": [
                {
                    "timeperiod_type": 0,
                    "period": 3600
                }
            ]
        })
        logging.info(r)
        return r["maintenanceids"][0]

    def get_hostids_in_maintenance_period(self, maintenanceid):
        logging.info("Getting hosts in maintenance period...")
        r = self.zapi.maintenance.get(params={"maintenanceid": maintenanceid}, selectHosts="extend")
        logging.info(r)
        existing_hostids = []
        for row in r:
            logging.info(row)
            if row["maintenanceid"] == maintenanceid:
                logging.info("Found matching maintenanceid")
                for host in row["hosts"]:
                    logging.info(host)
                    existing_hostids.append(host["hostid"])
        logging.info("Existing hostids list:")
        logging.info(existing_hostids)
        return existing_hostids

    def get_hostids_in_maintenance_mode(self):
        logging.info("Getting hosts in maintenance mode...")
        r = self.zapi.maintenance.get(selectHosts="extend")
        logging.info(r)
        existing_hostids = []
        for row in r:
            for host in row["hosts"]:
                logging.info(host)
                existing_hostids.append(host["hostid"])
        return existing_hostids

    def put_hostids_into_maintenance_mode(self, maintenanceid, hostids):
        logging.info("Putting hosts into maintenance mode...")
        logging.info("Get existing hostids already in the maintenance period")
        existing_hostids = self.get_hostids_in_maintenance_period(maintenanceid)
        logging.info("Add the new hostids to the list, skipping duplicates")
        new_hostids = list(set(existing_hostids + hostids))
        logging.info(new_hostids)
        logging.info("Updating maintenance period with new hostids")
        r = self.zapi.maintenance.update({"maintenanceid": maintenanceid, "hostids": new_hostids})
        logging.info(r)
        return r

    def remove_hostids_from_maintenance_mode(self, maintenanceid, hostids):
        logging.info("Removing hosts from maintenance mode...")
        logging.info("Get existing hostids already in the maintenance period")
        existing_hostids = self.get_hostids_in_maintenance_period(maintenanceid)
        logging.info("Removing hostids from the list...")
        new_hostids = list(filter(lambda i: i not in hostids, existing_hostids))
        logging.info(new_hostids)
        logging.info("Updating maintenance period with new hostids")
        r = self.zapi.maintenance.update({"maintenanceid": maintenanceid, "hostids": new_hostids})
        logging.info(r)
        return r