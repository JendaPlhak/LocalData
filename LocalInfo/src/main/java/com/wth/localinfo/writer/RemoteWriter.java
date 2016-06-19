package com.wth.localinfo.writer;

import java.io.IOException;
import java.util.List;

import com.wth.localinfo.model.MappedParams;
import com.wth.localinfo.ws.Queries;
import com.wth.localinfo.ws.WSClient;

/**
 * {@link RemoteWriter} writes provided rows data via given {@link WSClient}.
 */
public class RemoteWriter {

    private final WSClient mWS;

    public RemoteWriter(WSClient mWS) {
        super();
        this.mWS = mWS;
    }

    public void remoteWrite(List<MappedParams> rowsWithParams) throws IOException {
        for (MappedParams rowMap : rowsWithParams) {
            mWS.sendRequest(Queries.getInsertRow(rowMap));
        }
    }

}
