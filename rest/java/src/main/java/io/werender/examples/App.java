package io.werender.examples;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.openapitools.client.ApiClient;
import org.openapitools.client.Configuration;
import org.openapitools.client.model.StorageFile;

import okhttp3.OkHttpClient;
import okhttp3.logging.HttpLoggingInterceptor;

public class App {
    private static Log log = LogFactory.getLog(App.class);

    private static final String APP_NAME = "werender-example-rest-java";

    private static final String COMMAND_UPLOAD_FILE = "upload_file";
    private static final String COMMAND_HELP = "help";

    public static void handleUploadFile(CommandLine cmdLine) {
	// Retrieve configuration.
	Config config = Config.create();
	log.info(String.format("Using server %s", config.getAddress()));

	// Create API client.
	ApiClient apiClient = Configuration.getDefaultApiClient();
	apiClient.setBasePath(config.getAddress());
	apiClient.setUserAgent("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15.7) WeRender/0.4.0");

	OkHttpClient client = new OkHttpClient.Builder()
		.addInterceptor(new SignatureInterceptor(config.getPublicKey(), config.getPrivateKey()))
		.addInterceptor(new HttpLoggingInterceptor()).build();
	apiClient.setHttpClient(client);

	// Upload the local file to remote directory.
	try {
	    // Get local file path and remote directory path.
	    String[] optionValues = cmdLine.getOptionValues(COMMAND_UPLOAD_FILE);
	    String localFilePath = optionValues[0];
	    String remoteDirPath = optionValues[1];
	    log.info(String.format("Start to upload file from %s to %s", localFilePath, remoteDirPath));

	    // Create command to do the actual work.
	    CommandContext commandContext = new CommandContext(apiClient);
	    UploadFileCommand command = new UploadFileCommand(localFilePath, remoteDirPath);
	    StorageFile file = command.execute(commandContext);

	    log.info(String.format("Uploaded file from %s to %s with id %s", localFilePath, remoteDirPath,
		    file.getId()));
	} catch (Exception e) {
	    e.printStackTrace();
	}
    }

    public static void handleHelp(Options options) {
	HelpFormatter formatter = new HelpFormatter();
	formatter.printHelp(APP_NAME, options);
    }

    public static void main(String[] args) {
	// Prepare command line options.
	Option uploadFileOption = Option.builder(COMMAND_UPLOAD_FILE).hasArgs()
		.desc("upload a file from local path to remote directory").build();
	Option helpOption = Option.builder(COMMAND_HELP).desc("print help").build();

	Options options = new Options();
	options.addOption(uploadFileOption);
	options.addOption(helpOption);

	// Process command line.
	try {
	    CommandLineParser parser = new DefaultParser();
	    CommandLine cmdLine = parser.parse(options, args);
	    if (cmdLine.hasOption(COMMAND_HELP)) {
		handleHelp(options);
	    } else if (cmdLine.hasOption(COMMAND_UPLOAD_FILE)) {
		handleUploadFile(cmdLine);
	    } else {
		handleHelp(options);
	    }
	} catch (Exception e) {
	    System.out.println(e.getMessage());
	}
    }
}
