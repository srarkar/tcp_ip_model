import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.net.*;
import javax.swing.*;

public class SwingClient extends JFrame {
    private JTextArea displayArea;
    private JTextField inputField;
    private JButton sendButton;

    private Socket socket;
    private PrintWriter out;
    private BufferedReader in;

    private static final int WINDOW_WIDTH = 600;
    private static final int WINDOW_HEIGHT = 400;

    public SwingClient(String host, int port) {
        setTitle("Telnet Swing Client");
        setSize(WINDOW_WIDTH, WINDOW_HEIGHT);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        displayArea = new JTextArea();
        displayArea.setEditable(false);
        JScrollPane scrollPane = new JScrollPane(displayArea);

        inputField = new JTextField();
        sendButton = new JButton("Send");

        JPanel inputPanel = new JPanel(new BorderLayout());
        JLabel promptLabel = new JLabel("> ");  // prompt as part of input field
        inputPanel.add(promptLabel, BorderLayout.WEST);
        inputPanel.add(inputField, BorderLayout.CENTER);
        inputPanel.add(sendButton, BorderLayout.EAST);

        add(scrollPane, BorderLayout.CENTER);
        add(inputPanel, BorderLayout.SOUTH);

        // attempt server connection
        try {
            socket = new Socket(host, port);
            out = new PrintWriter(socket.getOutputStream(), true);
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            // create thread for server response
            Thread readerThread = new Thread(() -> {
                try {
                    String line;
                    while ((line = in.readLine()) != null) {
                        displayArea.append(line + "\n");

                        // If server says goodbye, close client as well
                        if (line.contains("Thanks for using the telnet server!")) {
                            try {
                                socket.close();
                            } catch (IOException ignored) {}
                            SwingUtilities.invokeLater(() -> {
                                JOptionPane.showMessageDialog(this, "Server closed connection. Goodbye!");
                                dispose(); // closes Swing window
                                System.exit(0);
                            });
                            break;
                        }
                    }
                } catch (IOException e) {
                    displayArea.append("Disconnected from server.\n");
                    SwingUtilities.invokeLater(() -> {
                        dispose();
                        System.exit(0);
                    });
                }
            });
            readerThread.start();

        } catch (IOException e) {
            JOptionPane.showMessageDialog(this, "Could not connect to server: " + e.getMessage(),
                    "Connection Error", JOptionPane.ERROR_MESSAGE);
            System.exit(1);
        }

        // Send action (button or enter key)
        ActionListener sendAction = e -> {
            String text = inputField.getText().trim();
            if (!text.isEmpty()) {
                out.println(text);
                inputField.setText("");
            }
        };

        sendButton.addActionListener(sendAction);
        inputField.addActionListener(sendAction);

        setVisible(true);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new SwingClient("localhost", 8080));
    }
}
