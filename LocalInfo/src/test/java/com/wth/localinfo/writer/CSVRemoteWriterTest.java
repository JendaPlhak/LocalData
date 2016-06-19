package com.wth.localinfo.writer;

import org.junit.Test;

import com.wth.localinfo.TestConsts;
import com.wth.localinfo.csv.LocalCSVReader;
import com.wth.localinfo.ws.WSClient;

public class CSVRemoteWriterTest {

    @Test
    public void testName() throws Exception {
        RemoteWriter remoteWriter = new RemoteWriter(new WSClient());
        LocalCSVReader localCSVReader = new LocalCSVReader();
        remoteWriter.remoteWrite(localCSVReader.load(TestConsts.CSV_FILE_NAME));
    }

}
