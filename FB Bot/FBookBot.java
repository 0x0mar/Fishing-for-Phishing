package examples.fbookbot;

import jodd.jerry.Jerry;
import jodd.jerry.JerryFunction;
import jodd.mutable.MutableInteger;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class FBookBot {

	private final static String EMAIL = "jcbraun@uchicago.edu";
	private final static String PASS = "3312crystal";

	public static void main(String[] args) throws IOException {
		Response response;

		response = loginToFacebook(EMAIL, PASS);

		response = findFriends(response);

		listAndAddFriends(response.getHtml(), new MutableInteger(0), response);
	}

	/**
	 * Creates new Facebook session.
	 */
	static Response loginToFacebook(String email, String pass) throws IOException {
		System.out.println("login...");
		Response response = HttpUtil.get("http://www.facebook.com", null);

		Jerry doc = Jerry.jerry(response.getHtml());
		Jerry loginForm = doc.$("#login_form");

		String action = loginForm.attr("action");

		Map<String, String> loginFormParams = JerryUtil.form(loginForm);
		loginFormParams.put("email", email);
		loginFormParams.put("pass", pass);

		return HttpUtil.post(action, loginFormParams, response.getCookieStore());
	}

	/**
	 * Reads the page with friends proposals.
	 */
	static Response findFriends(Response response) throws IOException {
		System.out.println("finding friends...");
		response = HttpUtil.get("http://www.facebook.com/find-friends/browser/?ref=tn", response.getCookieStore());
		return response;
	}

	/**
	 * Lists all friends and invite some.
	 */
	static void listAndAddFriends(String html, final MutableInteger numberOfFriendsToInvite, final Response response) {
		System.out.println("listing friends...\n");
		Jerry doc = Jerry.jerry(html);

		// find user id
		Jerry userLink = doc.$("#pageHead #headNav ul#pageNav li.topNavLink a");
		final String facebookUserId = extractId(userLink);
		System.out.println("facebook user id: " + facebookUserId);
		
		// find form id
		Jerry input = doc.$("input#post_form_id");
		final String postFormId = input.attr("value");
		System.out.println("post form id: " + postFormId);

		// parse friends
		Jerry form = doc.$("form.friendBrowserForm");

		form.$("ul.uiList li div.fsl").each(new JerryFunction() {
			public boolean onNode(Jerry $this, int index) {
				String friendName = $this.find("a").text();
				
				String friendFacebookId = extractId($this.$("a"));
				
				System.out.println(friendFacebookId + " > " + friendName);
				if (numberOfFriendsToInvite.value > 0) {
					try{
						addFriend(facebookUserId, friendFacebookId, postFormId, response);
					} catch (IOException ioex) {
						System.out.println("failed.");
					}
					numberOfFriendsToInvite.value--;
				}
				return true;
			}
		});
	}
	
	
	static void addFriend(String facebookUserId, String friendFacebookId, String postFormId, Response response) throws IOException {
		System.out.println(">>> adding friend: " + facebookUserId);

		HashMap<String, String> params = new HashMap<String, String>();
		
		params.put("__user", facebookUserId);
		params.put("action","add_friend");
		params.put("ego_log_data", "");
		params.put("fb_dtsg", "AQDloNJ-");
		params.put("how_found", "friend_browser");
		params.put("logging_location", "friend_browser");
		params.put("lsd", "");
		params.put("no_flyout_on_click", "true");
		params.put("outgoing_id", "");
		params.put("post_form_id", postFormId);
		params.put("post_form_id_source", "AsyncRequest");
		params.put("ref_param", "unknown");
		params.put("to_friend",	friendFacebookId);
		params.put("unwanted", "");
		
		response = HttpUtil.post("http://www.facebook.com/ajax/add_friend/action.php?__a=1", params, response.getCookieStore());
		System.out.println(response.getStatusLine());
	}

	/**
	 * Extracts facebook id from a link.
	 */
	static String extractId(Jerry link) {
		String href = link.attr("href");

		int index1 = href.indexOf("id=");
		if (index1 == -1) {
			href = link.attr("data-hovercard");
			index1 = href.indexOf("id=");
			if (index1 == -1) {
				return null;
			}
		}
		int index2 = href.indexOf('&', index1);
		if (index2 == -1) {
			return href.substring(index1);
		}
		return href.substring(index1, index2);
	}
}
