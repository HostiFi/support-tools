import zabbix
import config
import logging
import socket

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

r = socket.gethostname()
hostname = r.split('.')[0] + ".hostifi.com"

zabbix = zabbix.Zabbix()
hostid = [zabbix.get_hostid_from_hostname(hostname)]
logging.info("hostid:")
logging.info(hostid)
existing_hostids = zabbix.get_hostids_in_maintenance_mode()
logging.info("Existing hostids:")
logging.info(existing_hostids)

if hostid[0] in existing_hostids:
	logging.info("Removing server from maintenance mode on Zabbix")
	maintenance_ids = []
	maintenance_ids = zabbix.get_maintenance_ids_from_hostid(hostid[0])
	logging.info("Maintenance IDs:")
	logging.info(maintenance_ids)
	for maintenanceid in maintenance_ids:
		logging.info("Removing " + hostid[0] + " from " + maintenanceid)
		zabbix.remove_hostids_from_maintenance_mode(maintenanceid, hostid)
		zabbix.delete_maintenance_period(maintenanceid)
	print("Maintenance mode disabled")
else:
	logging.info("Placing server in maintenance period on Zabbix...")
	maintenanceid = zabbix.create_maintenance_period(hostname)
	zabbix.put_hostids_into_maintenance_mode(maintenanceid, hostid)
	logging.info("Server is in maintenance mode on Zabbix now")
	print("Maintenance mode enabled")
