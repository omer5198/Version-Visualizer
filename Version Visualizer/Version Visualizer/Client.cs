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

namespace Version_Visualizer
{
    class Client
    {
        private const int BUFF_SIZE = 1024;
        private int PORT;
        private string IP;
        private VersionVis ver;
        private Socket socket;
        private Process pyProcess;
        public Client(VersionVis ver, string IP, int PORT)
        {
            this.ver = ver;
            this.IP = IP;
            this.PORT = PORT;
            pyProcess = new Process();
            pyProcess.StartInfo.FileName = @"C:\Python27\python.exe";
            pyProcess.StartInfo.Arguments = @"Version-Visualizer\client.py";
            pyProcess.StartInfo.WindowStyle = ProcessWindowStyle.Hidden;
            pyProcess.Start();
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
                string data = Encoding.ASCII.GetString(buff, 0, bytesRec);
                while (data.IndexOf("<E\0O\0F>") > -1)
                {
                    buff = new byte[1024];
                    bytesRec = this.socket.Receive(buff);
                    data += Encoding.ASCII.GetString(buff, 0, bytesRec);
                }
                return data.Split('<')[0];
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
