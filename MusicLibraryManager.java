import java.io.File;
import java.util.ArrayList;
import java.util.List;

/**
 * MusicLibraryManager
 */
public class MusicLibraryManager {
    private static final String INPUT = "--input";
    private static final String LIST_FILES = "--list-files";

    public static void main(String[] args) {
        if (args.length < 3) {
            System.err.println("Not enough arguments.");
            System.exit(1);
        }

        String inputCommand = args[0];
        if (!inputCommand.equals(INPUT)) {
            System.err.println("Invalid argument: " + inputCommand);
            System.exit(1);
        }

        String directoryPath = args[1];
        String command = args[2];

        if (command.equals(LIST_FILES)) {
            handleListFiles(directoryPath);
            return;
        }

        System.err.println("Invalid command: " + command);
        System.exit(1);
    }

    private static void handleListFiles(String directoryPath) {
        File directory = new File(directoryPath);
        if (!directory.isDirectory()) {
            System.err.println("Error: " + directoryPath + " is not a valid directory");
            System.exit(1);
        }

        List<String> fileList = new ArrayList<>();
        listFiles(directory, fileList, directoryPath);

        for (String filePath : fileList) {
            System.err.println(filePath);
        }
    }

    private static void listFiles(File directory, List<String> fileList, String basePath) {
        File[] files = directory.listFiles();
        if (files == null) {
            return;
        }

        for (File file : files) {
            if (file.isDirectory()) {
                listFiles(file, fileList, basePath);
                return;
            }

            String fileName = file.getName().toLowerCase();
            if (!fileName.endsWith(".mp3")) {
                return;
            }
            fileList.add(file.getPath().substring(basePath.length()));
        }
    }
}