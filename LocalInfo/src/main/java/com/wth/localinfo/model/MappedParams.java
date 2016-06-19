package com.wth.localinfo.model;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

public class MappedParams {

    private final Map<String, String> params = new HashMap<String, String>();

    public String put(String key, String value) {
        return params.put(key, value);
    }

    public String get(Object key) {
        return params.get(key);
    }

    public Set<String> keySet() {
        return params.keySet();
    }

}
