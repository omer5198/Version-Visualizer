using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace Version_Visualizer
{
    public partial class VersionVis : Form
    {
        Client client;
        OpenFileDialog createProjectDialog = new OpenFileDialog();
        public VersionVis()
        {
            InitializeComponent();
            client = new Client(this, "127.0.0.1", 1356);
        }

        private void VersionVis_Load(object sender, EventArgs e)
        {
            Update_ProjectList();
            createProjectDialog.Multiselect = true;
        }
        private void Update_ProjectList()
        {
            client.Send("GetProjectList");
            listBox1.Items.Clear();
            string data = client.Recieve();
            foreach (string dir in data.Split('?'))
            {
                listBox1.Items.Add(dir);
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (createProjectDialog.ShowDialog() == DialogResult.OK)
            {
                foreach (string file in createProjectDialog.FileNames)
                {
                    listBox2.Items.Add(file);
                }
            }
        }

        private void tabControl1_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (tabControl1.SelectedTab == tabPage1)
            {
                Update_ProjectList();
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            CreateProject(textBox1.Text, String.Join("?", listBox2.Items.Cast<String>()));
            string response = client.Recieve();
            if (response == "SUCCESS")
                MessageBox.Show("The Project \"" + textBox1.Text + "\" Was Successfully Created.");
            else
                MessageBox.Show("Something Went Wrong. The Project Was Not Created.");
        }
        private void CreateProject(string name, string files_path)
        {
            client.Send("CreateProject|" + name + "|" + files_path);
        }

        private void listBox2_MouseDoubleClick(object sender, MouseEventArgs e)
        {
            listBox2.Items.Remove(listBox2.SelectedItem);
        }
    }
}
