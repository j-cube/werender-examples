package io.werender.examples;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

import org.apache.commons.lang3.SystemUtils;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

public class Config {
    private static Log log = LogFactory.getLog(Config.class);

    public static final String DEFAULT_SERVER_ADDRESS = "https://api-us-east-2.werender.io/v1";
    public static final String DEFAULT_SERVER_VERSION = "v1";

    private String address;
    private String publicKey;
    private String privateKey;

    public static Config create() {
	/* Create instance. */
	Config config = new Config();

	/* Get home folder and configuration folder. */
	String homeDirPath = SystemUtils.getUserHome().getAbsolutePath();
	String configDirPath = new String(homeDirPath);
	if (SystemUtils.IS_OS_MAC_OSX) {
	    configDirPath += "/Library/Application Support/werender";
	} else {
	    log.fatal(String.format("Unsupported platform"));
	}

	/* Read werender.config file. */
	try {
	    String serverAddress = Config.DEFAULT_SERVER_ADDRESS;

	    String configFilePath = configDirPath + "/werender.config";
	    FileReader reader = new FileReader(configFilePath);
	    JsonParser parser = new JsonParser();
	    JsonElement rootElement = parser.parse(reader);
	    JsonObject rootObject = rootElement.getAsJsonObject();
	    if (rootObject.has("internal")) {
		JsonObject internalObject = rootObject.get("internal").getAsJsonObject();
		if (internalObject.has("server")) {
		    JsonObject serverObject = internalObject.get("server").getAsJsonObject();
		    if (serverObject.has("server_address")) {
			serverAddress = serverObject.get("server_address").getAsString();
		    }
		}
	    }

	    if (!serverAddress.endsWith(DEFAULT_SERVER_VERSION)) {
		serverAddress += String.format("/%s", DEFAULT_SERVER_VERSION);
	    }
	    config.setAddress(serverAddress);
	} catch (FileNotFoundException e) {
	    e.printStackTrace();
	}

	/* Read werender.key file. */
	try {
	    String keyFilePath = configDirPath + "/werender.key";
	    String key = Files.readString(Paths.get(keyFilePath));
	    String[] keyTokens = key.split(",");
	    config.setPublicKey(keyTokens[0]);
	    config.setPrivateKey(keyTokens[1].trim());
	} catch (IOException e) {
	    e.printStackTrace();
	}

	/* Return instance. */
	return config;
    }

    private Config() {
    }

    public String getAddress() {
	return address;
    }

    public void setAddress(String address) {
	this.address = address;
    }

    public String getPublicKey() {
	return publicKey;
    }

    public void setPublicKey(String publicKey) {
	this.publicKey = publicKey;
    }

    public String getPrivateKey() {
	return privateKey;
    }

    public void setPrivateKey(String privateKey) {
	this.privateKey = privateKey;
    }

}
