package com.wth.localinfo.csv;

import java.util.List;

import org.junit.Assert;
import org.junit.Test;

import com.wth.localinfo.TestConsts;
import com.wth.localinfo.TestUtils;
import com.wth.localinfo.model.MappedParams;

public class LocalCSVReaderTest {

    private final LocalCSVReader reader = new LocalCSVReader();

    @Test
    public void testDataPrint() throws Exception {
        List<MappedParams> csvData = reader.load(TestConsts.CSV_FILE_NAME);
        TestUtils.consolePrint(csvData);
        Assert.assertTrue("Loaded data should not be empty.", !csvData.isEmpty());
    }

}
