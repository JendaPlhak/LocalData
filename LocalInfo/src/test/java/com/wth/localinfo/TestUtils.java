package com.wth.localinfo;

import java.util.List;
import java.util.Map;
import java.util.Set;

public class TestUtils {

    public static void consolePrint(List<Map<String, String>> lines) throws Exception {
        for (Map<String, String> rowMap : lines) {
            Set<String> keySet = rowMap.keySet();
            for (String columnKey : keySet) {
                System.out.print(columnKey + "; ");
            }
            System.out.println();
            for (String columnKey : keySet) {
                System.out.print(rowMap.get(columnKey) + "; ");
            }
            System.out.println();
            System.out.println();
        }
    }

}
