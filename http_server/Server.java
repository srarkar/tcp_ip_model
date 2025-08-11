// 1. Setup Phase
// Define port number (e.g., 8080).

// Create a ServerSocket bound to that port.

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