package io.werender.examples;

import org.openapitools.client.ApiClient;
import org.openapitools.client.api.StorageApi;

public class CommandContext {

    private ApiClient apiClient;
    private StorageApi storageApi;

    public CommandContext(ApiClient apiClient) {
	this.apiClient = apiClient;
	storageApi = new StorageApi(apiClient);
    }

    public ApiClient getApiClient() {
	return apiClient;
    }

    public StorageApi getStorageApi() {
	return storageApi;
    }

}
