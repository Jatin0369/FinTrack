import ttkbootstrap as ttk
from tkinter import *
from tkinter import messagebox
import pymysql as pymysql
from customtkinter import *
from PIL import Image
import ttkbootstrap as ttb
from pdf import my_cust_PDF
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from ttkbootstrap.toast import ToastNotification
import ctypes


class DashboardClass:
    def __init__(self, un, ut, theme, mode):
        self.un = un
        print(un)
        self.theme = theme
        self.mode = mode
        #self.window = ttk.Window(themename=self.theme)
        self.window = Toplevel()
        #self.window = CTkToplevel(fg_color=('#f2f2e9', '#000000'))
        self.window.focus()

        self.total_sum = None
        self.used_sum = None
        set_appearance_mode(self.mode)
        self.window.title("FinTrack")
        self.window.state('zoomed')
        # myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
        # ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        # self.window.iconbitmap('myimages/logo.ico')
        # img = PhotoImage(file='myimages/logo.png')
        # self.window.iconphoto(False, img)

        self.LeftFrame = CTkFrame(self.window)
        self.LeftFrame.configure(fg_color=('#d6d6d2', '#121211'), border_color='#B76E79', border_width=0.5, height=550,
                                 width=250, corner_radius=20)
        self.LeftFrame.place(x=-5, y=210)
        self.createwidgets()

        self.TopFrame = CTkFrame(self.window)
        self.TopFrame.configure(fg_color=('#d6d6d2', '#121211'), border_color='#B76E79', border_width=0.5, width=1210,
                                height=130, corner_radius=20)
        self.TopFrame.place(x=270, y=-15)
        self.createwidgets_tp()
        self.databaseconnection()

        self.date_entry = None
        self.fr = None
        self.scroll_frame2 = None
        self.fr1 = None
        self.charge_subs_entry = None
        self.genre_subs_entry = None
        self.name_subs_entry = None
        self.scroll_frame = None
        self.subs_frame_1()
        self.subs_frame_2()
        self.sumarizer_view()
        self.graph_card_view()
        self.loan_view()
        self.card_view()
        self.used_sum_cc = None
        self.used_sum_db = None
        self.total_sum_db = None
        self.total_sum_cc = None
        self.due_date = None
        self.remind_amt = None
        self.window.focus()
        self.notification_view()
        self.window.bind('<Escape>', lambda e: self.back())

        self.window.mainloop()
# ------------this creates buttons in left frame----------

    def createwidgets(self):

        from Portfolio import PortfolioClass
        port_bg = CTkImage(Image.open("myimages//port.png"), size=(30, 30))
        portfolio_button = CTkButton(self.LeftFrame, text='Portfolio', width=240, height=50, corner_radius=5)
        portfolio_button.configure(anchor='center', fg_color=('#d6d6d2', '#121211'), hover_color=('#333331', '#000000'),
                                   image=port_bg, text_color=('#43605E', '#ffe5d4'), border_color=('#FFFFFF', '#d9b30b')
                                   , font=('sans', 20, 'bold'), border_spacing=5,
                                   command=lambda: PortfolioClass(self.theme, self.un))

        # from Dashboard import DashboardClass
        port_bg = CTkImage(Image.open("myimages//dash.png"), size=(30, 30))
        dashboard_button = CTkButton(self.LeftFrame, text='Dashboard', width=240, height=50, corner_radius=5)
        dashboard_button.configure(anchor='center', fg_color=('#d6d6d2', '#121211'), hover_color=('#333331', '#000000'),
                                   image=port_bg, text_color=('#43605E', '#ffe5d4'), border_color=('#FFFFFF', '#d9b30b')
                                   , font=('sans', 20, 'bold'), border_spacing=5)

        from Loan import LoanClass
        port_bg = CTkImage(Image.open("myimages//loan.png"), size=(30, 30))
        loans_button = CTkButton(self.LeftFrame, text='Loans', width=240, height=50, corner_radius=5)
        loans_button.configure(anchor='center', fg_color=('#d6d6d2', '#121211'), hover_color=('#333331', '#000000'),
                               image=port_bg, text_color=('#43605E', '#ffe5d4'), border_color=('#FFFFFF', '#d9b30b'),
                               font=('sans', 20, 'bold'), border_spacing=5,
                               command=lambda: LoanClass(self.theme, self.un))
        from Card import CardClass
        port_bg = CTkImage(Image.open("myimages//card.png"), size=(30, 30))
        cards_button = CTkButton(self.LeftFrame, text='Cards', width=240, height=50, corner_radius=5)
        cards_button.configure(anchor='center', fg_color=('#d6d6d2', '#121211'), hover_color=('#333331', '#000000'),
                               image=port_bg, text_color=('#43605E', '#ffe5d4'), border_color=('#FFFFFF', '#d9b30b'),
                               font=('sans', 20, 'bold'), border_spacing=5,
                               command=lambda: CardClass(self.theme, self.un))

        from Subscription import SubscriptionClass
        port_bg = CTkImage(Image.open("myimages//subs.png"), size=(30, 30))
        subscription_button = CTkButton(self.LeftFrame, text='Subscription', width=240, height=50, corner_radius=5)
        subscription_button.configure(anchor='center', fg_color=('#d6d6d2', '#121211'),
                                      hover_color=('#333331', '#000000'), image=port_bg,
                                      text_color=('#43605E', '#ffe5d4'), border_color=('#FFFFFF', '#d9b30b')
                                      , font=('sans', 20, 'bold'), border_spacing=5,
                                      command=lambda: SubscriptionClass(self.theme, self.un))

        # home_button.place(x=5, y=50)
        dashboard_button.place(x=5, y=50)
        portfolio_button.place(x=5, y=150)
        # investment_button.place(x=5, y=350)
        loans_button.place(x=5, y=250)
        cards_button.place(x=5, y=350)
        subscription_button.place(x=5, y=450)
# -------------this created the top welcome frame---------

    def createwidgets_tp(self):
        img = CTkImage(Image.open("myimages//wel.png"), size=(400, 100))
        wel = CTkLabel(self.TopFrame, image=img, text='')

        sublabel = CTkLabel(self.TopFrame, text='Review your track and progress', font=('Sans', 18, 'bold'),
                            fg_color='transparent')

        profile_combobox = ttk.Combobox(self.TopFrame, values=['User', 'Change User', 'Log out'])
        profile_combobox.current(0)

        wel.place(x=5, y=8)
        sublabel.place(x=35, y=95)
        profile_combobox.place(x=1300, y=35)
        # sw = CTkSwitch(self.TopFrame, width=20, height=15, command=self.toggle)
        # sw.place(x=1000, y=30)
# --------------this establishes database connection-----
    def databaseconnection(self):
        try:
            self.connection = pymysql.connect(host='localhost', db='finance_manager_db', user='root', password='')
            self.cur = self.connection.cursor()
        except Exception as e:
            messagebox.showerror("Error", "Database connection error \n" + str(e), parent=self.window)
# ------- this fetches list for display of card number to select------

    def subs_frame_1(self):
        self.scroll_frame = CTkFrame(self.window, width=350, height=300, fg_color=('#d6d6d2', '#121211'),
                                     border_color='#B76E79', border_width=1, corner_radius=5)
        self.scroll_frame.place(x=290, y=130)

    def subs_frame_2(self):
        self.scroll_frame2 = CTkFrame(self.window, width=250, height=300, fg_color=('#d6d6d2', '#121211'),
                                      border_color='#B76E79', border_width=1, corner_radius=5)
        self.scroll_frame2.place(x=290, y=450)

    def sumarizer_view(self):

        sum_frame = CTkFrame(self.window, width=300, height=300, fg_color=('#f2f2e9', '#000000'),
                             border_color='#B76E79', border_width=1, corner_radius=5)
        sum_frame.place(x=660, y=130)
        year_exp = 0
        month_exp = 0
        week_exp = 0
        try:
            qry = " select * from subscription where user_name=%s"
            rowcount = self.cur.execute(qry, self.un)
            data = self.cur.fetchall()
            for i in range(len(data)):
                if data[i][4] == 'yearly':
                    year_exp += int(data[i][3])
                elif data[i][4] == 'monthly':
                    month_exp += int(data[i][3])
                elif data[i][4] == 'weekly':
                    week_exp += int(data[i][3])
            lable1 = CTkLabel(sum_frame, fg_color=('#f2f2e9', '#000000'),
                              font=('sans', 24,), width=40, text_color=('#43605E', '#ffe5d4'),
                              text='Subscription\nSummarizer')
            lable1.place(x=30, y=20)
            lable1 = CTkLabel(sum_frame, fg_color=('#f2f2e9', '#000000'),
                              font=('sans', 16,), width=40, text_color=('#43605E', '#ffe5d4'),
                              text='Total\nSubscriptions')
            lable1.place(x=50, y=110)
            label2 = CTkLabel(sum_frame, fg_color=('#f2f2e9', '#000000'),
                              font=('sans', 46,), width=40, text_color=('#43605E', '#ffe5d4'),
                              text=str(len(data)))
            label2.place(x=60, y=170)
            lable3 = CTkLabel(sum_frame, fg_color=('#f2f2e9', '#000000'),
                              font=('sans', 12,), width=40, text_color=('#43605E', '#ffe5d4'),
                              text='Expenditure pattern --->')
            lable3.place(x=70, y=270)

        except Exception as e:
            messagebox.showerror("Error", "Error while fetching Data  : \n" + str(e), parent=self.window)

        frameChartsLT = CTkFrame(self.window)
        frameChartsLT.configure(height=250)
        frameChartsLT.place(x=860, y=130)

        stockListExp = ['Yearly', 'Monthly', 'Weekly']
        stockSplitExp = [year_exp, month_exp, week_exp]

        fig = Figure()  # create a figure object
        fig.set_size_inches(3, 3, forward=True)

        ax = fig.add_subplot(111)  # add an Axes to the figure
        _, texts, autotexts = ax.pie(stockSplitExp, radius=1, labels=stockListExp, autopct='%0.2f%%')
        if self.theme == 'cyborg':
            fig.patch.set_facecolor('xkcd:black')

            for text in texts:
                text.set_color('grey')
            for ins in autotexts:
                ins.set_color('white')

        if self.theme == 'mylight':
            fig.patch.set_facecolor(color='#f2f2e9')

            for text in texts:
                text.set_color('grey')
            for ins in autotexts:
                ins.set_color('white')

        chart1 = FigureCanvasTkAgg(fig, frameChartsLT)
        chart1.get_tk_widget().pack()

    def loan_view(self):
        lb = CTkLabel(self.scroll_frame2, text='Loan Overview',
                      fg_color=('#d6d6d2', '#121211'),
                      font=('sans', 24, 'bold'), width=40, text_color=('#43605E', '#ffe5d4'))
        lb.place(x=30, y=20)

        try:
            qry = " select * from loan where user_name=%s"
            rowcount = self.cur.execute(qry, self.un)
            data = self.cur.fetchall()
            ls = []
            for i in range(len(data)):
                ls.append(data[i][6])
            ls = [str(ele) for ele in ls]
            ls = ','.join(ls)

            lable1 = CTkLabel(self.scroll_frame2, fg_color=('#d6d6d2', '#121211'),
                              font=('sans', 16,), width=40, text_color=('#43605E', '#ffe5d4'),
                              text='Total\nLoans')
            lable1.place(x=20, y=110)
            label2 = CTkLabel(self.scroll_frame2, fg_color=('#d6d6d2', '#121211'),
                              font=('sans', 46,), width=40, text_color=('#43605E', '#ffe5d4'),
                              text=str(len(data)))
            label2.place(x=80, y=100)

            lable3 = CTkLabel(self.scroll_frame2, fg_color=('#d6d6d2', '#121211'),
                              font=('sans', 16,), width=40, text_color=('#43605E', '#ffe5d4'),
                              text='Emi')
            lable3.place(x=20, y=170)
            label4 = CTkLabel(self.scroll_frame2, fg_color=('#d6d6d2', '#121211'),
                              font=('sans', 16,), width=40, text_color=('#43605E', '#ffe5d4'),
                              text=ls)
            label4.place(x=80, y=170)

        except Exception as e:
            messagebox.showerror("Error", "Error while fetching Data  : \n" + str(e), parent=self.window)

    def graph_card_view(self):
        lb = CTkLabel(self.scroll_frame, text='Card Expenditure Overview',
                      fg_color=('#d6d6d2', '#121211'),
                      font=('sans', 24, 'bold'), width=40, text_color=('#43605E', '#ffe5d4'))
        lb.place(x=15, y=20)
        try:
            qry = " select total_limit, used_limit from cards where card_type='Credit' and user_name=%s"
            rowcount = self.cur.execute(qry, self.un)
            data = self.cur.fetchall()
            self.total_sum_cc = 0
            self.used_sum_cc = 0
            for t in data:
                self.total_sum_cc += t[0]
                self.used_sum_cc += t[1]

        except Exception as e:
            messagebox.showerror("Error", "Error while fetching Data  : \n"+str(e), parent=self.window)
        per = (self.used_sum_cc/self.total_sum_cc)*100

        meter = ttb.Floodgauge(self.scroll_frame, mode='determinate', maximum=self.total_sum_cc, value=self.used_sum_cc,
                               length=300, orient='vertical')
        meter.place(x=40, y=100)
        lb = CTkLabel(self.scroll_frame, text='Credit limit:\n' + str(self.total_sum_cc),
                      fg_color=('#d6d6d2', '#121211'),
                      font=('sans', 16,), width=40, text_color=('#43605E', '#ffe5d4'))
        lb.place(x=80, y=100)

        lb2 = CTkLabel(self.scroll_frame, text='Limit Used:\n' + str(self.used_sum_cc),
                       fg_color=('#d6d6d2', '#121211'),
                       font=('sans', 16,), width=40, text_color=('#43605E', '#ffe5d4'))
        lb2.place(x=80, y=170)

        lb2 = CTkLabel(self.scroll_frame, text=str(round(per, 2)) + ' % Used',
                       fg_color=('#d6d6d2', '#121211'),
                       font=('sans', 16,), width=40, text_color=('#43605E', '#ffe5d4'))
        lb2.place(x=80, y=240)
        try:
            qry = " select total_limit, used_limit from cards where card_type='Debit' and user_name=%s"
            rowcount = self.cur.execute(qry, self.un)
            data = self.cur.fetchall()
            self.total_sum_db = 0
            self.used_sum_db = 0
            for t in data:
                self.total_sum_db += t[0]
                self.used_sum_db += t[1]
        except Exception as e:
            messagebox.showerror("Error", "Error while fetching Data  : \n"+str(e), parent=self.window)
        per2 = ((self.used_sum_db / self.total_sum_db) * 100)
        meter2 = ttb.Floodgauge(self.scroll_frame, mode='determinate', maximum=self.total_sum_db,
                                value=self.used_sum_db,
                                length=300, orient='vertical')
                               # text=str('{:,}'.format(self.used_sum_cc)),

        meter2.place(x=230, y=100)
        lb = CTkLabel(self.scroll_frame, text='Debit limit:\n' + str(self.total_sum_db),
                      fg_color=('#d6d6d2', '#121211'),
                      font=('sans', 16,), width=40, text_color=('#43605E', '#ffe5d4'))
        lb.place(x=230, y=100)

        lb2 = CTkLabel(self.scroll_frame, text='Limit Used:\n' + str(self.used_sum_db),
                       fg_color=('#d6d6d2', '#121211'),
                       font=('sans', 16,), width=40, text_color=('#43605E', '#ffe5d4'))
        lb2.place(x=230, y=170)

        lb3 = CTkLabel(self.scroll_frame, text=str(round(per2, 2)) + ' % Used',
                       fg_color=('#d6d6d2', '#121211'),
                       font=('sans', 16,), width=40, text_color=('#43605E', '#ffe5d4'))
        lb3.place(x=230, y=240)

    def card_view(self):
        card_frame = CTkFrame(self.window, width=470, height=300, fg_color=('#d6d6d2', '#121211'),
                              border_color='#B76E79', border_width=1, corner_radius=5)
        card_frame.place(x=560, y=450)
        lb = CTkLabel(card_frame, text='Card Overview',
                      fg_color=('#d6d6d2', '#121211'),
                      font=('sans', 24, 'bold'), width=40, text_color=('#43605E', '#ffe5d4'))
        lb.place(x=30, y=15)
        lb = CTkLabel(card_frame, text='Card Holder',
                      fg_color=('#d6d6d2', '#121211'),
                      font=('sans', 18, 'bold'), width=40, text_color=('#43605E', '#ffe5d4'))
        lb.place(x=30, y=50)
        lb = CTkLabel(card_frame, text='Card Number',
                      fg_color=('#d6d6d2', '#121211'),
                      font=('sans', 18, 'bold'), width=40, text_color=('#43605E', '#ffe5d4'))
        lb.place(x=200, y=50)
        lb = CTkLabel(card_frame, text='Bank Name',
                      fg_color=('#d6d6d2', '#121211'),
                      font=('sans', 18, 'bold'), width=40, text_color=('#43605E', '#ffe5d4'))
        lb.place(x=350, y=50)
        ls_name = []
        ls_num = []
        ls_bank_name = []
        try:
            qry = " select card_num, card_name, bank_name from cards where user_name=%s"
            rowcount = self.cur.execute(qry, self.un)
            data = self.cur.fetchall()
            for t in data:
                ls_num.append(t[0])
                ls_name.append(t[1])
                ls_bank_name.append(t[2])
            print(ls_num, "\n", ls_bank_name, "\n", ls_name)
        except Exception as e:
            messagebox.showerror("Error", "Error while fetching Data  : \n"+str(e), parent=self.window)
        y_diff = 0
        for ele in ls_name:
            lb = CTkLabel(card_frame, text=ele,
                          fg_color=('#d6d6d2', '#121211'),
                          font=('sans', 16, 'bold'), width=40, text_color=('#43605E', '#ffe5d4'))
            lb.place(x=30, y=80 + y_diff)
            y_diff += 25
        y_diff = 0
        for ele in ls_num:
            lb = CTkLabel(card_frame, text=ele,
                          fg_color=('#d6d6d2', '#121211'),
                          font=('sans', 16), width=40, text_color=('#43605E', '#ffe5d4'))
            lb.place(x=200, y=80 + y_diff)
            y_diff += 25
        y_diff = 0
        for ele in ls_bank_name:
            lb = CTkLabel(card_frame, text=ele,
                          fg_color=('#d6d6d2', '#121211'),
                          font=('sans', 16), width=40, text_color=('#43605E', '#ffe5d4'))
            lb.place(x=350, y=80 + y_diff)
            y_diff += 25

    def noti_delay_view(self):
        try:
            qry = " select * from notification where user_name=%s"
            rowcount = self.cur.execute(qry, self.un)
            data = self.cur.fetchall()
            #print(data)
        except Exception as e:
            messagebox.showerror("Error", "Error while fetching Data  : \n"+str(e), parent=self.window)
        toast = ToastNotification(
            title="Pending Amount",
            message= str(data[0][1]) + " is to be paid by " + data[0][2],
            duration=3000, alert=True, icon='')
        toast.show_toast()

    def notification_view(self):
        noti_frame = CTkFrame(self.window, fg_color=('#d6d6d2', '#121211'), width=250, height=300,
                              border_color='#B76E79', border_width=1, corner_radius=5)
        noti_frame.place(x=1050, y=450)
        lb = CTkLabel(noti_frame, text='Reminder',
                      fg_color=('#d6d6d2', '#121211'),
                      font=('sans', 24, 'bold'), width=40, text_color=('#43605E', '#ffe5d4'))
        lb.place(x=30, y=20)
        remind_amt = CTkLabel(noti_frame, text='Enter Amount', text_color=('#43605E', '#ffe5d4'),
                              font=('sans', 18))
        remind_amt.place(x=20, y=60)
        self.remind_amt = CTkEntry(noti_frame, placeholder_text='Amount: ', fg_color='#faf9f5',
                                   text_color='black')
        self.remind_amt.place(x=20, y=90)
        due_date = CTkLabel(noti_frame, text='Enter Due period', text_color=('#43605E', '#ffe5d4'),
                            font=('sans', 20))
        due_date.place(x=20, y=130)
        self.due_date = CTkEntry(noti_frame, placeholder_text='Due Period: ', fg_color='#faf9f5',
                                 text_color='black')
        self.due_date.place(x=20, y=160)
        save_button = CTkButton(noti_frame, text='Save', width=115, height=30, corner_radius=5,
                                fg_color=('#d6d6d2', '#121211'),
                                font=('sans', 14,), border_color='#B76E79', border_width=1,
                                text_color=('#43605E', '#ffe5d4'), hover_color=('#333331', '#000000'),
                                command=lambda: self.add_noti_data())
        save_button.place(x=20, y=210)
        add_button = CTkButton(noti_frame, text='Click to Check Amount', width=115, height=30, corner_radius=5,
                               fg_color=('#d6d6d2', '#121211'),
                               font=('sans', 14,), border_color='#B76E79', border_width=1,
                               text_color=('#43605E', '#ffe5d4'), hover_color=('#333331', '#000000'),
                               command=lambda: self.noti_delay_view())
        add_button.place(x=20, y=250)

    def add_noti_data(self):
        try:
            qry = 'Update notification set amount=%s, due_date=%s where user_name=%s'
            rowcount = self.cur.execute(qry, (self.remind_amt.get(), self.due_date.get(), self.un))
            self.connection.commit()
            if rowcount == 2:
                messagebox.showinfo("Success", "Data Added Successfully", parent=self.window)
                self.remind_amt.delete(0, END)
                self.due_date.delete(0, END)
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
                ls.append([myrow[1], myrow[2], myrow[3], myrow[4], myrow[5], myrow[6]])
        except Exception as e:
            messagebox.showerror("Error", "Error while fetching Data  : \n" + str(e), parent=self.window)

        headings = ['Payment', 'Date', 'Card Number', 'Credit/Debit', 'Amount', 'Payment ID']
        pdf = my_cust_PDF()
        pdf.print_chapter(ls, headings)

        pdf.output('pdf_file1.pdf')
        os.system('explorer.exe "pdf_file1.pdf"')

    # def toggle(self):
    #     if self.mode == 'dark':
    #         self.mode = 'light'
    #         set_appearance_mode('light')
    #     elif self.mode == 'light':
    #         self.mode = 'dark'
    #         set_appearance_mode('dark')
    #     # if self.theme == 'cyborg' and self.mode == 'dark':
    #     #     self.theme = 'mylight'
    #     #     self.mode = 'light'
    #     # else:
    #     #     self.theme = 'cyborg'
    #     #     self.mode = 'dark'
    #     # self.window.destroy()
    #     # Work(self.theme, self.mode)

if __name__ == '__main__':
    obj = DashboardClass()
