import java.io.File;
import java.util.ArrayList;
import java.util.List;
import org.jaudiotagger.audio.AudioFile;
import org.jaudiotagger.audio.AudioFileIO;
import org.jaudiotagger.tag.FieldKey;
import org.jaudiotagger.tag.Tag;

/**
 * MusicLibraryManager
 */
public class MusicLibraryManager {
    private static final String INPUT = "--input";
    private static final String LIST_FILES = "--list-files";
    private static final String SHOW_METADATA = "--show-metadata";

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
        if (command.equals(SHOW_METADATA)) {
            handleMetadata(directoryPath);
        }

        System.err.println("Invalid command: " + command);
        System.exit(1);
    }

    private static void handleMetadata(String directoryPath) {
        File directory = new File(directoryPath);

        List<String> fileList = new ArrayList<>();
        listFiles(directory, fileList, directoryPath);

        for (String filePath : fileList) {
            File file = new File(directory, filePath);
            try {
                AudioFile audioFile = AudioFileIO.read(file);
                Tag tag = audioFile.getTag();
                if (tag != null) {
                    System.out.println("____________________");
                    System.out.println("File: " + filePath);
                    System.out.println("Song: " + tag.getFirst(FieldKey.TITLE));
                    System.out.println("Artist: " + tag.getFirst(FieldKey.ARTIST));
                    System.out.println("Album: " + tag.getFirst(FieldKey.ALBUM));
                } else {
                    System.out.println("____________________");
                    System.out.println("File: " + filePath);
                    System.out.println("Metadata not available");
                }
            } catch (Exception e) {
                System.out.println("____________________");
                System.out.println("File: " + filePath);
                System.out.println("Error reading metadata: " + e.getMessage());
            }
        }
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