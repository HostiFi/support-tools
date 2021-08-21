#!/bin/bash
while getopts d: option
do
case "${option}"
in
d) HOSTNAME=${OPTARG};;
esac
done

UNIFI_HOSTNAME=$HOSTNAME
UNIFI_SERVICE=unifi

UNIFI_DIR=/var/lib/unifi
JAVA_DIR=/usr/lib/unifi
KEYSTORE=${UNIFI_DIR}/keystore

LE_LIVE_DIR=/etc/letsencrypt/live

ALIAS=unifi
PASSWORD=aircontrolenterprise

echo "Importing SSL to UniFi"

LE_MODE=true

PRIV_KEY=${LE_LIVE_DIR}/${UNIFI_HOSTNAME}/privkey.pem
CHAIN_FILE=${LE_LIVE_DIR}/${UNIFI_HOSTNAME}/fullchain.pem

if [[ ${LE_MODE} == "true" ]]; then
	echo "Checking cert to see if it changed..."
	if md5sum -c "${LE_LIVE_DIR}/${UNIFI_HOSTNAME}/privkey.pem.md5" &>/dev/null; then
		echo "Cert is unchanged, exiting..."
		exit 0
	else
	echo "SSL changed, updating UniFi..."
	fi
fi

if [[ ! -f ${PRIV_KEY} ]] || [[ ! -f ${CHAIN_FILE} ]]; then
	echo "Files are missing"
	exit 1
else
	echo "Importing files"
fi

P12_TEMP=$(mktemp)

echo "Stopping UniFi"
service "${UNIFI_SERVICE}" stop

if [[ ${LE_MODE} == "true" ]]; then
	md5sum "${PRIV_KEY}" > "${LE_LIVE_DIR}/${UNIFI_HOSTNAME}/privkey.pem.md5"
fi

if [[ -s "${KEYSTORE}.orig" ]]; then
	cp "${KEYSTORE}" "${KEYSTORE}.bak"
else
	cp "${KEYSTORE}" "${KEYSTORE}.orig"
fi

if [[ -f ${SIGNED_CRT} ]]; then
    openssl pkcs12 -export \
    -in "${CHAIN_FILE}" \
    -in "${SIGNED_CRT}" \
    -inkey "${PRIV_KEY}" \
    -out "${P12_TEMP}" -passout pass:"${PASSWORD}" \
    -name "${ALIAS}"
else
    openssl pkcs12 -export \
    -in "${CHAIN_FILE}" \
    -inkey "${PRIV_KEY}" \
    -out "${P12_TEMP}" -passout pass:"${PASSWORD}" \
    -name "${ALIAS}"
fi
	
echo "Removing previous data from UniFi"
keytool -delete -alias "${ALIAS}" -keystore "${KEYSTORE}" -deststorepass "${PASSWORD}"
	

echo "Importing SSL into UniFi"
keytool -importkeystore \
-srckeystore "${P12_TEMP}" -srcstoretype PKCS12 \
-srcstorepass "${PASSWORD}" \
-destkeystore "${KEYSTORE}" \
-deststorepass "${PASSWORD}" \
-destkeypass "${PASSWORD}" \
-alias "${ALIAS}" -trustcacerts

rm -f "${P12_TEMP}"
	
echo "Restarting UniFi"
service "${UNIFI_SERVICE}" start


echo "Done"

exit 0