package io.werender.examples;

import java.io.IOException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.text.SimpleDateFormat;
import java.util.Base64;
import java.util.Calendar;
import java.util.Locale;
import java.util.TimeZone;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

import okhttp3.Interceptor;
import okhttp3.Request;
import okhttp3.Response;

public class SignatureInterceptor implements Interceptor {
    private static final String SIGNATURE_ALGORITHM = "HmacSHA1";

    private String publicKey;
    private String privateKey;

    private static String getDate() {
	Calendar calendar = Calendar.getInstance();
	SimpleDateFormat dateFormat = new SimpleDateFormat("EEE, dd MMM yyyy HH:mm:ss z", Locale.US);
	dateFormat.setTimeZone(TimeZone.getTimeZone("GMT"));
	return dateFormat.format(calendar.getTime());
    }

    private static String getSignature(String method, String host, String date, String privateKey) {
	String message = String.format("%s\n%s\n%s", method, host, date);
	String signature = null;
	try {
	    SecretKeySpec signingKey = new SecretKeySpec(privateKey.getBytes(), SIGNATURE_ALGORITHM);
	    Mac mac = Mac.getInstance(SIGNATURE_ALGORITHM);
	    mac.init(signingKey);
	    byte[] macOutput = mac.doFinal(message.getBytes());
	    signature = Base64.getEncoder().encodeToString(macOutput);
	} catch (NoSuchAlgorithmException e) {
	    e.printStackTrace();
	} catch (InvalidKeyException e) {
	    e.printStackTrace();
	}
	return signature;
    }

    public SignatureInterceptor(String publicKey, String privateKey) {
	this.publicKey = publicKey;
	this.privateKey = privateKey;
    }

    @Override
    public Response intercept(Chain chain) throws IOException {
	Request request = chain.request();
	String method = request.method();
	String date = getDate();
	String host = request.url().host();
	String signature = getSignature(method, host, date, privateKey);
	Request newRequest = request.newBuilder()
		.addHeader("Authorization", String.format("WR %s:%s", publicKey, signature))
		.addHeader("Date", getDate()).addHeader("Host", host).build();
	return chain.proceed(newRequest);
    }

}
