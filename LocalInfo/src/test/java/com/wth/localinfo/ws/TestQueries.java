package com.wth.localinfo.ws;

public class TestQueries extends Queries {

    public static String getTableSelect() {
        return "q=SELECT+*+FROM+" + TABLE_NAME + "&api_key=d05fa756f999fc42852c6513cee04a29386dd87d";
    }

    public static String getInsertMockedDataRow() {
        return "q=INSERT+INTO+" + TABLE_NAME
                + "(the_geom,lon,lat)VALUES(ST_GeomFromText('POINT(14.4373283642+50.0848113671)',4326),50.0848113671,14.4373283642)&api_key=d05fa756f999fc42852c6513cee04a29386dd87d";
    }

}
