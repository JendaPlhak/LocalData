package com.wth.localinfo.csv;

import org.junit.Test;

import com.wth.localinfo.TestConsts;
import com.wth.localinfo.TestUtils;

public class LocalCSVReaderTest {

    private final LocalCSVReader reader = new LocalCSVReader();

    @Test
    public void testDataPrint() throws Exception {
        TestUtils.consolePrint(reader.load(TestConsts.CSV_FILE_NAME));
    }

}
