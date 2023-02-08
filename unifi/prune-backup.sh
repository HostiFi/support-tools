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

java jdk.internal.jshell.tool.JShellToolProvider "-R-Din_file=${in_file}" "-R-Dout_file=${out_file}" --class-path="${mongo_jar[0]}" - <<'EOF'
var key = new javax.crypto.spec.SecretKeySpec("bcyangkmluohmars".getBytes(), "AES");
var iv = new javax.crypto.spec.IvParameterSpec("ubntenterpriseap".getBytes());

var decryptCipher = javax.crypto.Cipher.getInstance("AES/CBC/NoPadding");
decryptCipher.init(javax.crypto.Cipher.DECRYPT_MODE, key, iv);
var unzip = new java.util.zip.ZipInputStream(new javax.crypto.CipherInputStream(new java.io.FileInputStream(System.getProperty("in_file")), decryptCipher));

var encryptCipher = javax.crypto.Cipher.getInstance("AES/CBC/NoPadding");
encryptCipher.init(javax.crypto.Cipher.ENCRYPT_MODE, key, iv);
var rezip = new java.util.zip.ZipOutputStream(new javax.crypto.CipherOutputStream(new java.io.FileOutputStream(System.getProperty("out_file")), encryptCipher));

for (;;) {
    var entry = unzip.getNextEntry();
    if (entry == null)
        break;
    rezip.putNextEntry(entry);
    if (entry.getName().equals("db_stat.gz")) {
        new java.util.zip.GZIPOutputStream(rezip).finish();
    } else if (entry.getName().equals("db.gz")) {
        var bsonStream = new java.util.zip.GZIPInputStream(unzip);
        var bsonOutStream = new java.util.zip.GZIPOutputStream(rezip);
        var bsonDecoder = new org.bson.BasicBSONDecoder();
        var bsonEncoder = new org.bson.BasicBSONEncoder();
        String collection = null;
        while (bsonStream.available() != 0) {
            var bson = bsonDecoder.readObject(bsonStream);
            if (bson.containsField("__cmd")) {
                if (!bson.get("__cmd").equals("select")) {
                    throw new RuntimeException("Invalid command in bson");
                }
                collection = (String) bson.get("collection");
            } else if (collection.equals("alert") ||
                       collection.equals("rogue") ||
                       collection.equals("alarm") ||
                       collection.equals("event") ||
                       collection.equals("voucher") ||
                       collection.equals("guest") ||
                       (collection.equals("user") && !(bson.containsField("use_fixedip") || bson.containsField("noted") || bson.containsField("blocked")))) {
                continue;
            }
            bsonOutStream.write(bsonEncoder.encode(bson));
        }
    } else {
        unzip.transferTo(rezip);
    }
}

rezip.close();
EOF
