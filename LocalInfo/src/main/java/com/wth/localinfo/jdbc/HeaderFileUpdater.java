package com.wth.localinfo.jdbc;

import java.io.File;
import java.io.FileOutputStream;

import org.junit.Assert;

import com.wth.localinfo.TestConsts;
import com.wth.localinfo.Utils;
import com.wth.localinfo.csv.LocalCSVReader;

public class HeaderFileUpdater {

    private final JDBCReader reader;

    public HeaderFileUpdater(JDBCReader reader) {
        super();
        this.reader = reader;
    }

    public void updateHeaderFile() throws Exception {
        String[] currentHeader = reader.loadHeader();
        String headerLine = Utils.getItems(currentHeader);
        File headerFile = new File(TestConsts.CSV_TABLE_HEADER_FILE_NAME);
        FileOutputStream fos = new FileOutputStream(headerFile);
        fos.write(headerLine.getBytes());
        fos.close();
        System.out.println("Header file updated by...\n" + headerLine);
        Assert.assertTrue("Header file should exist.", headerFile.exists());
    }

    public static void main(String[] args) throws Exception {
        String[] header = new LocalCSVReader().loadHeader(TestConsts.CSV_TABLE_HEADER_FILE_NAME);
        HeaderFileUpdater updater = new HeaderFileUpdater(new JDBCReader(header));
        updater.updateHeaderFile();
    }

}
