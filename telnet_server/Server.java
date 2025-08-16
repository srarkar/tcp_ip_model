import java.io.*;
import java.net.*;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;

// used for math expression evaluation
import net.objecthunter.exp4j.Expression;
import net.objecthunter.exp4j.ExpressionBuilder;

// used for parsing Wikipedia REST API
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

// notes for exp4j:
// available constants: π/"pi", e the value of Euler's number e, and φ (type "phi") the value of the golden ratio (1.61803398874)
// scientific notation, implicit multiplication
// builtin operators:
    // Addition: 2 + 2
    // Subtraction: 2 - 2
    // Multiplication: 2 * 2
    // Division: 2 / 2
    // Exponentation: 2 ^ 2
    // Unary Minus,Plus (Sign Operators): +2 - (-2)
    // Modulo: 2 % 2



/// Compile: javac -cp lib/exp4j-0.4.8.jar Server.java
/// Build JAR file: jar cfm Server.jar MANIFEST.MF Server.class lib/exp4j-0.4.8.jar
/// Run JAR file: java -jar Server.jar

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
                System.out.println("Client connected from: " + clientSocket.getInetAddress().getHostAddress());
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
                    if (response.equalsIgnoreCase("exit")) {
                        outPrinter.println("Thanks for using the telnet server! - RS.");
                        System.out.println("Client exited.");
                        clientSocket.close();
                        break;
                    }
                    String[] tokens = parse_args(response);
                    String result = execute_command(tokens[0], tokens, response);
                    
                    // update server display
                    System.out.println("Client sent: " + response);
                    System.out.println("Output: " + result);

                    // reply to client
                    outPrinter.println(result);
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

    private static String[] parse_args(String response) {
        String[] tokens = response.split("\\s+");
        return tokens;
    }

    private static String execute_command(String command, String[] args, String response) {
        String result;
        // check if first token is a command 
        if (command.charAt(0) != '/') {
            result = "You said: " + response;
            return result;
        }

        switch (command) {
            case "/echo" -> result = echo_handler(response);
            case "/math" -> result = math_handler(response);
            case "/wiki" -> result = wiki_handler(response);
            case "/weather" -> result = weather_handler(args);
            default -> result = "Unknown command: " + command;
        }
        return result;
    }

    // TODO: implement and test all handlers
    // TODO: brainstorm additional if time
    private static String echo_handler(String response) {
        // "/echo " is 6 chars
        return response.substring(6);
    }

    private static String math_handler(String response) {
        // "/math " is 6 chars
        String expression = response.substring(6);
        try {
            Expression e = new ExpressionBuilder(expression).variable("phi")
                                                                .build()
                                                                .setVariable("phi", 1.61803398874); // UTC-8 
            double res = e.evaluate();
            return Double.toString(res);
        } catch (Exception e) {
            return ("Invalid math expression: " + expression);
        } 
    }

    private static String wiki_handler(String response) {
        // "/wiki " is 6 chars
        String query = response.substring(6);
        try {
            String urlStr = "https://en.wikipedia.org/api/rest_v1/page/summary/" + URLEncoder.encode(query, "UTF-8");
            HttpURLConnection conn = (HttpURLConnection) new URL(urlStr).openConnection();
            conn.setRequestMethod("GET");

            StringBuilder json;
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {
                json = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    json.append(line);
                }
            }

            // parse JSON using Gson
            JsonObject obj = JsonParser.parseString(json.toString()).getAsJsonObject();
            if (obj.has("extract")) {
                return obj.get("extract").getAsString();
            } else {
                return "No summary found for: " + query;
            }
        } catch (Exception e) {
            return "Wikipedia API failed for query: " + query + "due to: " + e.getMessage();
        }
    }


    private static String weather_handler(String[] args) {
        return "pip pip cheerio, how's the weathuh";
    }


}


