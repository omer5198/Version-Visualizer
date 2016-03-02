using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;

namespace Version_Control_Visualizer
{
    static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new SignForm());
        }
    }
}
