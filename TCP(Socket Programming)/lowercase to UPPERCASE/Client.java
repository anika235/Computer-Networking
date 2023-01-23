
// A Java program for a Client
import java.io.*;
import java.net.*;
import java.util.Scanner;

public class Client {
    // initialize socket and input output streams
    private Socket socket = null;
    private Socket socketout = null;
    private ServerSocket server = null;
    private DataInputStream input = null;
    private DataOutputStream out = null;
    private DataInputStream in = null;

    // constructor to put ip address and port
    public Client(String address, int port) {
        Scanner scanner = new Scanner(System.in);
        // establish a connection
        try {
            server = new ServerSocket(5000);
            socket = new Socket(address, port);
            System.out.println("Connected");
            socketout = server.accept();

            // takes input from terminal
            input = new DataInputStream(System.in);

            // sends output to the socket
            out = new DataOutputStream(
                    socket.getOutputStream());
            in = new DataInputStream(socketout.getInputStream());
        } catch (UnknownHostException u) {
            System.out.println(u);
            return;
        } catch (IOException i) {
            System.out.println(i);
            return;
        }

        // string to read message from input
        String line = "Hello";

        // keep reading until "Over" is input
        while (true) {
            try {
                line = input.readLine();
                out.writeUTF(line);
                line = in.readUTF();
                System.out.println(line);

            } catch (IOException i) {
                System.out.println(i);
                break;
            }
        }

        // close the connection
        try {
            input.close();
            out.close();
            socket.close();
        } catch (IOException i) {
            System.out.println(i);
        }
    }

    public static void main(String args[])
    {
        Client client = new Client("10.33.2.89", 5000);
    }
}