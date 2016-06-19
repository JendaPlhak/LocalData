package com.wth.localinfo.writer;

import org.junit.Test;

import com.wth.localinfo.TestConsts;
import com.wth.localinfo.csv.LocalCSVReader;
import com.wth.localinfo.jdbc.JDBCReader;
import com.wth.localinfo.ws.WSClient;

public class JDBCRemoteWriterTest {

    @Test
    public void testName() throws Exception {
        RemoteWriter remoteWriter = new RemoteWriter(new WSClient());

        String[] header = new LocalCSVReader().loadHeader(TestConsts.CSV_TABLE_HEADER_FILE_NAME);
        JDBCReader reader = new JDBCReader(header);
        int testLimit = 5;
        int queriesCount = remoteWriter.remoteWrite(reader.load(testLimit));
        System.out.println("Sent queries... " + queriesCount);
    }

}
