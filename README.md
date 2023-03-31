# Computer Networking Experiments

## Experiment 1  
### [Introduction to Socket Programming](https://github.com/anika235/Computer-Networking/blob/7b81cd74bd5f35009bbde0f2f3a500e299855131/TCP(Socket%20Programming)/report.pdf)
Creating TCP Connections using Socket Programming
- Establishing a TCP connection between a server process running on
host A and a client process running on host B can be done using socket
programming
  - Small letter to capital conversion for a line of text: The client
process can send a request to the server process with a line of
text, and the server process can convert all small letters to capital
letters and send the converted text as a response to the client
process.
  - Checking whether a number is prime or not: The client process
can send a request to the server process with a number, and the
server process can check whether the number is prime or not and
send the result as a response to the client process.
- To handle failure of request messages, failure of response messages and
process execution failures, a non-idempotent operation using exactly-
once semantics can be implemented.
  - An application-level protocol can be designed that allows a user’s
card and password to be verified, the account balance to be
queried, and an account withdrawal to be made. The protocol
can include messages such as:
    - Request for verification of card and password
    - Request for account balance
    - Request for withdrawal
    - Confirmation of withdrawal
    - Error message if there is not enough money in the account
  - To handle errors related to both request and response messages,
the protocol can include a mechanism for resending messages
in case of failures, and an acknowledgement system to confirm the receipt of messages. The protocol can also include a time-
out mechanism to handle cases where a response is not received
within a certain period. In case of process execution failures, the
protocol can include a mechanism to restart the process.
## Experiment 2
### [Implementing File transfer using Socket Programming and HTTP GET/POST requests](https://github.com/anika235/Computer-Networking/blob/7b81cd74bd5f35009bbde0f2f3a500e299855131/File%20Transfer%20via%20Socket%20Programming/Experiment.pdf)
The objective of this lab is to give hands-on experience with socket pro
gramming and HTTP file transfer. You will
- implement multithreaded chat from many clients to one server
- set up an HTTP server process with a few objects
- use GET and POST methods to upload and download objects in between HTTP clients and a server
## Experiment 3
### [Distributed Database Management and Implementation of Iterative and Recursive Queries of DNS Records.](https://github.com/anika235/Computer-Networking/blob/7b81cd74bd5f35009bbde0f2f3a500e299855131/Iterative%20and%20Recursive%20Dns%20Records/report.pdf)
The preliminary objective of this lab is to emulate the Domain Name Service (DNS) protocol and to understand the
difference between iterative and recursive DNS resolution. The client can request IP address of his desired domain and
the nameserver hierarchy will use the DNS resolution to return the IP address of the corresponding domain to the client
if the domain name is valid.
## Experiment 4
### [Implementation of TCP flow control and congestion control algorithm (TCP Tahoe).](https://github.com/anika235/Computer-Networking/blob/7b81cd74bd5f35009bbde0f2f3a500e299855131/TCP%20Tahoe/TCP%20Tahoe.pdf)
- To gather knowledge about how TCP controls the flow of data between a sender and a receiver
- To learn how TCP controls and avoids the congestion of data when a sender or receiver detects a
congestion in the link in-between them. ( TCP Tahoe)

## Exepriement 5
### [Implementation of TCP Reno congestion control algorithm.](https://github.com/anika235/Computer-Networking/blob/7b81cd74bd5f35009bbde0f2f3a500e299855131/TCP%20Reno/Report.pdf)
- To understand and implement the TCP Reno congestion control algorithm, and compare it with TCP
Tahoe.

## Experiment 6
### [Implementation of Link State Algorithm](https://github.com/anika235/Computer-Networking/blob/7b81cd74bd5f35009bbde0f2f3a500e299855131/Link%20State%20Algorithm/Lab_experiment_7_47_61.pdf)
The purpose of this experiment is to develop an understanding of the Link State Algorithm and its applications in
computer networks by implementing the algorithm.
