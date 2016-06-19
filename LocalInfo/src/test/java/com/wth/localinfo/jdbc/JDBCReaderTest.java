package com.wth.localinfo.jdbc;

import java.io.IOException;

import org.junit.Test;

import com.wth.localinfo.TestConsts;
import com.wth.localinfo.TestUtils;
import com.wth.localinfo.csv.LocalCSVReader;

public class JDBCReaderTest {

    private final JDBCReader reader;

    public JDBCReaderTest() throws IOException {
        String[] header = new LocalCSVReader().loadHeader(TestConsts.CSV_TABLE_HEADER_FILE_NAME);
        reader = new JDBCReader(header);
    }

    @Test
    public void testDataPrint() throws Exception {
        int defaultLimit = 5;
        TestUtils.consolePrint(reader.load(defaultLimit));
    }

}
