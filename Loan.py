import time
from tkinter import *
from tkinter import messagebox
import pymysql as pymysql
from customtkinter import *
from PIL import Image
import ttkbootstrap as ttb
from ttkbootstrap.tooltip import ToolTip
import webbrowser
from pdf import my_cust_PDF
import random


class LoanClass:
    def __init__(self, mode, un):
        self.un = un
        self.frame_emi = None
        self.input_amt = None
        self.input_app_no = None
        self.input_interest = None
        self.input_period = None
        self.input_loan_amount = None
        self.input_loan_type = None
        self.mode = mode
        set_appearance_mode(mode)

        self.window = CTkToplevel(fg_color=('#f2f2e9', '#000000'))
        #self.window = ttb.Window()
        self.window.title("Subscription")
        self.window.overrideredirect(True)

        self.window.minsize(1200, 780)
        self.window.geometry("1514x990+338+30")

        self.TopFrame = CTkFrame(self.window)
        self.TopFrame.configure(fg_color=('#d6d6d2', '#121211'), border_color='#B76E79', border_width=0.5, width=1210,
                                height=130, corner_radius=20)
        self.TopFrame.place(x=0, y=-15)
        self.createwidgets_tp()
        self.databaseconnection()
        self.options_frame()
        self.emi_frame()
        self.loan_display_frame()

        self.window.bind('<Escape>', lambda e: self.back())
        self.window.focus()

        self.window.mainloop()

    # --------------this establishes database connection-----
    def options_frame(self):
        frame = CTkFrame(self.window, height=150, width=340, fg_color=('#d6d6d2', '#121211'),
                         border_color='#B76E79',  border_width=1)
        frame.place(x=860, y=150)



        delete_button = CTkButton(frame, text=' -  Delete Loan ', width=115, height=30, corner_radius=5,
                                  fg_color=('#d6d6d2', '#121211'),
                                  font=('sans', 16,), border_color='#B76E79', border_width=1,
                                  text_color=('#43605E', '#ffe5d4'), hover_color=('#333331', '#000000'),
                                  command=self.del_loan)
        delete_button.place(x=190, y=20)

        edit_button = CTkButton(frame, text=' *  Edit Loan ', width=115, height=30, corner_radius=5,
                                fg_color=('#d6d6d2', '#121211'),
                                font=('sans', 16,), border_color='#B76E79', border_width=1,
                                text_color=('#43605E', '#ffe5d4'), hover_color=('#333331', '#000000'),
                                command=self.edit_loan)
        edit_button.place(x=30, y=90)

        check_offers_button = CTkButton(frame, text='Check Loan Offers', width=115, height=30, corner_radius=5,
                                        fg_color=('#d6d6d2', '#121211'),
                                        font=('sans', 16,), border_color='#B76E79', border_width=1,
                                        text_color=('#43605E', '#ffe5d4'), hover_color=('#333331', '#000000'),
                                        command=lambda: self.url('apply loan'))
        check_offers_button.place(x=180, y=90)

    def emi_frame(self):
        self.frame_emi = CTkFrame(self.window, height=280, width=340, fg_color=('#d6d6d2', '#121211'),
                                  border_color='#B76E79',  border_width=1)
        self.frame_emi.place(x=860, y=350)
        y_diff = 40
        heading = CTkLabel(self.frame_emi, text='EMI Calculator ', text_color=('#43605E', '#ffe5d4'),
                           font=('Sans', 24, 'bold'))
        heading.place(x=100, y=15)

        amt = CTkLabel(self.frame_emi, text='Amount: ', text_color=('#43605E', '#ffe5d4'))
        amt.place(x=15, y=5 + y_diff*2)
        self.input_amt = CTkEntry(self.frame_emi, placeholder_text='Enter Amount: ', fg_color='#faf9f5',
                                  text_color='black')
        self.input_amt.place(x=120, y=5 + y_diff*2)

        tenure = CTkLabel(self.frame_emi, text='Tenure: ', text_color=('#43605E', '#ffe5d4'))
        tenure.place(x=15, y=5 + y_diff*3)
        self.input_tenure = CTkEntry(self.frame_emi, placeholder_text='Enter Tenure: ', fg_color='#faf9f5',
                                     text_color='black')
        self.input_tenure.place(x=120, y=5 + y_diff*3)

        interest = CTkLabel(self.frame_emi, text='Interest: ', text_color=('#43605E', '#ffe5d4'))
        interest.place(x=15, y=5 + y_diff*4)
        self.input_interest = CTkEntry(self.frame_emi, placeholder_text='Enter Interest: ', fg_color='#faf9f5',
                                       text_color='black')
        self.input_interest.place(x=120, y=5 + y_diff*4)

        save_button = CTkButton(self.frame_emi, text='Compute')
        save_button.configure(anchor='center', fg_color=('#d6d6d2', '#121211'), hover_color=('#333331', '#000000'),
                              text_color=('#43605E', '#ffe5d4'),
                              command=self.emi_computation_inter)
        save_button.place(x=120, y=5 + y_diff*5)

    def emi_computation_inter(self):
        ans = self.emi_calculator(float(self.input_amt.get()), float(self.input_tenure.get()),
                                  float(self.input_interest.get()))
        emi = CTkLabel(self.frame_emi, text='EMI: '+str(int(ans)), text_color=('#43605E', '#ffe5d4'),
                       font=('Sans', 18, 'bold'))
        emi.place(x=120, y=5 + 40*6)

    def emi_calculator(self, p, t, r):
        r = r/(12*100)
        t = t*12
        numerator = p*r*pow(1+r, t)
        denominator = pow(1+r, t)-1
        emi = numerator/denominator
        return emi

    def url(self, item):
        url = "https://www.google.com/search?q="
        webbrowser.open(url + item)
    def databaseconnection(self):
        try:
            self.connection = pymysql.connect(host='localhost', db='finance_manager_db', user='root', password='')
            self.cur = self.connection.cursor()
        except Exception as e:
            messagebox.showerror("Error", "Database connection error \n" + str(e), parent=self.window)

    def createwidgets_tp(self):

        img = CTkImage(Image.open("myimages//wel.png"), size=(400, 100))
        wel = CTkLabel(self.TopFrame, image=img, text='')

        sublabel = CTkLabel(self.TopFrame, text='Review your Loan track and progress',
                            font=('Sans', 18, 'bold'),
                            fg_color='transparent')

        profile_combobox = ttb.Combobox(self.TopFrame, values=['User', 'Change User', 'Log out'])
        profile_combobox.current(0)

        b1 = CTkButton(self.TopFrame, text="<--", command=self.back, fg_color=('#d6d6d2', '#121211'), width=18,
                       text_color=('#43605E', '#ffe5d4'), hover_color=('#333331', '#000000'))
        b1.place(x=5, y=14)
        ToolTip(b1, text="Press ESC to Close")

        wel.place(x=25, y=8)
        sublabel.place(x=55, y=95)
        profile_combobox.place(x=1300, y=35)

    def add_loan(self):

        small_window = CTkToplevel(self.window)
        small_window.title('Add Loan')
        small_window.configure(fg_color=('#d6d6d2', '#121211'))
        small_window.after(10, small_window.lift)
        width = 400
        height = 400
        small_window.minsize(width, height)
        x = small_window.winfo_screenwidth() // 2 - width // 2
        y = small_window.winfo_screenheight() // 2 - height // 2
        small_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        y_diff = 40

        card_num = CTkLabel(small_window, text='Loan type: ', text_color=('#43605E', '#ffe5d4'))
        card_num.place(x=5, y=5)
        self.input_loan_type = CTkEntry(small_window, placeholder_text='Enter Loan type: ', fg_color='#faf9f5',
                                        text_color='black')
        self.input_loan_type.place(x=120, y=5)

        card_name = CTkLabel(small_window, text='Loan amount: ', text_color=('#43605E', '#ffe5d4'))
        card_name.place(x=5, y=5 + y_diff)
        self.input_loan_amount = CTkEntry(small_window, placeholder_text='Enter Loan amount: ', fg_color='#faf9f5',
                                          text_color='black')
        self.input_loan_amount.place(x=120, y=5 + y_diff)

        period = CTkLabel(small_window, text='Tenure: ', text_color=('#43605E', '#ffe5d4'))
        period.place(x=5, y=5 + y_diff * 2)
        self.input_period = CTkEntry(small_window, placeholder_text='Enter Tenure: ', fg_color='#faf9f5',
                                     text_color='black')
        self.input_period.place(x=120, y=5 + y_diff * 2)

        interest = CTkLabel(small_window, text='Interest Rate: ', text_color=('#43605E', '#ffe5d4'))
        interest.place(x=5, y=5 + y_diff * 3)
        self.input_interest = CTkEntry(small_window, placeholder_text='Enter Interest Rate: ', fg_color='#faf9f5',
                                       text_color='black')
        self.input_interest.place(x=120, y=5 + y_diff * 3)

        app_no = CTkLabel(small_window, text='Application Number: ', text_color=('#43605E', '#ffe5d4'))
        app_no.place(x=5, y=5 + y_diff * 4)
        self.input_app_no = CTkEntry(small_window, placeholder_text='Enter Application Number: ', fg_color='#faf9f5',
                                     text_color='black')
        self.input_app_no.place(x=120, y=5 + y_diff * 4)

        save_button = CTkButton(small_window, text='Add')
        save_button.configure(anchor='center', fg_color=('#d6d6d2', '#121211'), hover_color=('#333331', '#000000'),
                              text_color=('#43605E', '#ffe5d4'),
                              command=lambda: self.add_loan_data(small_window))
        save_button.place(x=120, y=5 + y_diff * 5)

        small_window.mainloop()

    def clearpage(self):
        self.input_app_no.delete(0, END)
        self.input_loan_amount.delete(0, END)
        self.input_loan_type.delete(0, END)
        self.input_period.delete(0, END)
        self.input_interest.delete(0, END)

    def add_loan_data(self, small_window):
        ans = self.emi_calculator(float(self.input_loan_amount.get()), float(self.input_period.get()),
                                  float(self.input_interest.get()))
        try:
            qry = 'insert into loan values(%s,%s,%s,%s,%s,%s,%s)'
            rowcount = self.cur.execute(qry, (self.un, self.input_app_no.get(), self.input_loan_type.get(),
                                              self.input_loan_amount.get(),
                                              self.input_period.get(), self.input_interest.get(), ans))
            self.connection.commit()
            if rowcount == 1:
                messagebox.showinfo("Success", "Loan Data Added Successfully", parent=small_window)
                self.clearpage()
        except Exception as e:
            messagebox.showerror("Error", "Insertion Error : \n" + str(e), parent=small_window)

    def loan_display(self):
        pass

    def del_loan(self):
        small_window = CTkToplevel(self.window)
        small_window.title('Delete Loan')
        small_window.configure(fg_color=('#d6d6d2', '#121211'))
        small_window.after(10, small_window.lift)
        width = 400
        height = 400
        small_window.minsize(width, height)
        x = small_window.winfo_screenwidth() // 2 - width // 2
        y = small_window.winfo_screenheight() // 2 - height // 2
        small_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        app_no = CTkLabel(small_window, text='Application Number: ', text_color=('#43605E', '#ffe5d4'))
        app_no.place(x=5, y=5)
        self.input_app_no = CTkEntry(small_window, placeholder_text='Enter Application Number: ', fg_color='#faf9f5',
                                     text_color='black')
        self.input_app_no.place(x=140, y=5)

        save_button = CTkButton(small_window, text='Delete')
        save_button.configure(anchor='center', fg_color=('#d6d6d2', '#121211'), hover_color=('#333331', '#000000'),
                              text_color=('#43605E', '#ffe5d4'),
                              command=lambda: self.delete_loan_data(small_window))
        save_button.place(x=120, y=55)

        small_window.mainloop()

    def delete_loan_data(self, small_window):
        ans = messagebox.askquestion("Confirmation", "Are you sure to delete ??", parent=small_window)
        if ans == "yes":
            try:
                qry = "delete from loan where application_number=%s and user_name=%s"
                rowcount = self.cur.execute(qry, (self.input_app_no.get(), self.un))
                self.connection.commit()
                if rowcount == 1:
                    messagebox.showinfo("Success", "Loan Data Deleted Successfully", parent=small_window)
                    self.input_app_no.delete(0, END)
            except Exception as e:
                messagebox.showerror("Error", "Deletion Error : \n" + str(e), parent=small_window)

    def edit_loan(self):
        small_window = CTkToplevel(self.window)
        small_window.title('Add Loan')
        small_window.configure(fg_color=('#d6d6d2', '#121211'))
        small_window.after(10, small_window.lift)
        width = 400
        height = 400
        small_window.minsize(width, height)
        x = small_window.winfo_screenwidth() // 2 - width // 2
        y = small_window.winfo_screenheight() // 2 - height // 2
        small_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        y_diff = 40

        card_num = CTkLabel(small_window, text='Loan type: ', text_color=('#43605E', '#ffe5d4'))
        card_num.place(x=5, y=5)
        self.input_loan_type = CTkEntry(small_window, placeholder_text='Enter Loan type: ', fg_color='#faf9f5',
                                        text_color='black')
        self.input_loan_type.place(x=120, y=5)

        card_name = CTkLabel(small_window, text='Loan amount: ', text_color=('#43605E', '#ffe5d4'))
        card_name.place(x=5, y=5 + y_diff)
        self.input_loan_amount = CTkEntry(small_window, placeholder_text='Enter Loan amount: ', fg_color='#faf9f5',
                                          text_color='black')
        self.input_loan_amount.place(x=120, y=5 + y_diff)

        period = CTkLabel(small_window, text='Tenure: ', text_color=('#43605E', '#ffe5d4'))
        period.place(x=5, y=5 + y_diff * 2)
        self.input_period = CTkEntry(small_window, placeholder_text='Enter Tenure: ', fg_color='#faf9f5',
                                     text_color='black')
        self.input_period.place(x=120, y=5 + y_diff * 2)

        interest = CTkLabel(small_window, text='Interest Rate: ', text_color=('#43605E', '#ffe5d4'))
        interest.place(x=5, y=5 + y_diff * 3)
        self.input_interest = CTkEntry(small_window, placeholder_text='Enter Interest Rate: ', fg_color='#faf9f5',
                                       text_color='black')
        self.input_interest.place(x=120, y=5 + y_diff * 3)

        app_no = CTkLabel(small_window, text='Application Number: ', text_color=('#43605E', '#ffe5d4'))
        app_no.place(x=5, y=5 + y_diff * 4)
        self.input_app_no = CTkEntry(small_window, placeholder_text='Enter Application Number: ', fg_color='#faf9f5',
                                     text_color='black')
        self.input_app_no.place(x=120, y=5 + y_diff * 4)

        save_button = CTkButton(small_window, text='Edit')
        save_button.configure(anchor='center', fg_color=('#d6d6d2', '#121211'), hover_color=('#333331', '#000000'),
                              text_color=('#43605E', '#ffe5d4'),
                              command=lambda: self.edit_loan_data(small_window))
        save_button.place(x=120, y=5 + y_diff * 5)

        small_window.mainloop()

    def edit_loan_data(self, small_window):
        try:
           qry = 'Update loan set type = %s, amount=%s, period=%s, interest=%s where application_number = %s ' \
                 'and user_name=%s'
           rowcount = self.cur.execute(qry, (self.input_loan_type.get(),
                                             self.input_loan_amount.get(),
                                             self.input_period.get(),
                                             self.input_interest.get(),
                                             self.input_app_no.get(),
                                             self.un))
           self.connection.commit()
           if rowcount == 1:
            messagebox.showinfo("Success", "Transaction Record Added Successfully", parent=small_window)
            self.clearpage()
        except Exception as e:
            messagebox.showerror("Error", "Insertion Error : \n" + str(e), parent=small_window)

    def loan_display_frame(self):
        y_diff = 0
        dark = ['#2F4F4F', '#8B3A3A', '#35586C', '#E38217', '#36648B', '#8B7D6B', '#344152', '#004F00',
                '#E33638',
                '#9370DB', '#4F2F4F', '#551033']
        light = ['#5C9A9A', '#BF6666', '#5D92B0', '#EEA85A', '#6195C1', '#AFA497', '#617A99', '#00D600',
                 '#EB7273',
                 '#B299E5', '#9A5C9A', '#C12474']
        try:
            qry = " select * from loan where user_name=%s"
            rowcount = self.cur.execute(qry, self.un)
            data = self.cur.fetchall()
            print(data)
            for i in range(len(data)):
                random_int = random.randint(0, len(dark) - 1)
                pic_list = ['loan1.png', 'loan2.png', 'loan3.png', 'loan4.png']
                random_int_pic = random.randint(0, len(pic_list) - 1)
                img = CTkImage(Image.open("myimages//" + pic_list[i]), size=(150, 90))
                frame_dis = CTkFrame(self.window, width=650, height=140, border_width=2,
                                     border_color=dark[random_int], fg_color=light[random_int])
                label = CTkLabel(frame_dis, text=" ", image=img)
                label.place(x=10, y=5)
                lb1 = CTkLabel(frame_dis, text=data[i][2], text_color=('#43605E', '#ffe5d4'),
                               font=('Sans', 32, 'bold'))
                lb1.place(x=250, y=5)

                lb2 = CTkLabel(frame_dis, text="Application Number: " + str(data[i][1]), text_color=('#43605E', '#ffe5d4'),
                               font=('Sans', 18, 'bold'))
                lb2.place(x=250, y=50)

                ans = self.emi_calculator(data[i][3], data[i][4], data[i][5])
                lb6 = CTkLabel(frame_dis, text="EMI: " + str(int(ans)), text_color=('#43605E', '#ffe5d4'),
                               font=('Sans', 18, 'bold'))
                lb6.place(x=250, y=100)

                lb3 = CTkLabel(frame_dis, text="Amount: " + str(data[i][3]), text_color=('#43605E', '#ffe5d4'),
                               font=('Sans', 18, 'bold'))
                lb3.place(x=480, y=5)

                lb4 = CTkLabel(frame_dis, text="Tenure: " + str(data[i][4]), text_color=('#43605E', '#ffe5d4'),
                               font=('Sans', 18, 'bold'))
                lb4.place(x=480, y=50)

                lb5 = CTkLabel(frame_dis, text="Interest rate: " + str(data[i][5]), text_color=('#43605E', '#ffe5d4'),
                               font=('Sans', 18, 'bold'))
                lb5.place(x=480, y=100)

                frame_dis.place(x=20, y=150 + y_diff)
                y_diff += 160
            if rowcount == 1:
                messagebox.showinfo("Success", "Transaction Record Added Successfully", parent=self.window)
                #self.clearpagetransaction()
        except Exception as e:
            messagebox.showerror("Error", "Insertion Error : \n" + str(e), parent=self.window)

    def back(self):
        self.window.destroy()

    def print(self):
        try:
            qry = " select * from transactions where user_name=%s"
            rowcount = self.cur.execute(qry, self.un)
            transactions = self.cur.fetchall()
            ls = []
            for myrow in transactions:
                ls.append([myrow[0], myrow[1], myrow[2], myrow[3], myrow[4], myrow[5]])
        except Exception as e:
            messagebox.showerror("Error", "Error while fetching Data  : \n" + str(e), parent=self.window)

        headings = ['Payment', 'Date', 'Card Number', 'Credit/Debit', 'Amount', 'Payment ID']
        pdf = my_cust_PDF()
        pdf.print_chapter(ls, headings)

        pdf.output('pdf_file1.pdf')
        os.system('explorer.exe "pdf_file1.pdf"')


if __name__ == '__main__':
    obj = LoanClass('light')