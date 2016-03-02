using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net.Sockets;
using System.Net;
using System.Windows.Forms;

namespace Version_Control_Visualizer
{
    class Client
    {
        private const int BUFF_SIZE = 1024;
        private int PORT;
        private string IP;
        private SignForm form;
        private Socket socket;
        public Client(SignForm form, string IP, int PORT)
        {
            this.form = form;
            this.IP = IP;
            this.PORT = PORT;
            try
            {
                IPEndPoint remoteEP = new IPEndPoint(IPAddress.Parse(IP), PORT);
                this.socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
                this.socket.Connect(remoteEP);
            }
            catch
            {
                MessageBox.Show("Couldn't connect to the server. Entering offline mode.");
            }
        }
        
        public void Send(string data)
        {
            try
            {
                byte[] buff = new byte[BUFF_SIZE];
                byte[] msg = Encoding.ASCII.GetBytes(data);
                int bytesSent = this.socket.Send(msg);
            }
            catch
            {
                MessageBox.Show("Failed to send the data. Please try again. If the problem persists, reopen the program.");
            }
        }
        public string Recieve()
        {
            try
            {
            byte[] buff = new byte[BUFF_SIZE];
            int bytesRec = this.socket.Receive(buff);
            return Encoding.ASCII.GetString(buff, 0, bytesRec);
            }
            catch
            {
                MessageBox.Show("Failed to send the data. Please try again. If the problem persists, reopen the program.");
                return "Error";
            }
        }
        public void Close()
        {
            socket.Shutdown(SocketShutdown.Both);
            socket.Close();
        }
    }
}
