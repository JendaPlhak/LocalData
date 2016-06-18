package com.wth.localinfo.csv;

import java.util.List;
import java.util.Map;
import java.util.Set;

import org.junit.Test;

import com.wth.localinfo.TestConsts;

public class LocalCSVReaderCopy {

    private final LocalCSVReader reader = new LocalCSVReader();

    @Test
    public void testDataPrint() throws Exception {
        dataPrint(reader.load(TestConsts.CSV_FILE_NAME));
    }

    public void dataPrint(List<Map<String, String>> lines) throws Exception {
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
