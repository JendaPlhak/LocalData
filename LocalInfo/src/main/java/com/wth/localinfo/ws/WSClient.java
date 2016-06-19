package com.wth.localinfo.ws;

import java.net.URI;
import java.net.URISyntaxException;

import javax.ws.rs.core.MediaType;

import com.sun.jersey.api.client.Client;
import com.sun.jersey.api.client.ClientResponse;
import com.sun.jersey.api.client.WebResource;
import com.sun.jersey.api.representation.Form;

/**
 * 
 * {@link WSClient} sends provided parameters to defined web service.
 *
 */
public class WSClient {

    private final String mEndpointAddress = "https://localinfo.cartodb.com/api/v2/sql";

    public void sendPostRequest(Form parameters) {
        WebResource webResource = initWebResource(mEndpointAddress);
        String type = MediaType.APPLICATION_FORM_URLENCODED;
        ClientResponse response = webResource.accept(type).post(ClientResponse.class, parameters);
        processResponse(response);
    }

    public void sendGetRequest(String parameters) {
        URI urlEncoded = null;
        try {
            urlEncoded = new URI(mEndpointAddress + "?" + parameters);
        } catch (URISyntaxException e) {
            throw new IllegalArgumentException(e);
        }
        WebResource webResource = initWebResource(urlEncoded.toString());
        ClientResponse response = webResource.accept("application/json").get(ClientResponse.class);
        processResponse(response);
    }

    private WebResource initWebResource(String url) {
        System.out.println(url);
        WebResource webResource = Client.create().resource(url);
        return webResource;
    }

    private void processResponse(ClientResponse response) {
        if (response.getStatus() != 200) {
            throw new RuntimeException("Failed : HTTP error code : " + response.getStatus());
        }

        String output = response.getEntity(String.class);
        System.out.println("Output from Server...");
        System.out.println(output);
    }
}
