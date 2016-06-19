package com.wth.localinfo.ws;

import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.util.Iterator;
import java.util.Set;

import com.sun.jersey.api.representation.Form;
import com.wth.localinfo.model.MappedParams;

/**
 * 
 * Queries helper.
 *
 */
public class Queries {

    protected final static String TABLE_NAME = "wth_table_ws_filled_2_copy2";

    private final static String COLUMN_LAT = "lat";

    private final static String COLUMN_LON = "lon";

    private final static String COLUMN_GEOM_NAME = "the_geom";

    private final static String COLUMN_PRIMARY_KEY = "cartodb_id";

    private final static String API_KEY = "api_key";

    private final static String API_KEY_VALUE = "d05fa756f999fc42852c6513cee04a29386dd87d";

    private final static String QUERY_KEY = "q";

    public static String getURLParams(MappedParams params) throws UnsupportedEncodingException {
        String query = createURLQueryParam(params);
        return query + "&api_key=d05fa756f999fc42852c6513cee04a29386dd87d";
    }

    public static Form getFormParams(MappedParams params) throws UnsupportedEncodingException {
        Form form = new Form();
        form.add(QUERY_KEY, createFormQueryParam(params));
        form.add(API_KEY, API_KEY_VALUE);
        return form;
    }

    private static String createURLQueryParam(MappedParams params) throws UnsupportedEncodingException {
        StringBuilder query = new StringBuilder("q=INSERT+INTO+" + TABLE_NAME);
        StringBuilder columnsBuilder = new StringBuilder();
        StringBuilder valuesBuilder = new StringBuilder();
        Set<String> columns = params.keySet();

        for (Iterator<String> iterator = columns.iterator(); iterator.hasNext();) {
            String column = iterator.next();
            boolean skipColumn = false;
            switch (column) {
            case COLUMN_PRIMARY_KEY:
                skipColumn = true;
                break;
            case COLUMN_GEOM_NAME:
                columnsBuilder.append(column);
                valuesBuilder.append(
                        "ST_GeomFromText('POINT(" + params.get(COLUMN_LON) + "+" + params.get(COLUMN_LAT) + ")',4326)");
                break;
            default:
                columnsBuilder.append(column);
                String columnValue = params.get(column);
                valuesBuilder.append("'" + URLEncoder.encode(columnValue, "UTF8") + "'");
                break;
            }

            if (skipColumn) {
                continue;
            }
            if (iterator.hasNext()) {
                columnsBuilder.append(",");
                valuesBuilder.append(",");
            }
        }

        query.append("(");
        query.append(columnsBuilder.toString());
        query.append(")");
        query.append("VALUES");
        query.append("(");
        query.append(valuesBuilder.toString());
        query.append(")");
        return query.toString();
    }

    // TODO simplify both params-oriented methods.

    private static String createFormQueryParam(MappedParams params) throws UnsupportedEncodingException {
        StringBuilder query = new StringBuilder("INSERT INTO " + TABLE_NAME);
        StringBuilder columnsBuilder = new StringBuilder();
        StringBuilder valuesBuilder = new StringBuilder();
        Set<String> columns = params.keySet();

        for (Iterator<String> iterator = columns.iterator(); iterator.hasNext();) {
            String column = iterator.next();
            boolean skipColumn = false;
            switch (column) {
            case COLUMN_PRIMARY_KEY:
                skipColumn = true;
                break;
            case COLUMN_GEOM_NAME:
                columnsBuilder.append(column);
                valuesBuilder.append(
                        "ST_GeomFromText('POINT(" + params.get(COLUMN_LON) + " " + params.get(COLUMN_LAT) + ")',4326)");
                break;
            default:
                columnsBuilder.append(column);
                String columnValue = params.get(column);
                valuesBuilder.append("'" + columnValue + "'");
                break;
            }

            if (skipColumn) {
                continue;
            }
            if (iterator.hasNext()) {
                columnsBuilder.append(",");
                valuesBuilder.append(",");
            }
        }

        query.append("(");
        query.append(columnsBuilder.toString());
        query.append(")");
        query.append("VALUES");
        query.append("(");
        query.append(valuesBuilder.toString());
        query.append(")");
        return query.toString();
    }

}
