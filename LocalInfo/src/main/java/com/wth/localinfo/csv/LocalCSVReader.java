package com.wth.localinfo.csv;

import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import au.com.bytecode.opencsv.CSVReader;

/**
 * Reads CSV data and maps them with loaded header.
 */
public class LocalCSVReader {

    public List<Map<String, String>> load(String file) throws IOException {
        List<Map<String, String>> mappedLines = new ArrayList<Map<String, String>>();
        CSVReader reader = new CSVReader(new FileReader(file));

        // The first line is header definition.
        String[] header = reader.readNext();

        String[] nextLine;
        while ((nextLine = reader.readNext()) != null) {
            Map<String, String> params = prepareParamsMap(header, nextLine);
            mappedLines.add(params);
        }
        reader.close();
        return mappedLines;
    }

    private Map<String, String> prepareParamsMap(String[] header, String[] nextLine) {
        Map<String, String> params = new HashMap<String, String>();
        for (int i = 0; i < header.length; i++) {
            String columnName = header[i];
            params.put(columnName, nextLine[i]);
        }
        return params;
    }

}
