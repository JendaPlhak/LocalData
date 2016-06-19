package com.wth.localinfo;

import java.util.HashMap;
import java.util.Map;

/**
 * 
 * Shared utilities.
 *
 */
public class Utils {

    public static Map<String, String> prepareParamsMap(String[] header, String[] nextLine) {
        Map<String, String> params = new HashMap<String, String>();
        for (int i = 0; i < header.length; i++) {
            String columnName = header[i];
            params.put(columnName, nextLine[i]);
        }
        return params;
    }

    public static String getItems(String[] values) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < values.length;) {
            sb.append(values[i]);
            i++;
            if (i < values.length) {
                sb.append(",");
            }
        }
        return sb.toString();
    }

}
