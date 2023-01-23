
        // A Java program for a Client
        import java.io.*;
        import java.net.*;
        import java.security.spec.RSAOtherPrimeInfo;
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
        String line , line2, line3;

        // keep reading until "Over" is input
        while (true) {
            try {
                System.out.println("Enter Username:");
                line = input.readLine();
                out.writeUTF(line);

                System.out.println("Enter Password:");
                line2 = input.readLine();
                out.writeUTF(line2);

                line3 = in.readUTF();
                if(line3.equals("ok"))
                {
                    System.out.println("Proceed");
                    int choose;
                    do
                    {
                        System.out.println("Press 1 for Check balance\nPress 2 for Credit balance\nPress 3 for debit balance\nPress 0 for exit");
                        choose = scanner.nextInt();
                        //System.out.println(choose);
                        if(choose ==1 )
                        {
                            out.writeUTF("1");
                            line = in.readUTF();
                            System.out.println(line);
                        }
                        if(choose ==2)
                        {
                            out.writeUTF("2");
                            String money = input.readLine();
                            out.writeUTF(money);
                            line = in.readUTF();
                            if(line.equals("1"))
                            {
                                line = in.readUTF();
                                System.out.println(line);
                                System.out.println("Your transection is successful");
                            }
                            else {
                                System.out.println("insufficient balance");
                            }

                        }

                        if(choose ==3)
                        {
                            out.writeUTF("3");
                            String money = input.readLine();
                            out.writeUTF(money);
                            line = in.readUTF();
                            if(line.equals("1"))
                            {
                                line = in.readUTF();
                                System.out.println(line);
                                System.out.println("Your transection is successful");
                            }
                        }

                    }
                    while (choose!=0);
                }
                else System.out.println("Invalid username or password");

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
