package io.werender.examples;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

import org.openapitools.client.model.StorageChunk;
import org.openapitools.client.model.StorageFile;
import org.openapitools.client.model.StorageFileCreate200Response;
import org.openapitools.client.model.StorageFileCreateRequest;
import org.openapitools.client.model.StorageFileFinalizeRequest;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class UploadFileCommand implements Command<StorageFile> {

    private String localFilePath;
    private String remoteDirPath;

    public UploadFileCommand(String localFilePath, String remoteDirPath) {
	this.localFilePath = localFilePath;
	this.remoteDirPath = remoteDirPath;
    }

    @Override
    public StorageFile execute(CommandContext context) throws Exception {
	// Calculate file checksum.
	File localFile = Paths.get(localFilePath).toFile();
	String localFileChecksum = FileUtil.computeFileChecksum(localFile);
	String localFileContentType = FileUtil.getContentType(localFilePath);

	String localFileName = Paths.get(localFilePath).getFileName().toString();
	String remoteFilePath = Paths.get(remoteDirPath, localFileName).toString();

	// Create file.
	StorageFileCreateRequest createReq = new StorageFileCreateRequest();
	createReq.setChecksum(localFileChecksum);
	createReq.setContentType(localFileContentType);
	createReq.setMode(FileUtil.MODE_UNIQUE);
	createReq.setPath(remoteFilePath);
	createReq.setSize(Files.size(Paths.get(localFilePath)));
	StorageFileCreate200Response createRes = context.getStorageApi().storageFileCreate(createReq);

	// Get file.
	StorageFileFinalizeRequest getReq = new StorageFileFinalizeRequest();
	getReq.setId(createRes.getId());
	StorageFile file = context.getStorageApi().storageFileGet(null, getReq);

	// Upload file if there is no data.
	long fileFinalizedAt = file.getFinalizedAt();
	if (fileFinalizedAt == 0) {
	    InputStream fileStream = new FileInputStream(Paths.get(localFilePath).toFile());

	    OkHttpClient httpClient = new OkHttpClient();
	    List<StorageChunk> chunks = createRes.getChunks();
	    for (StorageChunk chunk : chunks) {
		Long chunkSize = chunk.getSize();
		byte[] chunkData = fileStream.readNBytes(chunkSize.intValue());
		String chunkUrl = chunk.getUrl();
		Request chunkReq = new Request.Builder().url(chunkUrl)
			.addHeader("Content-Type", FileUtil.CONTENT_TYPE_BINARY).put(RequestBody.create(chunkData))
			.build();
		Response chunkRes = httpClient.newCall(chunkReq).execute();
		if (!chunkRes.isSuccessful()) {
		    return null;
		}
	    }

	    // Finalize file.
	    file = context.getStorageApi().storageFileFinalize(getReq);
	}

	// Return file.
	return file;
    }
}
