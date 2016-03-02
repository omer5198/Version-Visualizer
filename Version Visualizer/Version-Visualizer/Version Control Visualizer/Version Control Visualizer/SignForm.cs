using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Net.Sockets;

namespace Version_Control_Visualizer
{
    public partial class SignForm : Form
    {
        Client client;
        public SignForm()
        {
            InitializeComponent();
            client = new Client(this, "127.0.0.1", 1356);
        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {
            textBox2.PasswordChar = '*';
        }

        private void LoginButton_Click(object sender, EventArgs e)
        {
            if (textBox1.Text == "" || textBox2.Text == "")
                MessageBox.Show("Please fill in both fields.");
            else
            {
                client.Send("Login|" + textBox1.Text + "|" + textBox2.Text);
                Handle_Response(client.Recieve());
            }
        }

        private void SignUpButton_Click(object sender, EventArgs e)
        {
            if (textBox1.Text == "" || textBox2.Text == "")
                MessageBox.Show("Please fill in both fields.");
            else
            {
                client.Send("Create|" + textBox1.Text + "|" + textBox2.Text);
                Handle_Response(client.Recieve());
            }
        }
        private void Handle_Response(string response)
        {
            switch (response)
            {
                case "Successful":
                    MessageBox.Show("Logged in successfully, Initializing...");
                    break;
                case "Invalid_User":
                    MessageBox.Show("Invalid user.");
                    textBox1.SelectAll();
                    textBox1.Focus();
                    break;
                case "Invalid_Pass":
                    MessageBox.Show("Wrong password. Please try again.");
                    textBox2.SelectAll();
                    textBox2.Focus();
                    break;
                case "Created":
                    MessageBox.Show("The user created successfully. You may now log in.");
                    break;
                case "Already_Exists":
                    MessageBox.Show("This username is already taken.");
                    textBox1.SelectAll();
                    textBox1.Focus();
                    break;
                case "Error":
                    break;
                default:
                    MessageBox.Show("An error occured. Please try again.");
                    break;
            }
        }
    }
}
