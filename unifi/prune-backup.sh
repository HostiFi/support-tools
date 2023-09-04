#!/bin/bash

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

declare -a mongo_jar=(/usr/lib/unifi/lib/mongo-java-driver-*.jar)

java -classpath "${BASH_SOURCE[0]%/*}/../lib/unifi/java:${mongo_jar[0]}" \
     PruneBackup "$in_file" "$out_file"
