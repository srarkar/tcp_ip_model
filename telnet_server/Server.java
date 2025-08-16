import java.io.*;
import java.net.*;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;

// used for math expression evaluation (ignore red squigglies)
import net.objecthunter.exp4j.Expression;
import net.objecthunter.exp4j.ExpressionBuilder;

// used for parsing Wikipedia REST API (more red squigglies -- don't worry!)
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;


/// Compile: javac -cp lib/exp4j-0.4.8.jar Server.java
/// Build JAR file: jar cfm Server.jar MANIFEST.MF Server.class lib/exp4j-0.4.8.jar
/// Run JAR file: java -jar Server.jar
/// oooooor just `make run` silly

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
                    String result = execute_command(tokens[0], response);
                    
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

    private static String arg_handler_helper(String response, int cmdLength, String usageHint) {
        if (response.length() <= cmdLength) return usageHint;

        String args = response.substring(cmdLength).trim();
        if (args.isEmpty()) return usageHint;

        return args;
    }

    private static String execute_command(String command, String response) {
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
            case "/weather" -> result = weather_handler(response);
            default -> result = "Unknown command: " + command;
        }
        return result;
    }

    private static String echo_handler(String response) {
        return arg_handler_helper(response, 6, "");

    }

    private static String math_handler(String response) {
        String expression = arg_handler_helper(response, 6, "Please provide an expression, e.g., /math 2 + 2");
        if (expression.startsWith("Please")) return expression; // returns usage hint

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
        String query = arg_handler_helper(response, 6, "Please specify a topic to search, e.g., /wiki Albert Einstein");
        if (query.startsWith("Please")) return query;
        query = query.replace(' ', '_');

        try {
            String urlStr = "https://en.wikipedia.org/api/rest_v1/page/summary/" + URLEncoder.encode(query, "UTF-8");
            HttpURLConnection conn = (HttpURLConnection) 
                new URI(urlStr).toURL().openConnection();
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
            return "Wikipedia API failed for query: " + query + " due to: " + e.getMessage();
        }
    }


    private static String weather_handler(String response) {
        String location = arg_handler_helper(response, 9, "Please specify a location, e.g., /weather Paris");
        if (location.startsWith("Please")) return location;

        StringBuilder result = new StringBuilder();
        try {
            // Correct format string with necessary details for readability
            String format = "%l: %c %t, feels:%f, humidity:%h, wind:%w%s, moon:%m";
            
            // Encode the location and format string for the URL
            String encodedLocation = URLEncoder.encode(location, StandardCharsets.UTF_8);
            String encodedFormat = URLEncoder.encode(format, StandardCharsets.UTF_8);
            
            String urlStr = "https://wttr.in/" + encodedLocation + "?format=" + encodedFormat;

            HttpURLConnection conn = (HttpURLConnection) new URI(urlStr).toURL().openConnection();
            conn.setRequestMethod("GET");

            try (BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    result.append(line);
                }
            }

            return result.toString();
        } catch (Exception e) {
            return "Weather lookup failed for location: " + location + " due to: " + e.getMessage();
        }
    }



}


