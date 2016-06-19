package com.wth.localinfo.jdbc;

import java.io.IOException;
import java.util.List;

import org.junit.Assert;
import org.junit.Test;

import com.wth.localinfo.TestConsts;
import com.wth.localinfo.TestUtils;
import com.wth.localinfo.Utils;
import com.wth.localinfo.csv.LocalCSVReader;
import com.wth.localinfo.model.MappedParams;

public class JDBCReaderTest {

    private final JDBCReader reader;

    public JDBCReaderTest() throws IOException {
        String[] header = new LocalCSVReader().loadHeader(TestConsts.CSV_TABLE_HEADER_FILE_NAME);
        reader = new JDBCReader(header);
    }

    @Test
    public void testDataPrint() throws Exception {
        int defaultLimit = 5;
        List<MappedParams> loadedData = reader.load(defaultLimit);
        TestUtils.consolePrint(loadedData);
        Assert.assertTrue("Loaded data should not be empty.", !loadedData.isEmpty());
    }

    @Test
    public void testLoadHeader() throws Exception {
        String[] header = reader.loadHeader();
        System.out.println(Utils.getItems(header));
        Assert.assertNotNull(header);
    }

}
