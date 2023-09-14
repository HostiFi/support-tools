#!/bin/bash

set -eu
shopt -s extglob

declare in_file out_file
if (( $# )); then
  in_file="$1"; shift
else
  IFS= read -e -p "Input .unf file name: " in_file
  in_file="${in_file% }"
fi

if (( $# )); then
  out_file="$1"; shift
else
  IFS= read -e -p "Output .unf file name: " out_file
  out_file="${out_file% }"
fi

declare -a bson_jar=(/usr/lib/unifi/lib/bson-*([0-9.]).jar)
if (( ${#bson_jar[@]} == 0 )); then
	bson_jar=(/usr/lib/unifi/lib/mongo-java-driver-*([0-9.]).jar)
fi

java -classpath "${BASH_SOURCE[0]%/*}/../lib/unifi/java:${bson_jar[0]}" \
     PruneBackup "$in_file" "$out_file"
