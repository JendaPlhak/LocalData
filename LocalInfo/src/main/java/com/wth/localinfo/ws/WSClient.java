package com.wth.localinfo.ws;

import java.net.URI;

import com.sun.jersey.api.client.Client;
import com.sun.jersey.api.client.ClientResponse;
import com.sun.jersey.api.client.WebResource;

/**
 * 
 * Sends provided parameters to defined web service.
 *
 */
public class WSClient {

    private final String mEndpoint = "https://localinfo.cartodb.com/api/v2/sql";

    public void sendRequest(String parameters) {
        try {
            Client client = Client.create();
            // URI urlEncoded = new URI(endpoint +"?"+
            // URLEncoder.encode(parameters , "UTF8" ));
            URI urlEncoded = new URI(mEndpoint + "?" + parameters);
            System.out.println(urlEncoded);
            WebResource webResource = client.resource(urlEncoded);

            ClientResponse response = webResource.accept("application/json").get(ClientResponse.class);

            if (response.getStatus() != 200) {
                throw new RuntimeException("Failed : HTTP error code : " + response.getStatus());
            }

            String output = response.getEntity(String.class);

            System.out.println("Output from Server...");
            System.out.println(output);

        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}
