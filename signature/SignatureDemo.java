import java.io.UnsupportedEncodingException;
import java.security.InvalidKeyException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SignatureException;
import java.text.SimpleDateFormat;
import java.util.Base64;
import java.util.Date;
import java.util.Locale;
import java.util.TimeZone;
import java.util.UUID;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

public class SignatureDemo {

	private static final String ALGORITHM_HMAC_MD5 = "HmacMD5"; // HMAC-MD5
	private static final String ALGORITHM_HMAC_SHA1 = "HmacSHA1"; // HMAC-SHA1，推荐使用
	private static final String ALGORITHM_HMAC_SHA256 = "HmacSHA256"; // HMAC-SHA256

	private static final String APP_SECRET = "pealse input your app secret here";

	/**
	 * 计算Content-MD5
	 * @param data 请求body，JSON格式字符串，不添加\n、\t、\和空格字符
	 * @return Content-MD5
	 */
	public String calculateMd5(String data) throws NoSuchAlgorithmException, UnsupportedEncodingException {
		MessageDigest md = MessageDigest.getInstance("MD5");
		md.update(data.getBytes("utf-8"));
		return Base64.getEncoder().encodeToString(md.digest());
	}

	/**
	 * 计算签名，采用HMAC-SHA1签名算法
	 * @param data 按规则拼接的加签字符串
	 * @return 签名
	 */
	public String calculateSignature(String data)
		throws SignatureException, NoSuchAlgorithmException, InvalidKeyException, UnsupportedEncodingException {
		SecretKeySpec signingKey = new SecretKeySpec(APP_SECRET.getBytes("utf-8"), ALGORITHM_HMAC_SHA1);
		Mac mac = Mac.getInstance(ALGORITHM_HMAC_SHA1);
		mac.init(signingKey);
		return Base64.getEncoder().encodeToString(mac.doFinal(data.getBytes("utf-8")));
	}

	public static void main(String[] args) throws Exception {
		SignatureDemo demo = new SignatureDemo();
		String body = "{\"name\":\"张大爷\",\"gender\":\"male\",\"id_card\":\"510123193810081230\",\"mobile\":\"18612345678\",\"birthday\":\"1930-10-08\"}";
		String contentMd5 = demo.calculateMd5(body);
		System.out.println("Content-MD5 = " + contentMd5);
		
		String verb = "POST";
		String contentType = "application/json;charset=utf-8";
		SimpleDateFormat sdf = new SimpleDateFormat("EEE, d MMM yyyy HH:mm:ss 'GMT'Z", Locale.US);
		sdf.setTimeZone(TimeZone.getDefault()); 
		String date = sdf.format(new Date());
		String host = "***.***.***";
		String signatureMethod = "HMAC-SHA1";
		String signatureNonce = UUID.randomUUID().toString();
		String signatureVersion = "1.0";
		// GET请求示例：uri = "/v1/olds?mobile=18612345678&order=asc&order_by=old_id&page=1&page_size=50"
		String uri = "/v1/olds"; 

		String stringToSign = verb + "\n"
			+ (verb.equals("POST") || verb.equals("PUT") ? contentMd5 + "\n" + contentType + "\n" : "")
            + date + "\n"
            + host + "\n"
            + signatureMethod + "\n"
            + signatureNonce + "\n"
            + signatureVersion + "\n"
			+ uri;
		System.out.println("stringToSign:\n" + stringToSign);
			
		String signature = demo.calculateSignature(stringToSign);
		System.out.println("signature = " + signature);
  }
  
}
