using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Pong
{
    public partial class Form1 : Form
    {
        // GAME OBJECTS
        int leftPaddleY = 200;
        int rightPaddleY = 200;
        
        int leftPaddleX = 100;
        int paddleHeight = 100;
        int paddleWidth = 15;
        
        int ball_X_Pos = 400;
        int ball_Y_Pos = 300;
        int ball_X_Speed = 7;
        int ball_Y_Speed = 7;
        int ball_Size = 15;

        int leftScore = 0;
        int rightScore = 0;

        bool fameRunning = true;

        bool upPressed, downPressed, wPressed, sPressed;



        public Form1()
        {
            InitializeComponent();
            Timer timer = new Timer();
            timer.Interval = 20;
            timer.Tick += timer_tick;
            timer.Start();

            int leftPaddleY = 200;
            int rightPaddleY = 200;

            int leftPaddleX = 100;
            int paddleHeight = 100;
            int paddleWidth = 15;

            int ball_X_Pos = 400;
            int ball_Y_Pos = 300;
            int ball_X_Speed = 7;
            int ball_Y_Speed = 7;
            int ball_Size = 15;

            int leftScore = 0;
            int rightScore = 0;

            bool fameRunning = true;

            bool upPressed, downPressed, wPressed, sPressed;

            int rightPaddleX = this.ClientSize.Width - 45;

            // FORM SETTINGS
            this.Text = "Ping-Pong Game.exe";
            this.Size = new Size(800, 600);
            this.StartPosition = FormStartPosition.CenterParent;
            this.DoubleBuffered = true;
            this.KeyPreview = true;

            // EVENTS
            this.Paint += Form1_Paint;
            this.KeyDown += (s, e) => { UpdateKey(e.KeyCode, true); };
            this.KeyUp += (s, e) => { UpdateKey(e.KeyCode, false); };



        }
        // RENDERING
        private void Form1_Paint(object sender, PaintEventArgs e)
        {
            Graphics g = e.Graphics;
            Pen whitePen = new Pen(Color.White, 3);
            this.ResizeRedraw = true;
            e.Graphics.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;

            g.FillRectangle(Brushes.Black,0,0,this.Width,this.Height);
            
            g.DrawLine(whitePen, this.Width / 2, 0, this.Width / 2, this.Height);

            g.FillRectangle(Brushes.White, 30, leftPaddleY, 15, 100);
            g.FillRectangle(Brushes.White, this.ClientSize.Width-45, rightPaddleY, 15, 100);
            g.FillEllipse(Brushes.White, ball_X_Pos, ball_Y_Pos, ball_Size, ball_Size);
        }
        private void UpdateKey(Keys key, bool isPressed)
        {
            if (key == Keys.Up) upPressed = isPressed;
            if (key == Keys.Down) downPressed = isPressed;
            if (key == Keys.W) wPressed = isPressed;
            if (key == Keys.S) sPressed = isPressed;
        }
        private void timer_tick(object sender, EventArgs e)
        { 
            if (upPressed && leftPaddleY > 0) leftPaddleY -= 10;
            if (downPressed && leftPaddleY < this.Height - 100) leftPaddleY += 10;
            if (wPressed && rightPaddleY > 0) rightPaddleY -= 10;
            if (sPressed && rightPaddleY < this.Height - 100) rightPaddleY += 10;

            ball_X_Pos += ball_X_Speed;
            ball_Y_Pos += ball_Y_Speed;


            if (ball_Y_Pos <= 0)
            {
                ball_Y_Pos = 0;
                ball_Y_Speed = Math.Abs(ball_Y_Speed); // Летит вниз
            }
            if (ball_Y_Pos >= this.ClientSize.Height - ball_Size)
            {
                ball_Y_Pos = this.ClientSize.Height - ball_Size;
                ball_Y_Speed = -Math.Abs(ball_Y_Speed); // Летит вверх
            }

            if (ball_X_Pos <= 45 && ball_X_Pos >= 30)
            {
                if (ball_Y_Pos + ball_Size >= leftPaddleY && ball_Y_Pos <= leftPaddleY + paddleHeight)
                {
                    ball_X_Speed = Math.Abs(ball_X_Speed);
                    ball_X_Pos = 46; 
                }
            }

            
            int rightPaddleX = this.ClientSize.Width-45;
            if (ball_X_Pos + ball_Size >= rightPaddleX && ball_X_Pos + ball_Size <= rightPaddleX + paddleHeight)
            {
                if (ball_Y_Pos + ball_Size >= rightPaddleY && ball_Y_Pos <= rightPaddleY + 100)
                {
                    ball_X_Speed = -Math.Abs(ball_X_Speed); // Летит влево
                    ball_X_Pos = rightPaddleX - ball_Size - 1; // Выталкиваем
                }
            }

            
            if (ball_X_Pos < 0 || ball_X_Pos > this.ClientSize.Width)
            {
                if (ball_X_Pos < 0) { rightScore++; }
                if (ball_X_Pos > this.ClientSize.Width) {  leftScore++; }
                ball_X_Pos = this.ClientSize.Width / 2;
                ball_Y_Pos = this.ClientSize.Height / 2;
                ball_X_Speed = -ball_X_Speed; // Отдаем мяч проигравшему
            }


            this.Invalidate();
        }
    }
}
