import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.charset.Charset;

public class Server {
    // alternate HTTP port
    public static final int PORT = 8080;
    public static void main(String[] args) {

        // Create a ServerSocket bound to alternate HTTP port
        try(ServerSocket serverSocket = new ServerSocket(PORT)) {
            System.out.println("Server started on port " + PORT);

            while(true) {
                try (Socket clientSocket = serverSocket.accept()) { // block until a client connects
                    System.out.println("Client conneced from: " + clientSocket.getInetAddress());
                    // this will read what the client sends as raw bytes
                    InputStream inStream = clientSocket.getInputStream();
                    // this will decode raw bytes into characters via a specified charset
                    InputStreamReader inStreamReader = new InputStreamReader(inStream, Charset.forName("UTF-8"));
                    // improve efficiency -- speeds up IO by reading larger blocks at a time
                    BufferedReader inBuffReader = new BufferedReader(inStreamReader);
                    // read input stream until a blank line is hit
                    String response = inBuffReader.readLine();
                    System.out.println(response);
                    /// TODO: add outputStream to respond to server to prevent curl 52 errors


                } catch (IOException e) {
                    System.err.println("Error accepting client connection: " + e.getMessage());
                }
            }
            
        } catch (IOException e) {
            System.err.println("Could not start server on port " + PORT + ": " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
        System.exit(0);
        
    }
}


// 1. Declare and connect to a port (such as 8080)
// Print a message so you know the server is running.

// 2. Main Loop (Accepting Connections)
// Continuously:

// Call accept() on the ServerSocket to block until a client connects.

// Get the Socket object representing that client connection.

// 3. Read HTTP Request
// Create an input stream from the Socket.

// Wrap it in something that allows line-by-line reading (for HTTP headers).

// Read the request line (e.g., GET / HTTP/1.1).

// Read the HTTP headers until you hit a blank line (end of headers).

// (Optional) If it’s a POST or PUT, read the body based on Content-Length.

// 4. Prepare HTTP Response
// Decide on a status code (200 OK, 404 Not Found, etc.).

// Set headers: Content-Type, Content-Length, etc.

// Create a body (HTML, plain text, JSON — whatever you’re serving).

// Concatenate headers + a blank line + body into a complete HTTP response.

// 5. Send Response
// Write the response bytes to the Socket output stream.

// Flush to ensure all data is sent.

// 6. Close Connection
// Close the Socket for this client (but keep the ServerSocket open to accept new ones).

// Go back to Step 2 for the next client.

// 7. Exit Handling
// If you ever break out of the loop, close the ServerSocket.

// Optionally handle IOException for network errors.
// put whole thing in try-catch block?? or is there a better way