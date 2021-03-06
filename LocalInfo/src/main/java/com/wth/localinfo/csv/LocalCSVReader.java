package com.wth.localinfo.csv;

import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import com.wth.localinfo.Utils;
import com.wth.localinfo.model.MappedParams;

import au.com.bytecode.opencsv.CSVReader;

/**
 * Reads CSV data and maps them with loaded header.
 */
public class LocalCSVReader {

    public String[] loadHeader(String file) throws IOException {
        CSVReader reader = new CSVReader(new FileReader(file));
        String[] header = reader.readNext();
        reader.close();
        return header;
    }

    public List<MappedParams> load(String file) throws IOException {
        List<MappedParams> mappedLines = new ArrayList<MappedParams>();
        CSVReader reader = new CSVReader(new FileReader(file));

        // The first line is header definition.
        String[] header = reader.readNext();

        String[] nextLine;
        while ((nextLine = reader.readNext()) != null) {
            MappedParams params = Utils.prepareParamsMap(header, nextLine);
            mappedLines.add(params);
        }
        reader.close();
        return mappedLines;
    }

}
