import java.io.*;
import java.net.*;
import java.nio.charset.Charset;
public class Server {
    // alternate HTTP port
    public static final int PORT = 8080;
    public static void main(String[] args) {

        // Create a ServerSocket bound to alternate HTTP port
        try(ServerSocket serverSocket = new ServerSocket(PORT)) {
            System.out.println("Telnet server started on port " + PORT);
            System.out.println("Connect via: telnet localhost " + PORT);
            System.out.println("Type CTRL-C at any point to kill.");

            // main loop
            while(true) {
                Socket clientSocket = serverSocket.accept();
                System.out.println("Client connected from: " + clientSocket.getInetAddress());
                // this will read what the client sends as raw bytes
                InputStream inStream = clientSocket.getInputStream();
                // this will decode raw bytes into characters via a specified charset
                InputStreamReader inStreamReader = new InputStreamReader(inStream, Charset.forName("UTF-8"));
                // improve efficiency -- speeds up IO by reading larger blocks at a time
                BufferedReader inBuffReader = new BufferedReader(inStreamReader);
                
                // do the same for output to client
                OutputStream outputStream = clientSocket.getOutputStream();
                OutputStreamWriter outWriter = new OutputStreamWriter(outputStream, Charset.forName("UTF-8"));
                PrintWriter outPrinter = new PrintWriter(outWriter, true);
                
                // welcome client
                outPrinter.println("Welcome to this telnet server.");
                outPrinter.println("Type \'exit\' to disconnect.");
                outPrinter.print("> ");
                outPrinter.flush();

                // read client input
                String response;
                while ((response = inBuffReader.readLine()) != null) {
                    System.out.println("Client sent: " + response);
                    if (response.equalsIgnoreCase("exit")) {
                        outPrinter.println("Thank you, and goodye.");
                        System.out.println("Client exited.");
                        break;
                    }
                    outPrinter.println("You said: " + response);
                    outPrinter.print("> ");
                    outPrinter.flush();
                }
            }
            
        } catch (IOException e) {
            System.err.println("Could not start server on port " + PORT + ": " + e.getMessage());
            e.printStackTrace(System.out);
            System.exit(1);
        }
        System.exit(0);
    }

    private static String[] parse_args(String args) {
        return new String[]{};
    }


    private static String echo_handler(String args) {
        return "";
    }

    private static String math_handler(String args) {
        return "";
    }

    private static String wiki_handler(String args) {
        return "";
    }

    private static String weather_handler(String args) {
        return "";
    }


}


