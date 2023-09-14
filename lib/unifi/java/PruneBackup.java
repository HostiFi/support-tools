import java.io.EOFException;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

import java.util.zip.GZIPInputStream;
import java.util.zip.GZIPOutputStream;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;
import java.util.zip.ZipOutputStream;

import javax.crypto.Cipher;
import javax.crypto.CipherInputStream;
import javax.crypto.CipherOutputStream;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

import org.bson.BSONObject;
import org.bson.BasicBSONDecoder;
import org.bson.BasicBSONEncoder;

public class PruneBackup {
    public static SecretKeySpec KEY =
        new SecretKeySpec("bcyangkmluohmars".getBytes(), "AES");
    public static IvParameterSpec IV =
        new IvParameterSpec("ubntenterpriseap".getBytes());

    private static Cipher makeCipher(int mode) {
        try {
            var cipher = Cipher.getInstance("AES/CBC/NoPadding");
            cipher.init(mode, KEY, IV);
            return cipher;
        } catch (Exception ex) {
            throw new RuntimeException(ex);
        }
    }

    private static ZipInputStream openBackupInput(InputStream in) {
        var cis = new CipherInputStream(in, makeCipher(Cipher.DECRYPT_MODE));
        return new ZipInputStream(cis);
    }

    private static ZipOutputStream openBackupOutput(OutputStream out) {
        var cos = new CipherOutputStream(out, makeCipher(Cipher.ENCRYPT_MODE));
        return new ZipOutputStream(cos);
    }

    private static void pruneDbGz(InputStream in, OutputStream out)
        throws IOException {

        var decoder = new BasicBSONDecoder();
        var encoder = new BasicBSONEncoder();
        var bsonIn = new GZIPInputStream(in);
        var bsonOut = new GZIPOutputStream(out);
        try {
            for (String collection = null;;) {
                BSONObject bson;
                try {
                    bson = decoder.readObject(bsonIn);
                } catch (EOFException ex) {
                    break;
                }
                if (bson.containsField("__cmd")) {
                    if (!bson.get("__cmd").equals("select")) {
                        throw new RuntimeException("Invalid command in bson");
                    }
                    collection = (String) bson.get("collection");
                } else {
                    switch (collection) {
                    case "alert":
                    case "rogue":
                    case "alarm":
                    case "event":
                    case "voucher":
                    case "guest":
                        continue;

                    case "user":
                        if (!(bson.containsField("use_fixedip") ||
                              bson.containsField("noted") ||
                              bson.containsField("blocked"))) {
                            continue;
                        }
                    }
                }
                bsonOut.write(encoder.encode(bson));
            }
        } finally {
            bsonOut.finish();
        }
    }

    public static void main(String... args) throws IOException {
        if (args.length != 2) {
            System.err.println("Usage: PruneBackup in_file out_file");
            System.exit(2);
        }

        var in_file = args[0];
        var out_file = args[1];

        try (var in = openBackupInput(new FileInputStream(in_file));
             var out = openBackupOutput(new FileOutputStream(out_file))) {
            for (;;) {
                ZipEntry entry = null;
                try {
                    entry = in.getNextEntry();
                } catch (EOFException ex) {}
                if (entry == null)
                    break;

                out.putNextEntry(entry);

                switch (entry.getName()) {
                case "db_stat.gz":
                    new GZIPOutputStream(out).finish();
                    break;

                case "db.gz":
                    pruneDbGz(in, out);
                    break;

                default:
                    in.transferTo(out);
                }
            }
        }
    }
}
