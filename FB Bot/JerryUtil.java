package examples.fbookbot;

import jodd.jerry.Jerry;
import jodd.jerry.JerryFunction;

import java.util.HashMap;
import java.util.Map;

public class JerryUtil {

	/**
	 * Collects all names and values for all input elements
	 * of given form, quick and dirty.
	 */
	public static Map<String, String> form(Jerry form) {
		final Map<String, String> map = new HashMap<String, String>();
		form.first().$(":input").each(new JerryFunction() {
			public boolean onNode(Jerry $this, int index) {
				String name = $this.attr("name");
				String value = $this.attr("value");
				map.put(name, value);
				return true;
			}
		});
		return map;
	}
}
