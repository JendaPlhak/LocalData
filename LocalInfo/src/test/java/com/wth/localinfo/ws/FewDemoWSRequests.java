package com.wth.localinfo.ws;

public class FewDemoWSRequests {

    public static void main(String[] args) {
        WSClient wsClient = new WSClient();
        wsClient.sendGetRequest(TestQueries.getInsertMockedDataRow());
        wsClient.sendGetRequest(TestQueries.getTableSelect());
    }

}
