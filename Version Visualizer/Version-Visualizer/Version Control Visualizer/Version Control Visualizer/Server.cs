using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Sockets;
using System.Net;
using System.Threading;
using System.Windows.Forms;
using System.Diagnostics;

namespace Version_Control_Visualizer
{
    class Server
    {
        private const int BUFF_SIZE = 1024;
        private int PORT;
        private string IP;
        private SignForm form;
        private Socket socket;
        Socket listener;
        Socket reciever;
        private Process pyProcess;

        public Server(SignForm form)
        {
            this.form = form;
            Thread serverThread = new Thread(Run);
            serverThread.IsBackground = true;
            serverThread.Start();
        }
        private void Run()
        { 
            pyProcess = new Process();
            pyProcess.StartInfo.FileName = @"C:\Python27\python.exe";
            pyProcess.StartInfo.Arguments = "client.py";
            //pyProcess.StartInfo.WindowStyle = ProcessWindowStyle.Hidden;
            pyProcess.Start();
            listener = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            listener.Bind(new IPEndPoint(IPAddress.Loopback, PORT));
            listener.Listen(1);
            reciever = listener.Accept();
            while (true)
            {
                byte[] buf = new byte[1024];
                int recv = reciever.Receive(buf);
                string data = Encoding.ASCII.GetString(buf, 0, recv);
                while (data.IndexOf("<E\0O\0F>") > -1)
                {
                    buf = new byte[1024];
                    recv = reciever.Receive(buf);
                    data += Encoding.ASCII.GetString(buf, 0, recv);
                }
                
            }
        }
        public void Send(string command)
        {
            reciever.Send(Encoding.ASCII.GetBytes(command));
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
    }
}
