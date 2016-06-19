package com.wth.localinfo;

import java.util.List;
import java.util.Set;

import com.wth.localinfo.model.MappedParams;

public class TestUtils {

    public static void consolePrint(List<MappedParams> lines) throws Exception {
        for (MappedParams rowMap : lines) {
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
