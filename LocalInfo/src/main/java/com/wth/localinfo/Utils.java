package com.wth.localinfo;

import com.wth.localinfo.model.MappedParams;

/**
 * 
 * Shared utilities.
 *
 */
public class Utils {

    public static MappedParams prepareParamsMap(String[] header, String[] nextLine) {
        MappedParams params = new MappedParams();
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
