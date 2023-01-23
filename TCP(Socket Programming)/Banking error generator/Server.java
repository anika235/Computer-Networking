// A Java program for a Server
import java.net.*;
import java.io.*;
import java.util.Random;

public class Server
{
    //initialize socket and input stream
    private Socket		 socket = null;
    private ServerSocket server = null;
    private Socket       socketsent = null;
    private DataInputStream in	 = null;
    private DataOutputStream out = null;
    int clientid , myid ;

    // constructor with port
    public Server(int port)
    {
        // starts server and waits for a connection
        try
        {
            //10.33.2.89
            myid = 345239;
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

            Person [] person =  new Person[4];
            person[0] = new Person("Olin" ,"olinone","123456", 500000 );
            person[1] =   new Person("Anika", "anika", "123", 11000100);
            person[2] =    new Person("Ryana","lali", "fardin",10000);
            person[3] =   new Person("Fardin","magu", "halamadrid",80000);

            String line = "";

            // reads message from client until "Over" is sent
            while (true)
            {
                try
                {

                    line = in.readUTF();
                    String username = line;
                    System.out.println(line);
                    line = in.readUTF();
                    String pass = line;
                    System.out.println(line);
                    boolean credok = false;
                    for(int i=0;i<4;i++)
                    {
                        int totmoney = 0;
                        if(person[i].check(username,pass))
                        {
                            credok = true;
                            out.writeUTF("ok");
                            do {
                                line = in.readUTF();
                                System.out.println(line);
                                if(line.equals("1"))
                                {
                                    out.writeUTF("Your current balance is : " + person[i].balance);
                                }
                                if(line.equals("2"))
                                {
                                    myid++;
                                    line = in.readUTF();
                                    clientid = new Integer(line);
                                    out.writeUTF(""+myid);

                                    line = in.readUTF();
                                    int money = new Integer(line);
                                    int err;
                                    if(money<=person[i].balance && totmoney+money<=20000)
                                    {

                                        do {
                                            out.writeUTF("1*"+clientid);

                                            line = in.readUTF();
                                            Random rd = new Random(); // creating Random object
                                            System.out.println(rd.nextInt());
                                            err = Math.abs(rd.nextInt())%100;
                                            System.out.println("error = "+err);
                                            if(line.charAt(0) == 'm')
                                            {
                                                continue;
                                            }
                                            int x = new Integer(line);
                                            System.out.println("error = "+err);
                                            if(x==myid)
                                            {
                                                if(err<30)
                                                {
                                                    out.writeUTF("1");
                                                    break;
                                                }
                                                else {
                                                    out.writeUTF("0");
                                                }
                                            }
                                        }while (true);
                                        person[i].balance-=money;
                                        out.writeUTF("Your current balance is : "+person[i].balance);
                                        totmoney+=money;
                                    }
                                    else
                                    {
                                        out.writeUTF("0");
                                    }
                                }
                                if(line.equals("3"))
                                {
                                    line = in.readUTF();
                                    int money = new Integer(line);
                                    System.out.println(money);
                                    person[i].balance+=money;
                                    out.writeUTF("1");
                                    out.writeUTF("Your current balance is : " + person[i].balance);
                                }
                                if(line.equals("0"))
                                {
                                    break;
                                }
                            }while (true);

                        }
                    }
                    if(!credok)
                    {
                        System.out.println("Username or password is invalid");
                        out.writeUTF("not ok");
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