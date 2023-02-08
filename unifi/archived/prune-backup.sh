#!/bin/sh
# Reilly's less efficient Python3 implementation of Andrew's Java prune-backup.sh

set -e

echo "Input .unf file name:"
read INPUT_UNF
echo "Output .unf file name:"
read OUTPUT_UNF

OUTPUT_ZIP="unf.zip"
DIR_PATH=$(cd $(dirname “${BASH_SOURCE:-$0}”) && pwd)
TMP_FILE=$(mktemp)
trap "rm -f ${TMP_FILE}" EXIT

openssl enc -d -in "${INPUT_UNF}" -out "${TMP_FILE}" -aes-128-cbc -K 626379616e676b6d6c756f686d617273 -iv 75626e74656e74657270726973656170 -nopad
yes | zip -FF "${TMP_FILE}" --out "${OUTPUT_ZIP}" > /dev/null 2>&1

unzip ${OUTPUT_ZIP} -d unf_unzip > /dev/null 2>&1
rm unf_unzip/db_stat.gz
touch unf_unzip/db_stat
gzip unf_unzip/db_stat
gunzip unf_unzip/db.gz
/usr/bin/python3 /root/support-tools/lib/unifi/py/prune-db.py -f $DIR_PATH/unf_unzip/db
mv unf_unzip/db_new unf_unzip/db
gzip unf_unzip/db
cd unf_unzip
zip -r ../unf_new.zip . > /dev/null 2>&1
cd ..
rm -R unf_unzip > /dev/null 2>&1

INPUT_ZIP="unf_new.zip"

openssl enc -e -in "${INPUT_ZIP}" -out "${OUTPUT_UNF}" -aes-128-cbc -K 626379616e676b6d6c756f686d617273 -iv 75626e74656e74657270726973656170

rm unf_new.zip
rm unf.zip