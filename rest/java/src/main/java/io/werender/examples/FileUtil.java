package io.werender.examples;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.security.MessageDigest;

import javax.xml.bind.annotation.adapters.HexBinaryAdapter;

public final class FileUtil {
    
    public static final String MODE_STRICT = "strict";
    public static final String MODE_UNIQUE = "unique";

    public static final String EXT_FBX = "fbx";
    public static final String EXT_USD = "usd";
    
    public static final String CONTENT_TYPE_BINARY = "application/octet-stream";
    public static final String CONTENT_TYPE_MODEL_FBX = "model/fbx";
    public static final String CONTENT_TYPE_MODEL_USD = "model/usd";

    public static String computeFileChecksum(File file) throws Exception {
	MessageDigest sha1 = MessageDigest.getInstance("SHA-1");
	try (InputStream input = new FileInputStream(file)) {

	    byte[] buffer = new byte[8192];
	    int len = input.read(buffer);

	    while (len != -1) {
		sha1.update(buffer, 0, len);
		len = input.read(buffer);
	    }

	    String checksum = new HexBinaryAdapter().marshal(sha1.digest());
	    checksum = "sha1:" + checksum.toLowerCase();
	    return checksum;
	}
    }

    public static String getContentType(String filePath) {
	String contentType = CONTENT_TYPE_BINARY;
	String[] tokens = filePath.split("\\.");
	if (tokens.length > 0) {
	    String lastToken = tokens[tokens.length - 1];
	    switch (lastToken) {
	    case EXT_FBX:
		contentType = CONTENT_TYPE_MODEL_FBX;
		break;
	    case EXT_USD:
		contentType = CONTENT_TYPE_MODEL_USD;
		break;
	    default:
		break;
	    }
	}
	return contentType;
    }

}
