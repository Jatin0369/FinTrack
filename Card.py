from tkinter import *
from tkinter import messagebox
import pymysql as pymysql
from customtkinter import *
from PIL import Image
import ttkbootstrap as ttb
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.constants import *
import webbrowser
from pdf import my_cust_PDF


class CardClass:
    def __init__(self, mode, un):
        self.un = un

        self.used_sum_cc = None
        self.mode = mode
        set_appearance_mode(mode)
        # 121211
        self.window = CTkToplevel(fg_color=('#f2f2e9', '#000000'))
        self.window.title("Subscription")
        self.window.overrideredirect(True)

        self.window.minsize(1200, 780)
        self.window.geometry("1514x990+338+30")

        self.TopFrame = CTkFrame(self.window)
        self.TopFrame.configure(fg_color=('#d6d6d2', '#121211'), border_color='#B76E79', border_width=0.5, width=1210,
                                height=130, corner_radius=20)
        self.TopFrame.place(x=0, y=-15)
        self.createwidgets_tp()

        self.CardFrame = CTkFrame(self.window)
        self.var = None
        self.copyVar = None
        self.var2 = None
        self.copyVar2 = None
        self.var3 = None
        self.copyVar3 = None
        self.var4 = None
        self.copyVar4 = None
        self.input_card4 = None
        self.input_card3 = None
        self.input_card2 = None
        self.input_card1 = None
        self.button = None
        self.card4 = None
        self.card3 = None
        self.card2 = None
        self.card1 = None
        self.cur = None
        self.connection = None
        self.input_max_limit = None
        self.card_type = None
        self.total_sum_cc = None
        self.total_sum_db = None
        #self.used_sum = None

        self.databaseconnection()
        self.createcard()

        self.CardFrame.configure(width=1210, height=170, fg_color=('#d6d6d2', '#121211'), border_color='#B76E79',
                                 border_width=0.5, corner_radius=20)
        self.CardFrame.place(x=0, y=125)

        self.OptionsFrame = CTkFrame(self.window)
        self.del_data = None
        self.input_amount = None
        self.input_card_type = None
        self.input_date = None
        self.input_payment = None
        self.tree = None
        self.del_card = None
        self.cur = None
        self.connection = None
        self.input_bank_name = None
        self.input_pin_num = None
        self.input_cvv_num = None
        self.input_phn_num = None
        self.input_card_name = None
        self.input_card_num = None
        self.check = 0
        self.transactiontable()
        self.databaseconnection()
        self.getalldata()
        self.OptionsFrame.configure(border_color=('#f2f2e9', '#000000'), border_width=0.5, fg_color='transparent',
                                    height=100, width=490)
        self.OptionsFrame.place(x=730, y=688)

        ad_cd = CTkImage(Image.open("myimages//button_add-card.png"), size=(115, 30))
        add_button = CTkButton(self.OptionsFrame, text='', width=115, height=30, corner_radius=5, anchor='center',
                               fg_color='transparent', image=ad_cd, hover_color=('#f2f2e9', '#000000'),
                               command=lambda: self.addcard())
        add_button.place(x=0, y=50)

        dl_cd = CTkImage(Image.open("myimages//button_delete-card.png"), size=(115, 30))
        del_button = CTkButton(self.OptionsFrame, text='', width=115, height=30, corner_radius=5, anchor='center',
                               fg_color='transparent', image=dl_cd, hover_color=('#f2f2e9', '#000000'),
                               command=lambda: self.deletecard())
        del_button.place(x=120, y=50)

        ad_tr = CTkImage(Image.open("myimages//button_add-transaction.png"), size=(115, 30))
        add_button = CTkButton(self.OptionsFrame, text='', width=115, height=30, corner_radius=5, anchor='center',
                               fg_color='transparent', image=ad_tr, hover_color=('#f2f2e9', '#000000'),
                               command=lambda: self.addtransaction())
        add_button.place(x=240, y=50)

        ad_cd = CTkImage(Image.open("myimages//button_delete-transaction.png"), size=(115, 30))
        add_button = CTkButton(self.OptionsFrame, text='', width=115, height=30, corner_radius=5, anchor='center',
                               fg_color='transparent', image=ad_cd, hover_color=('#f2f2e9', '#000000'),
                               command=lambda: self.deletetransaction())
        add_button.place(x=360, y=50)

        self.offerframe = CTkFrame(self.window, width=470, height=150, fg_color=('#d6d6d2', '#121211'),
                                   border_color='#B76E79', border_width=1, corner_radius=20)
        self.offerframe.place(x=740, y=560)
        self.graph()
        self.window.bind('<Escape>', lambda e: self.back())
        self.window.focus()
        self.offers()
        self.window.mainloop()

    def back(self):
        self.window.destroy()

    def createwidgets_tp(self):

        img = CTkImage(Image.open("myimages//wel.png"), size=(400, 100))
        wel = CTkLabel(self.TopFrame, image=img, text='')

        sublabel = CTkLabel(self.TopFrame, text='Review your Card track and progress', font=('Sans', 18, 'bold'),
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
# --------------this establishes database connection-----
    def databaseconnection(self):
        try:
            self.connection = pymysql.connect(host='localhost', db='finance_manager_db', user='root', password='')
            self.cur = self.connection.cursor()
        except Exception as e:
            messagebox.showerror("Error", "Database connection error \n" + str(e), parent=self.window)
# ------- this fetches list for display of card number to select------

    def fetchdatacard(self):
        try:
            qry = " select card_num from cards where user_name=%s"
            rowcount = self.cur.execute(qry, self.un)
            data = self.cur.fetchall()
            data = list(data)
            ls = list()
            for item in data:
                ls.extend(item)
            return ls

        except Exception as e:
            messagebox.showerror("Error", "Error while fetching Data  : \n" + str(e), parent=self.window)
# -------- this displays the card details ---------------

    def fetchdata(self, card_num, card_frame):
        try:
            qry = " select * from cards where card_num=%s and user_name=%s"
            rowcount = self.cur.execute(qry, (card_num, self.un))
            data = self.cur.fetchone()
            for widget in card_frame.winfo_children():
                widget.destroy()
            if data:
                r1 = [data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9]]
                bank_label = CTkLabel(card_frame, text=r1[5], font=('Sans', 26, 'bold'), text_color='#f5edda')
                bank_label.place(x=30, y=5)
                name = CTkLabel(card_frame, text=r1[1], font=('Sans', 18, 'italic', 'bold'), text_color='#f2e70a')
                name.place(x=30, y=50)
                total = CTkLabel(card_frame, text="Total Limit\n" + str(r1[7]), font=('Sans', 14, 'bold'),
                                 text_color='#4bd12a')
                total.place(x=30, y=90)
                avail = CTkLabel(card_frame, text="Limit Used\n" + str(r1[8]), font=('Sans', 14, 'bold'),
                                 text_color='#b00951')
                avail.place(x=140, y=90)
            else:
                messagebox.showwarning("Empty", "No Record Found", parent=self.window)
        except Exception as e:
            messagebox.showerror("Error", "Error while fetching Data  : \n" + str(e), parent=self.window)
# ------------- this creates cards fram3------------

    def createcard(self):
        self.card1 = CTkFrame(self.CardFrame)
        self.card1.configure(height=140, width=240, fg_color='#a1a158', border_color='#f2bf30', border_width=1)

        self.card2 = CTkFrame(self.CardFrame)
        self.card2.configure(height=140, width=240, fg_color='#58a895', border_color='#f2bf30', border_width=1)

        self.card3 = CTkFrame(self.CardFrame)
        self.card3.configure(height=140, width=240, fg_color='#a88958', border_color='#f2bf30', border_width=1)

        self.card4 = CTkFrame(self.CardFrame)
        self.card4.configure(height=140, width=240, fg_color='#815fad', border_color='#f2bf30', border_width=1)

        cd_bg = CTkImage(Image.open("myimages//button_show-card (1).png"), size=(90, 30))
        self.button = CTkButton(self.CardFrame, text='', width=80, height=35, corner_radius=5)
        self.button.configure(anchor='center', fg_color='transparent', image=cd_bg, hover_color=('#d6d6d2', '#121211'),
                              command=lambda: self.carddisplay())

        self.card1.place(x=20, y=15)
        self.card2.place(x=295, y=15)
        self.card3.place(x=570, y=15)
        self.card4.place(x=845, y=15)
        self.button.place(x=1100, y=15)
# --------this places the cards on to frame and customizes it---------

    def carddisplay(self):

        small_window = CTkToplevel(self.window)
        small_window.title('Add Transaction')
        small_window.configure(fg_color=('#d6d6d2', '#121211'))
        small_window.after(10, small_window.lift)
        width = 400
        height = 400
        small_window.minsize(width, height)
        x = small_window.winfo_screenwidth() // 2 - width // 2
        y = small_window.winfo_screenheight() // 2 - height // 2
        small_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        y_diff = 40
        ls = self.fetchdatacard()

        self.var = StringVar(value=ls[0])
        card1_lb = CTkLabel(small_window, text='Card 1 Number: ', text_color=('#43605E', '#ffe5d4'))
        card1_lb.place(x=5, y=5)
        self.input_card1 = ttb.Combobox(small_window, values=ls, textvariable=self.var, state='readonly')
        self.input_card1.place(x=130, y=5)
        self.copyVar = self.var.get()

        self.var2 = StringVar(value=ls[1])
        card2_lb = CTkLabel(small_window, text='Card 2 Number: ', text_color=('#43605E', '#ffe5d4'))
        card2_lb.place(x=5, y=10 + y_diff)
        self.input_card2 = ttb.Combobox(small_window, values=ls, textvariable=self.var2, state='readonly')
        self.input_card2.place(x=130, y=20 + y_diff)
        self.copyVar2 = self.var2.get()

        self.var3 = StringVar(value=ls[2])
        card3_lb = CTkLabel(small_window, text='Card 3 Number: ', text_color=('#43605E', '#ffe5d4'))
        card3_lb.place(x=5, y=10 + y_diff * 2)
        self.input_card3 = ttb.Combobox(small_window, values=ls, textvariable=self.var3, state='readonly')
        self.input_card3.place(x=130, y=35 + y_diff * 2)
        self.copyVar3 = self.var3.get()

        self.var4 = StringVar(value=ls[3])
        card4_lb = CTkLabel(small_window, text='Card 4 Number: ', text_color=('#43605E', '#ffe5d4'))
        card4_lb.place(x=5, y=10 + y_diff * 3)
        self.input_card4 = ttb.Combobox(small_window, values=ls, textvariable=self.var4, state='readonly')
        self.input_card4.place(x=130, y=50 + y_diff * 3)
        self.copyVar4 = self.var4.get()

        save_button = CTkButton(small_window, text='Save')
        save_button.configure(anchor='center', fg_color=('#d6d6d2', '#121211'), hover_color=('#333331', '#000000'),
                              text_color=('#43605E', '#ffe5d4'),
                              command=lambda: self.show())
        save_button.place(x=110, y=5 + y_diff * 5)
        small_window.mainloop()
# ---------this calls the card details----------

    def show(self):
        self.check = 1
        self.copyVar = self.var.get()
        self.copyVar2 = self.var2.get()
        self.copyVar3 = self.var3.get()
        self.copyVar4 = self.var4.get()
        self.fetchdata(self.copyVar, self.card1)
        self.fetchdata(self.copyVar2, self.card2)
        self.fetchdata(self.copyVar3, self.card3)
        self.fetchdata(self.copyVar4, self.card4)

# ------ data fetch-------------

    def fetchdata_2(self, id):
        try:
            qry = " select * from transactions where payment_id=%s"
            rowcount = self.cur.execute(qry, id)
            data = self.cur.fetchone()
            if data:
                r1 = [data[1], data[2], data[3], data[4], data[5], data[6]]
                self.tree.insert("", END, values=r1)
            else:
                messagebox.showwarning("Empty", "No Record Found", parent=self.window)
        except Exception as e:
            messagebox.showerror("Error", "Error while fetching Data  : \n"+str(e), parent=self.window)

    def getalldata(self):
        try:
            qry = " select * from transactions where user_name=%s"
            rowcount = self.cur.execute(qry, self.un)
            data = self.cur.fetchall()
            if data:
                for myrow in data:
                    r1 = [myrow[1], myrow[2], myrow[3], myrow[4], myrow[5], myrow[6]]
                    self.tree.insert("", END, values=r1)
            else:
                messagebox.showwarning("Empty", "No Record Found", parent=self.window)
        except Exception as e:
            messagebox.showerror("Error", "Error while fetching Data  : \n"+str(e), parent=self.window)

    def addcard(self):
        small_window = CTkToplevel(self.window)
        small_window.title('Add Card')
        small_window.configure(fg_color=('#d6d6d2', '#121211'))
        small_window.after(10, small_window.lift)
        width = 400
        height = 400
        small_window.minsize(width, height)
        x = small_window.winfo_screenwidth() // 2 - width // 2
        y = small_window.winfo_screenheight() // 2 - height // 2
        small_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        y_diff = 40

        card_num = CTkLabel(small_window, text='Card Number: ', text_color=('#43605E', '#ffe5d4'))
        card_num.place(x=5, y=5)
        self.input_card_num = CTkEntry(small_window, placeholder_text='Enter Card Number: ', fg_color='#faf9f5',
                                       text_color='black')
        self.input_card_num.place(x=120, y=5)

        card_name = CTkLabel(small_window, text='Registered Name: ', text_color=('#43605E', '#ffe5d4'))
        card_name.place(x=5, y=5 + y_diff)
        self.input_card_name = CTkEntry(small_window, placeholder_text='Enter Registered Name: ', fg_color='#faf9f5',
                                        text_color='black')
        self.input_card_name.place(x=120, y=5 + y_diff)

        phn_num = CTkLabel(small_window, text='Phone Number: ', text_color=('#43605E', '#ffe5d4'))
        phn_num.place(x=5, y=5 + y_diff*2)
        self.input_phn_num = CTkEntry(small_window, placeholder_text='Enter Phone Number: ', fg_color='#faf9f5',
                                      text_color='black')
        self.input_phn_num.place(x=120, y=5 + y_diff*2)

        cvv_num = CTkLabel(small_window, text='CVV Number: ', text_color=('#43605E', '#ffe5d4'))
        cvv_num.place(x=5, y=5 + y_diff*3)
        self.input_cvv_num = CTkEntry(small_window, placeholder_text='Enter CVV Number: ', fg_color='#faf9f5',
                                      text_color='black')
        self.input_cvv_num.place(x=120, y=5 + y_diff*3)

        pin_num = CTkLabel(small_window, text='Pin Number: ', text_color=('#43605E', '#ffe5d4'))
        pin_num.place(x=5, y=5 + y_diff*4)
        self.input_pin_num = CTkEntry(small_window, placeholder_text='Enter Pin Number: ', fg_color='#faf9f5',
                                      text_color='black')
        self.input_pin_num.place(x=120, y=5 + y_diff*4)

        bank_name = CTkLabel(small_window, text='Bank Name: ', text_color=('#43605E', '#ffe5d4'))
        bank_name.place(x=5, y=5 + y_diff*5)
        self.input_bank_name = CTkEntry(small_window, placeholder_text='Enter Bank Name: ', fg_color='#faf9f5',
                                        text_color='black')
        self.input_bank_name.place(x=120, y=5 + y_diff*5)
        
        max_limit = CTkLabel(small_window, text='Bank Name: ', text_color=('#43605E', '#ffe5d4'))
        max_limit.place(x=5, y=5 + y_diff*6)
        self.input_max_limit = CTkEntry(small_window, placeholder_text='Enter Bank Name: ', fg_color='#faf9f5',
                                        text_color='black')
        self.input_max_limit.place(x=120, y=5 + y_diff*6)

        card_type = CTkLabel(small_window, text='Card type: ', text_color=('#43605E', '#ffe5d4'))
        card_type.place(x=5, y=5 + y_diff*7)
        self.card_type = ttb.Combobox(small_window, values=['Credit', 'Debit'], width=15)
        self.card_type.current(0)
        self.card_type.place(x=160, y=30 + y_diff*8)

        save_button = CTkButton(small_window, text='Save')
        save_button.configure(anchor='center', fg_color=('#d6d6d2', '#121211'), hover_color=('#333331', '#000000'),
                              text_color=('#43605E', '#ffe5d4'),
                              command=lambda: self.addcarddata(small_window))
        save_button.place(x=120, y=5 + y_diff*8)

        small_window.mainloop()

    def clearpagecard(self):
        self.input_card_num.delete(0, END)
        self.input_card_name.delete(0, END)
        self.input_phn_num.delete(0, END)
        self.input_cvv_num.delete(0, END)
        self.input_pin_num.delete(0, END)
        self.input_bank_name.delete(0, END)

    def clearpagetransaction(self):
        self.input_payment.delete(0, END)
        self.input_card_num.delete(0, END)
        self.input_amount.delete(0, END)

    def addcarddata(self, small_window):
        try:
            qry = 'insert into cards values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            rowcount = self.cur.execute(qry, (self.un,
                                              self.input_card_num.get(), self.input_card_name.get(),
                                              self.input_phn_num.get(), self.input_cvv_num.get(),
                                              self.input_pin_num.get(), self.input_bank_name.get(),
                                              self.card_type.get(), self.input_max_limit.get(), 0))
            self.connection.commit()
            if rowcount == 1:
                messagebox.showinfo("Success", "Card Data Added Successfully", parent=small_window)
                self.clearpagecard()
        except Exception as e:
            messagebox.showerror("Error", "Insertion Error : \n" + str(e), parent=small_window)

    def deletecard(self):
        pass
        small_window = CTkToplevel(self.window)
        small_window.title('Delete Card')
        small_window.configure(fg_color=('#d6d6d2', '#121211'))
        small_window.after(10, small_window.lift)
        width = 400
        height = 400
        small_window.minsize(width, height)
        x = small_window.winfo_screenwidth() // 2 - width // 2
        y = small_window.winfo_screenheight() // 2 - height // 2
        small_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        card_num = CTkLabel(small_window, text='Card Number: ', text_color=('#43605E', '#ffe5d4'))
        card_num.place(x=5, y=20)
        self.del_card = CTkEntry(small_window, placeholder_text='Enter Card Number: ', fg_color='#faf9f5',
                                 text_color='black')
        self.del_card.place(x=120, y=20)

        delete_button = CTkButton(small_window, text='Delete')
        delete_button.configure(anchor='center', fg_color=('#d6d6d2', '#121211'), hover_color=('#333331', '#000000'),
                                text_color=('#43605E', '#ffe5d4'),
                                command=lambda: self.deletecarddata(small_window))
        delete_button.place(x=120, y=60)

        small_window.mainloop()

    def deletecarddata(self, small_window):
        ans = messagebox.askquestion("Confirmation", "Are you sure to delete ??", parent=small_window)
        if ans == "yes":
            try:
                qry = "delete from cards where card_num=%s and user_name=%s"
                rowcount = self.cur.execute(qry, (self.del_card.get(), self.un))
                self.connection.commit()
                if rowcount == 1:
                    messagebox.showinfo("Success", "Card Data Deleted Successfully", parent=small_window)
                    self.del_card.delete(0, END)
            except Exception as e:
                messagebox.showerror("Error", "Deletion Error : \n" + str(e), parent=small_window)

    def transactiontable(self):
        columns = ('Payment', 'Date', 'Card Number', 'Credit/Debit', 'Amount', 'Payment ID')

        self.style = ttb.Style()
        if self.mode == 'mylight':
            self.style.configure("Treeview", background="#d6d6d2", foreground="#43605E", font=('Sans', 11))
        else:
            self.style.configure("Treeview", background="#000000", foreground="#43605E", font=('Sans', 11))
        self.style.configure("Treeview", rowheight=60)
        self.style.configure("Treeview.Heading", font=('Sans', 13, 'bold'), background="#a6a6a2",
                             foreground="#073602")

        self.tree = ttb.Treeview(self.window, columns=columns, show='headings')
        self.tree.column('#0', width=270, minwidth=270)
        self.tree.column('Payment', width=150, minwidth=70, stretch=NO, anchor='center')
        self.tree.column('Date', width=120, minwidth=70, stretch=NO, anchor='center')
        self.tree.column('Card Number', width=150, minwidth=70, stretch=NO, anchor='center')
        self.tree.column('Credit/Debit', width=140, minwidth=70, stretch=NO, anchor='center')
        self.tree.column('Amount', width=150, minwidth=70, stretch=NO, anchor='center')
        self.tree.column('Payment ID', width=90, minwidth=70, anchor='center')
        # define headings
        self.tree.heading('Payment', text='Merchant', anchor='center')
        self.tree.heading('Date', text='Date', anchor='center')
        self.tree.heading('Card Number', text='Card Number', anchor='center')
        self.tree.heading('Credit/Debit', text='Credit/Debit', anchor='center')
        self.tree.heading('Amount', text='Amount', anchor='center')
        self.tree.heading('Payment ID', text='Payment ID', anchor='center')

        self.tree.place(x=3, y=385, width=900, height=600)

    def addtransaction(self):
        small_window = CTkToplevel(self.window)
        small_window.title('Add Transaction')
        small_window.configure(fg_color=('#d6d6d2', '#121211'))
        small_window.after(10, small_window.lift)
        width = 400
        height = 400
        small_window.minsize(width, height)
        x = small_window.winfo_screenwidth() // 2 - width // 2
        y = small_window.winfo_screenheight() // 2 - height // 2
        small_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        y_diff = 40

        payment = CTkLabel(small_window, text='Merchant Name: ', text_color=('#43605E', '#ffe5d4'))
        payment.place(x=5, y=5)
        self.input_payment = CTkEntry(small_window, placeholder_text='Enter Merchant Name: ', fg_color='#faf9f5',
                                      text_color='black')
        self.input_payment.place(x=120, y=5)

        date = CTkLabel(small_window, text='Date: ', text_color=('#43605E', '#ffe5d4'))
        date.place(x=5, y=5 + y_diff)
        self.input_date = ttb.DateEntry(small_window, dateformat='%Y-%m-%d', firstweekday=2, width=15, bootstyle='info')
        self.input_date.place(x=150, y=13 + y_diff)

        card_num = CTkLabel(small_window, text='Card Number: ', text_color=('#43605E', '#ffe5d4'))
        card_num.place(x=5, y=5 + y_diff * 2)
        self.input_card_num = CTkEntry(small_window, placeholder_text='Enter Card Number: ', fg_color='#faf9f5',
                                       text_color='black')
        self.input_card_num.place(x=120, y=5 + y_diff * 2)

        amount = CTkLabel(small_window, text='Amount: ', text_color=('#43605E', '#ffe5d4'))
        amount.place(x=5, y=5 + y_diff * 3)
        self.input_amount = CTkEntry(small_window, placeholder_text='Enter Amount: ', fg_color='#faf9f5',
                                     text_color='black')
        self.input_amount.place(x=120, y=5 + y_diff * 3)

        save_button = CTkButton(small_window, text='Save')
        save_button.configure(anchor='center', fg_color=('#d6d6d2', '#121211'), hover_color=('#333331', '#000000'),
                              text_color=('#43605E', '#ffe5d4'), command=lambda: self.addtransactiondata(small_window))
        save_button.place(x=120, y=5 + y_diff * 4)
        small_window.mainloop()

    def addtransactiondata(self, small_window):
        import time
        var = str(time.time())
        var2 = (var.split("."))
        payment_id = var2[0][4:10]
        try:
            qry = 'select card_type from cards where card_num=%s and user_name=%s'
            row = self.cur.execute(qry, (self.input_card_num.get(), self.un))
            input_card_type = self.cur.fetchone()
            if row == 1:
                messagebox.showinfo("Success", "Transaction Record Added Successfully", parent=small_window)
        except Exception as e:
            messagebox.showerror("Error", "Insertion Error : \n" + str(e), parent=small_window)

        try:
            qry = 'insert into transactions values(%s,%s,%s,%s,%s,%s,%s)'
            rowcount = self.cur.execute(qry, (self.un, self.input_payment.get(), self.input_date.entry.get(),
                                              self.input_card_num.get(), input_card_type[0],
                                              self.input_amount.get(), payment_id))
            self.connection.commit()
            if rowcount == 1:
                messagebox.showinfo("Success", "Transaction Record Added Successfully", parent=small_window)
        except Exception as e:
            messagebox.showerror("Error", "Insertion Error : \n" + str(e), parent=small_window)
        try:
            qry = " select used_limit from cards where card_num=%s and user_name=%s"
            rowcount = self.cur.execute(qry, (self.input_card_num.get(), self.un))
            data = self.cur.fetchone()
            qry = 'Update cards set used_limit = %s where card_num = %s'
            rowcount = self.cur.execute(qry, (data[0] + int(self.input_amount.get()), self.input_card_num.get()))
            self.connection.commit()
            if rowcount == 1:
                messagebox.showinfo("Success", "Transaction Record Added Successfully", parent=small_window)
                self.clearpagetransaction()
        except Exception as e:
            messagebox.showerror("Error", "Insertion Error : \n" + str(e), parent=small_window)
        self.fetchdata_2(payment_id)
        if self.check == 1:
            self.show()
        self.graph()

    def deletetransaction(self):
        small_window = CTkToplevel(self.window)
        small_window.title('Delete Transaction')
        small_window.configure(fg_color=('#d6d6d2', '#121211'))
        small_window.after(10, small_window.lift)
        width = 400
        height = 400
        small_window.minsize(width, height)
        x = small_window.winfo_screenwidth() // 2 - width // 2
        y = small_window.winfo_screenheight() // 2 - height // 2
        small_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        card_num = CTkLabel(small_window, text='Payment ID: ', text_color=('#43605E', '#ffe5d4'))
        card_num.place(x=5, y=20)
        self.del_data = CTkEntry(small_window, placeholder_text='Enter Payment ID: ', fg_color='#faf9f5',
                                 text_color='black')
        self.del_data.place(x=120, y=20)

        delete_button = CTkButton(small_window, text='Delete')
        delete_button.configure(anchor='center', fg_color=('#d6d6d2', '#121211'), hover_color=('#333331', '#000000'),
                                text_color=('#43605E', '#ffe5d4'), font=('Sans', 14),
                                command=lambda: self.deletetransactiondata(small_window))
        delete_button.place(x=120, y=60)

        small_window.mainloop()

    def deletetransactiondata(self, small_window):
        ans = messagebox.askquestion("Confirmation", "Are you sure to delete ??", parent=small_window)
        if ans == "yes":
            try:
                qry = " select card_number, amount from transactions where payment_id=%s and user_name=%s"
                rowcount = self.cur.execute(qry, (self.del_data.get(), self.un))
                data_tra = self.cur.fetchone()

                qry = " select used_limit from cards where card_num=%s and user_name=%s"
                rowcount = self.cur.execute(qry, (data_tra[0], self.un))
                data = self.cur.fetchone()

                qry = 'Update cards set used_limit = %s where card_num = %s and user_name=%s'
                rowcount = self.cur.execute(qry, ((data[0] - data_tra[1]), data_tra[0], self.un))
                self.connection.commit()

                qry = "delete from transactions where payment_id=%s and user_name=%s"
                rowcount = self.cur.execute(qry, (self.del_data.get(), self.un))
                self.connection.commit()
                if rowcount == 1:
                    messagebox.showinfo("Success", "Transaction Record Deleted Successfully", parent=small_window)
                    self.del_data.delete(0, END)
            except Exception as e:
                messagebox.showerror("Error", "Deletion Error : \n" + str(e), parent=small_window)
        self.tree.delete(*self.tree.get_children())
        self.getalldata()
        if self.check == 1:
            self.show()
        self.graph()

    def graph(self):
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
            messagebox.showerror("Error", "Error while fetching Data  : \n" + str(e), parent=self.window)
        meter = ttb.Meter(self.window, metertype='full', interactive=False, amounttotal=self.total_sum_cc,
                          amountused=self.used_sum_cc, stripethickness=2, textleft='Limit Used:',
                          subtext='Total Credit Limit:\n'+str(self.total_sum_cc), subtextstyle='primary')
        meter.place(x=940, y=410)
        try:
            qry = " select total_limit, used_limit from cards where card_type='Debit' and user_name=%s"
            rowcount = self.cur.execute(qry, self.un)
            data = self.cur.fetchall()
            self.total_sum_db = 0
            self.used_sum = 0
            for t in data:
                self.total_sum_db += t[0]
                self.used_sum += t[1]
        except Exception as e:
            messagebox.showerror("Error", "Error while fetching Data  : \n"+str(e), parent=self.window)

        meter = ttb.Meter(self.window, metertype='full', interactive=False, amounttotal=self.total_sum_db,
                          amountused=self.used_sum, stripethickness=2, textleft='Limit Used:',
                          subtext='Total Debit Limit:\n'+str(self.total_sum_db), subtextstyle='primary')
        meter.place(x=1250, y=410)

    def offers(self):
        ac = CTkButton(self.offerframe, text='Apply Card', anchor='center', fg_color=('#d6d6d2', '#121211'),
                       hover_color=('#333331', '#000000'), text_color=('#43605E', '#ffe5d4'),
                       border_color=('#FFFFFF', '#d9b30b'), font=('sans', 16, 'bold'), border_spacing=5,
                       command=lambda: self.url('apply credit card'))
        ac.place(x=10, y=25)

        oc = CTkButton(self.offerframe, text='Check Offers', anchor='center', fg_color=('#d6d6d2', '#121211'),
                       hover_color=('#333331', '#000000'), text_color=('#43605E', '#ffe5d4'),
                       border_color=('#FFFFFF', '#d9b30b'), font=('sans', 16, 'bold'), border_spacing=5,
                       command=lambda: self.url('credit card offers'))
        oc.place(x=10, y=90)

        ac = CTkButton(self.offerframe, text='Transaction\nSummary', anchor='center', fg_color=('#d6d6d2', '#121211'),
                       hover_color=('#333331', '#000000'), text_color=('#43605E', '#ffe5d4'),
                       border_color=('#FFFFFF', '#d9b30b'), font=('sans', 16, 'bold'), border_spacing=5,
                       command=self.print)
        ac.place(x=160, y=25)
    def url(self, item):
        url = "https://www.google.com/search?q="
        webbrowser.open(url + item)
    def print(self):
        try:
            qry = " select * from transactions where user_name=%s"
            rowcount = self.cur.execute(qry, self.un)
            transactions = self.cur.fetchall()
            ls = []
            for myrow in transactions:
                ls.append([myrow[0], myrow[1], myrow[2], myrow[3], myrow[4], myrow[5]])
        except Exception as e:
            messagebox.showerror("Error", "Error while fetching Data  : \n"+str(e), parent=self.window)

        headings = ['Payment', 'Date', 'Card Number', 'Credit/Debit', 'Amount', 'Payment ID']
        pdf = my_cust_PDF()
        pdf.print_chapter(ls, headings)

        pdf.output('pdf_file1.pdf')
        os.system('explorer.exe "pdf_file1.pdf"')

#
# if __name__ == '__main__':
#     obj = CardClass('light')