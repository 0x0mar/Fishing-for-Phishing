package examples.fbookbot;

import org.apache.http.HttpEntity;
import org.apache.http.HttpRequest;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.ProtocolException;
import org.apache.http.client.CookieStore;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.impl.client.DefaultRedirectStrategy;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.params.HttpProtocolParams;
import org.apache.http.protocol.HttpContext;
import org.apache.http.util.EntityUtils;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class HttpUtil {

	/**
	 * Creates HTTP client. Uses Firefox User-Agent to fool Facebook.
	 * Sets cookies from provided CookieStore.
	 */
	private static DefaultHttpClient createHttpClient(CookieStore cookieStore) {
		DefaultHttpClient httpclient = new DefaultHttpClient();

		HttpProtocolParams.setUserAgent(httpclient.getParams(), "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:9.0.1) Gecko/20100101 Firefox/9.0.1");

		if (cookieStore != null) {
			httpclient.setCookieStore(cookieStore);
		}
		return httpclient;
	}

	/**
	 * Sends GET request.
	 */
	public static Response get(String url, CookieStore cookieStore) throws IOException {
		DefaultHttpClient httpclient = createHttpClient(cookieStore);

		HttpGet httpget = new HttpGet(url);
		HttpResponse response = httpclient.execute(httpget);

		HttpEntity entity = response.getEntity();
		if (entity == null) {
			return null;
		}

		String content = EntityUtils.toString(entity);
		httpclient.getConnectionManager().shutdown();
		return new Response(content, response.getStatusLine(), httpclient.getCookieStore());
	}

	/**
	 * Sends POST request.
	 */
	public static Response post(String action, Map<String, String> parameters, CookieStore cookieStore) throws IOException {
		DefaultHttpClient httpclient = createHttpClient(cookieStore);

		httpclient.setRedirectStrategy(new DefaultRedirectStrategy() {
			public boolean isRedirected(HttpRequest request, HttpResponse response, HttpContext context) {
				boolean isRedirect = false;
				try {
					isRedirect = super.isRedirected(request, response, context);
				} catch (ProtocolException e) {
					e.printStackTrace();
				}
				if (!isRedirect) {
					int responseCode = response.getStatusLine().getStatusCode();
					if (responseCode == 301 || responseCode == 302) {
						return true;
					}
				}
				return isRedirect;
			}
		});


		HttpPost httpPost = new HttpPost(action);

		List<NameValuePair> nvps = new ArrayList<NameValuePair>();
		for (Map.Entry<String, String> entry : parameters.entrySet()) {
			String name = entry.getKey();
			if (name == null) {
				continue;
			}
			String value = entry.getValue();
			nvps.add(new BasicNameValuePair(name, value));
		}

		httpPost.setEntity(new UrlEncodedFormEntity(nvps));
		HttpResponse response = httpclient.execute(httpPost);

		HttpEntity entity = response.getEntity();
		if (entity == null) {
			return null;
		}

		String content = EntityUtils.toString(entity);
		httpclient.getConnectionManager().shutdown();
		return new Response(content, response.getStatusLine(), httpclient.getCookieStore());
	}
}
