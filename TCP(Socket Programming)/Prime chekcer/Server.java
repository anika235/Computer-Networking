// A Java program for a Server
import java.net.*;
import java.io.*;

public class Server
{
    //initialize socket and input stream
    private Socket		 socket = null;
    private ServerSocket server = null;
    private Socket       socketsent = null;
    private DataInputStream in	 = null;
    private DataOutputStream out = null;
    private int traxid ;
    // constructor with port
    public Server(int port)
    {
        // starts server and waits for a connection
        traxid = 10000414;
        try
        {
            //10.33.2.89
            server = new ServerSocket(port);
            System.out.println("Server started");

            System.out.println("Waiting for a client ...");

            socket = server.accept();
            System.out.println("Client accepted");
            socketsent = new Socket("10.33.2.90",5000);

            // takes input from the client socket
            in = new DataInputStream(
                    new BufferedInputStream(socket.getInputStream()));
            out = new DataOutputStream(
                    socketsent.getOutputStream());

            String line = "";

            // reads message from client until "Over" is sent
            while (true)
            {
                try
                {

                    line = in.readUTF();
                    //prime checker
                    System.out.println(line);
                    int x = new Integer(line);
                    boolean ok = false;
                    for(int i=2;i*i<=x;i++)
                    {
                        if(x%i==0)
                        {
                            ok = true;
                        }
                    }
                    if(ok)
                    {
                        out.writeUTF("Not Prime");
                    }
                    else
                    {
                        out.writeUTF("Prime");
                    }

                }
                catch(IOException i) {
                    System.out.println(i);
                    break;
                }
            }
            System.out.println("Closing connection");
            // close connection
            socket.close();
            socketsent.close();
            in.close();
            out.close();
        }
        catch(IOException i)
        {
            System.out.println(i);
        }
    }

    public static void main(String args[])
    {
        Server server = new Server(5000);
    }
}
