from tkinter import *
import ttkbootstrap as ttb
from tkinter import messagebox
from customtkinter import *
from PIL import Image
from ttkbootstrap.tooltip import ToolTip
import pymysql

class LoginClass:
    def __init__(self):
        self.user_name = None
        self.e_id = None
        self.psswd = None
        self.window = None
        # self.theme = 'mylight'
        # self.mode = 'light'

        self.theme = 'cyborg'
        self.mode = 'dark'

        self.master = ttb.Window(themename=self.theme)
        self.master.title("FinTrack")
        self.master.iconbitmap('myimages/logo.ico')
        img = PhotoImage(file='myimages/logo.png')
        self.master.iconphoto(False, img)
        set_appearance_mode(self.mode)
        w = self.master.winfo_screenwidth()
        h = self.master.winfo_screenheight()
        w1 = int(w / 2)
        h1 = int(h / 2)
        x1 = int(w / 4)
        y1 = int(h / 4)
        self.master.geometry("%dx%d+%d+%d" % (w1-150, h1-60, x1+70, y1))
        img = CTkImage(Image.open("myimages//main_pic.png"), size=(400, 400))
        label = CTkLabel(self.master, text=" ", image=img, corner_radius=20)
        label.place(x=260, y=-5)

        img = CTkImage(Image.open("myimages//logo.png"), size=(50, 50))
        label = CTkLabel(self.master, text=" ", image=img, corner_radius=20)
        label.place(x=-15, y=0)

        hdlabel = CTkLabel(self.window, text='Finance Tracker',
                           text_color=('#43605E', '#ffe5d4'), font=('Arialic Hollow', 36, 'bold'))
        hdlabel.place(x=20, y=80)

        hdlabel2 = CTkLabel(self.window, text='"Where Money Meets\n Management"', text_color=('#43605E', '#ffe5d4'),
                            font=('Arial', 18, 'bold'))
        hdlabel2.place(x=60, y=140)

        login_button = CTkButton(self.window, text='Click to Manage', fg_color=('#f2f2e9', '#000000'),
                                 font=('Arial', 14), border_color='#B76E79', border_width=1, width=120, height=40,
                                 text_color=('#43605E', '#ffe5d4'), hover_color=('#333331', '#000000'),
                                 command=lambda: self.open(self.theme, self.mode))
        login_button.place(x=85, y=220)
        login_button = CTkButton(self.window, text='Click to Exit', fg_color=('#f2f2e9', '#000000'),
                                 font=('Arial', 14), border_color='#B76E79', border_width=1, width=120, height=30,
                                 text_color=('#43605E', '#ffe5d4'), hover_color=('#333331', '#000000'),
                                 command=lambda: self.master.destroy())
        login_button.place(x=85, y=280)

        self.master.mainloop()

    def open(self, theme, mode):

        self.user_name = None
        self.psswd = None
        self.e_id = None
        self.connection = None
        self.cur = None
        self.theme = theme
        self.mode = mode
        set_appearance_mode(self.mode)
        self.window = CTkToplevel(fg_color=('#f2f2e9', '#000000'))
        self.window.title("Finance Manager/Login")
        self.window.overrideredirect(True)
        # ----------- settings ------------------------
        w = self.window.winfo_screenwidth()
        h = self.window.winfo_screenheight()
        w1 = int(w / 2)
        h1 = int(h / 2)
        x1 = int(w / 4)
        y1 = int(h / 4)
        # self.window.minsize(w1,h1)
        self.window.geometry("%dx%d+%d+%d" % (w1 - 280, h1-100, x1+50, y1))  # width,height,x,y
        # ---------- widgets -----------------------
        img = CTkImage(Image.open("myimages//login_page.jpg"), size=(300, 1000))
        label = CTkLabel(self.window, text=" ", image=img, corner_radius=20)
        label.place(x=-20, y=-5)

        b1 = CTkButton(self.window, text="X", command=self.back, fg_color=('#d6d6d2', '#121211'), width=18,
                       text_color=('#43605E', '#ffe5d4'), hover_color=('#333331', '#000000'))
        b1.place(x=650, y=5)
        ToolTip(b1, text="Press ESC to Close")

        hdlabel = CTkLabel(self.window, text='Hello,', text_color=('#43605E', '#ffe5d4'), font=('Arialic Hollow', 42))
        hdlabel.place(x=400, y=30)

        hdlabel2 = CTkLabel(self.window, text='Welcome!', text_color=('#43605E', '#ffe5d4'), font=('Arial', 36, 'bold'))
        hdlabel2.place(x=400, y=80)

        self.user_name = CTkEntry(self.window, width=200, height=35, fg_color=('#f2f2e9', '#000000'),
                                  border_color='#B76E79',
                                  placeholder_text='User Name', border_width=1)
        self.user_name.place(x=400, y=150)

        self.e_id = CTkEntry(self.window, width=200, height=35, fg_color=('#f2f2e9', '#000000'), border_color='#B76E79',
                             placeholder_text='Email-id', border_width=1)
        self.e_id.place(x=400, y=200)

        self.psswd = CTkEntry(self.window, width=200, height=35, fg_color=('#f2f2e9', '#000000'),
                              border_color='#B76E79',
                              placeholder_text='Password', border_width=1)
        self.psswd.place(x=400, y=250)

        login_button = CTkButton(self.window, text='Login', fg_color=('#f2f2e9', '#000000'),
                                 font=('Arial', 14), border_color='#B76E79', border_width=1, width=80, height=30,
                                 text_color=('#43605E', '#ffe5d4'), hover_color=('#333331', '#000000'),
                                 command=self.LogInData)
        login_button.place(x=410, y=310)
        from Signup import SignUpClass
        signup_button = CTkButton(self.window, text='Sign Up', fg_color=('#f2f2e9', '#000000'),
                                  font=('Arial', 14), border_color='#B76E79', border_width=1, width=80, height=30,
                                  text_color=('#43605E', '#ffe5d4'), hover_color=('#333331', '#000000'),
                                  command=lambda:SignUpClass(self.user_name.get(), self.e_id.get(), self.psswd.get()))
        signup_button.place(x=510, y=310)

        label_psswd = CTkLabel(self.window, text='Forgot Password? ', text_color=('#43605E', '#ffe5d4'),
                               font=('Arial', 12))
        label_psswd.place(x=410, y=352)

        from psswd_recovery import PasswordRecoveryClass
        forgot_psswd_button = CTkButton(self.window, text='Click Here', fg_color=('#f2f2e9', '#000000'),
                                        font=('Arial', 13), width=80, height=30, text_color=('#43605E', '#ffe5d4'),
                                        hover_color=('#d6d6d2', '#121211'), command=PasswordRecoveryClass)
        forgot_psswd_button.place(x=510, y=350)
        self.databaseconnection()
        self.window.bind('<Escape>', lambda e: self.back())

    def databaseconnection(self):
        try:
            self.connection = pymysql.connect(host='localhost', db='finance_manager_db', user='root', password='')
            self.cur = self.connection.cursor()
        except Exception as e:
            messagebox.showerror("Error", "Database connection error \n" + str(e), parent=self.window)

    def LogInData(self):
        try:
            qry = " select * from user_table where user_name=%s and password=%s"
            rowcount = self.cur.execute(qry, (self.user_name.get(), self.psswd.get()))
            data = self.cur.fetchone()
            if data:
                un = self.user_name.get()
                ut = self.psswd.get()
                self.window.destroy()
                from Dashboard import DashboardClass
                DashboardClass(un, ut, self.theme, self.mode)
            else:
                messagebox.showwarning("Empty", "Wrong username or password", parent=self.window)
        except Exception as e:
            messagebox.showerror("Error", "Error while fetching Data  : \n"+str(e), parent=self.window)

    def back(self):
        self.window.destroy()


if __name__ == '__main__':
    LoginClass()