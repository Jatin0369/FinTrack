from tkinter import *
import ttkbootstrap as ttk
from tkinter import messagebox
from customtkinter import *
from PIL import Image
from ttkbootstrap.tooltip import ToolTip

import pymysql
class PasswordRecoveryClass:
    def __init__(self):
        self.window = CTkToplevel(fg_color=('#f2f2e9', '#000000'))
        self.window.title("Finance Manager/Login")
        self.window.overrideredirect(True)
        #----------- settings ------------------------
        w = self.window.winfo_screenwidth()
        h = self.window.winfo_screenheight()
        w1 = int(w/2)
        h1 = int(h/2)
        x1 = int(w/4)
        y1 = int(h/4)
        #self.window.minsize(w1,h1)
        self.window.geometry("%dx%d+%d+%d"%(w1-280, h1-100, x1+50, y1))# width,height,x,y
        # ---------- widgets -----------------------
        img = CTkImage(Image.open("myimages//login_page.jpg"), size=(300, 1000))
        label = CTkLabel(self.window, text=" ", image=img, corner_radius=20)
        label.place(x=-20, y=-5)

        b1 = CTkButton(self.window, text="<--", command=self.back, fg_color=('#d6d6d2', '#121211'), width=18,
                       text_color=('#43605E', '#ffe5d4'), hover_color=('#333331', '#000000'))
        b1.place(x=300, y=5)
        ToolTip(b1, text="Press ESC to Close")

        hdlabel = CTkLabel(self.window, text='Recover,', text_color=('#43605E', '#ffe5d4'), font=('Arialic Hollow', 32))
        hdlabel.place(x=400, y=30)

        hdlabel2 = CTkLabel(self.window, text='Password', text_color=('#43605E', '#ffe5d4'), font=('Arial', 28, 'bold'))
        hdlabel2.place(x=400, y=80)

        self.user_name = CTkEntry(self.window, width=200, height=35, fg_color=('#f2f2e9', '#000000'), border_color='#B76E79',
                                  placeholder_text='User Name', border_width=1)
        self.user_name.place(x=400, y=150)

        self.e_id = CTkEntry(self.window, width=200, height=35, fg_color=('#f2f2e9', '#000000'), border_color='#B76E79',
                             placeholder_text='Email-id', border_width=1)
        self.e_id.place(x=400, y=200)

        recover_button = CTkButton(self.window, text='Recover', fg_color=('#f2f2e9', '#000000'),
                                    font=('Arial', 14), border_color='#B76E79', border_width=1, width=80, height=30,
                                    text_color=('#43605E', '#ffe5d4'), hover_color=('#333331', '#000000'),
                                    command=self.show_psswd)
        recover_button.place(x=460, y=250)

        self.databaseconnection()
        self.window.bind('<Escape>', lambda e: self.back())
        self.window.mainloop()

    def databaseconnection(self):
        try:
            self.connection = pymysql.connect(host='localhost', db='finance_manager_db', user='root', password='')
            self.cur = self.connection.cursor()
        except Exception as e:
            messagebox.showerror("Error", "Database connection error \n" + str(e), parent=self.window)

    def back(self):
        self.window.destroy()

    def show_psswd(self):
        try:
            qry = " select password from user_table where user_name=%s and e_id=%s"
            rowcount = self.cur.execute(qry, (self.user_name.get(), self.e_id.get()))
            data = self.cur.fetchone()

        except Exception as e:
            messagebox.showerror("Error", "Error while fetching Data  : \n" + str(e), parent=self.window)
        label_psswd = CTkLabel(self.window, text='Your Password is: ' + data[0], text_color=('#43605E', '#ffe5d4'),
                               font=('Arial', 16))
        label_psswd.place(x=410, y=300)


if __name__ == '__main__':
    obj = PasswordRecoveryClass()