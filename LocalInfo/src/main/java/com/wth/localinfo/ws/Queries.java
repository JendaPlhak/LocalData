package com.wth.localinfo.ws;

import java.util.Iterator;
import java.util.Set;

import com.wth.localinfo.model.MappedParams;

/**
 * 
 * Queries helper.
 *
 */
public class Queries {

    private final static String TABLE_NAME = "wth_table_ws_filled";

    private final static String COLUMN_LAT = "lat";

    private final static String COLUMN_LON = "lon";

    private final static String COLUMN_GEOM_NAME = "the_geom";

    private final static String COLUMN_PRIMARY_KEY = "cartodb_id";

    public static String getTableSelect() {
        return "q=SELECT+*+FROM+" + TABLE_NAME + "&api_key=d05fa756f999fc42852c6513cee04a29386dd87d";
    }

    public static String getInsertMockedDataRow() {
        return "q=INSERT+INTO+" + TABLE_NAME
                + "(the_geom,lon,lat,description)VALUES(ST_GeomFromText('POINT(14.4373283642+50.0848113671)',4326),50.0848113671,14.4373283642,'api_inserted')&api_key=d05fa756f999fc42852c6513cee04a29386dd87d";
    }

    public static String getInsertRow(MappedParams params) {
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
                // String insertedValue = columnValue.isEmpty() ? "''" :
                // columnValue;
                String insertedValue = columnValue;
                valuesBuilder.append("'" + insertedValue + "'");
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
        return query.toString() + "&api_key=d05fa756f999fc42852c6513cee04a29386dd87d";
    }

}
