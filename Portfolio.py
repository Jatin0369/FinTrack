from tkinter import *
from tkinter import messagebox
import pymysql as pymysql
from customtkinter import *
from PIL import Image
import ttkbootstrap as ttb
from ttkbootstrap.tooltip import ToolTip
import webbrowser
from pdf import my_cust_PDF
import yfinance as yf
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from datetime import date, timedelta
import pandas as pd
from newsapi import NewsApiClient
from collections import defaultdict


class PortfolioClass:
    def __init__(self, mode, un):
        self.un = un
        self.mode = mode
        set_appearance_mode(mode)

        self.window = CTkToplevel(fg_color=('#f2f2e9', '#000000'))
        self.window.title("Portfolio")
        self.window.overrideredirect(True)

        self.window.minsize(1200, 780)
        self.window.geometry("1514x990+338+30")

        self.rate = None
        self.rate_entry = None
        self.time = None
        self.time_entry = None
        self.f1 = None
        self.p_id = None
        self.price_entry_mf = None
        self.name_entry_mf = None
        self.name_entry_st = None
        self.price_entry_st = None
        self.goal_entry = None
        self.ticker_entry = None
        self.quantity_entry = None
        self.tree = None
        self.textbox = None
        self.price_st = None
        self.ticker = None
        self.quantity_st = None
        self.name_st = None
        self.Start = None
        self.End = None
        self.tsla = None
        self.hist = None
        self.name_mf = None
        self.goal = None
        self.price_mf = None

        self.TopFrame = CTkFrame(self.window)
        self.TopFrame.configure(fg_color=('#d6d6d2', '#121211'), border_color='#B76E79', border_width=0.5, width=1210,
                                height=130, corner_radius=20)
        self.TopFrame.place(x=0, y=-15)
        self.createwidgets_tp()

        self.databaseconnection()

        self.news_window = CTkTextbox(self.window, width=340, height=350)
        self.news_window.configure(text_color=('#43605E', '#ffe5d4'), fg_color=('#d6d6d2', '#121211'),
                                   border_color='#B76E79',  border_width=1, font=('sans', 14),
                                   scrollbar_button_hover_color=('#333331', '#000000'))
        self.news_window.place(x=865, y=425)

        self.search_frame = CTkFrame(self.window, fg_color=('#d6d6d2', '#121211'), border_color='#B76E79',
                                     border_width=1, corner_radius=10, width=340, height=40)
        self.search_frame.place(x=865, y=375)

        self.label = CTkLabel(self.search_frame, text="News", text_color=('#43605E', '#ffe5d4'),
                              font=('sans', 20, 'bold'))
        self.label.place(x=20, y=5)
        self.title = StringVar()
        self.entry = CTkEntry(self.search_frame, fg_color=('#d6d6d2', '#121211'), border_color='#B76E79',
                              border_width=1, corner_radius=5, text_color=('#43605E', '#ffe5d4'), width=150, height=30,
                              font=('sans', 16, 'bold'), textvariable=self.title)
        self.entry.place(x=100, y=6)
        self.search_button = CTkButton(self.search_frame, text='Search', fg_color=('#d6d6d2', '#121211'),
                                       font=('sans', 16,), border_color='#B76E79', border_width=1, width=40,
                                       text_color=('#43605E', '#ffe5d4'), hover_color=('#333331', '#000000'),
                                       command=lambda: self.news_default_search())
        self.search_button.place(x=260, y=6)

        self.options_frame = CTkFrame(self.window, fg_color=('#d6d6d2', '#121211'), border_color='#B76E79',
                                      border_width=1, corner_radius=5, width=340, height=225)
        self.options_frame.place(x=865, y=130)
        self.options()
        self.create_display()
        self.window.bind('<Escape>', lambda e: self.back())
        self.window.focus()

        self.window.mainloop()
    # --------------this establishes database connection-----
    def databaseconnection(self):
        try:
            self.connection = pymysql.connect(host='localhost', db='finance_manager_db', user='root', password='')
            self.cur = self.connection.cursor()
        except Exception as e:
            messagebox.showerror("Error", "Database connection error \n" + str(e), parent=self.window)

    def options(self):
        tab = CTkTabview(self.options_frame, width=320, height=230, fg_color=('grey', '#121211'))
        tab.place(x=10, y=-10)
        stock = tab.add('Stocks')
        mf = tab.add('Mutual Fund')
        oi = tab.add('Others')

        self.name_st = StringVar()
        name_lbl = CTkLabel(stock, text='Name', font=('sans', 16, 'bold'), text_color=('#ffffff', '#ffe5d4'))
        name_lbl.place(x=5, y=5)
        self.name_entry_st = CTkEntry(stock, width=80, height=10, fg_color=('#d6d6d2', '#121211'),
                                      border_color='#B76E79',
                                      border_width=1, corner_radius=5, textvariable=self.name_st)
        self.name_entry_st.place(x=5, y=30)

        self.quantity_st = StringVar()
        quantity_lbl = CTkLabel(stock, text='Quantity', font=('sans', 16, 'bold'), text_color=('#ffffff', '#ffe5d4'))
        quantity_lbl.place(x=5, y=60)
        self.quantity_entry = CTkEntry(stock, width=80, height=10, fg_color=('#d6d6d2', '#121211'),
                                       border_color='#B76E79',
                                       border_width=1, corner_radius=5, textvariable=self.quantity_st)
        self.quantity_entry.place(x=5, y=85)

        self.ticker = StringVar()
        ticker_lbl = CTkLabel(stock, text='Ticker name', font=('sans', 16, 'bold'), text_color=('#ffffff', '#ffe5d4'))
        ticker_lbl.place(x=150, y=5)
        self.ticker_entry = CTkEntry(stock, width=80, height=10, fg_color=('#d6d6d2', '#121211'), border_color='#B76E79',
                                     border_width=1, corner_radius=5, textvariable=self.ticker)
        self.ticker_entry.place(x=150, y=30)

        self.price_st = StringVar()
        price_lbl = CTkLabel(stock, text='Price', font=('sans', 16, 'bold'), text_color=('#ffffff', '#ffe5d4'))
        price_lbl.place(x=150, y=60)
        self.price_entry_st = CTkEntry(stock, width=80, height=10, fg_color=('#d6d6d2', '#121211'), border_color='#B76E79',
                                       border_width=1, corner_radius=5, textvariable=self.price_st)
        self.price_entry_st.place(x=150, y=85)

        add_btn = CTkButton(stock, text='Add Stock', fg_color='#3b4657', command=self.add_stock)
        add_btn.place(x=5, y=120)
        del_btn = CTkButton(stock, text='Delete Stock', fg_color='#3b4657', command=self.del_st)
        del_btn.place(x=5, y=150)
        update_btn = CTkButton(stock, text='Update Stock', fg_color='#3b4657', command=self.update_stock)
        update_btn.place(x=150, y=120)
        view_btn = CTkButton(stock, text='View Stock', fg_color='#3b4657', command=self.view_st)
        view_btn.place(x=150, y=150)

#        ------------MF-------------------
        self.name_mf = StringVar()
        name_lbl = CTkLabel(mf, text='Name', font=('sans', 16, 'bold'), text_color=('#ffffff', '#ffe5d4'))
        name_lbl.place(x=5, y=5)
        self.name_entry_mf = CTkEntry(mf, width=80, height=10, fg_color=('#d6d6d2', '#121211'), border_color='#B76E79',
                                      border_width=1, corner_radius=5, textvariable=self.name_mf)
        self.name_entry_mf.place(x=5, y=30)

        self.goal = StringVar()
        goal_lbl = CTkLabel(mf, text='Goal name', font=('sans', 16, 'bold'), text_color=('#ffffff', '#ffe5d4'))
        goal_lbl.place(x=150, y=5)
        self.goal_entry = CTkEntry(mf, width=80, height=10, fg_color=('#d6d6d2', '#121211'), border_color='#B76E79',
                                   border_width=1, corner_radius=5, textvariable=self.goal)
        self.goal_entry.place(x=150, y=30)

        self.price_mf = StringVar()
        price_lbl = CTkLabel(mf, text='Price', font=('sans', 16, 'bold'), text_color=('#ffffff', '#ffe5d4'))
        price_lbl.place(x=5, y=60)
        self.price_entry_mf = CTkEntry(mf, width=80, height=10, fg_color=('#d6d6d2', '#121211'), border_color='#B76E79',
                                       border_width=1, corner_radius=5, textvariable=self.price_mf)
        self.price_entry_mf.place(x=5, y=85)

        add_btn = CTkButton(mf, text='Add MF', fg_color='#3b4657', command=self.add_mf)
        add_btn.place(x=5, y=120)
        del_btn = CTkButton(mf, text='Delete MF', fg_color='#3b4657', command=self.del_mf)
        del_btn.place(x=5, y=150)
        # update_btn = CTkButton(mf, text='Update MF', fg_color='#3b4657')
        # update_btn.place(x=150, y=120)
        view_btn = CTkButton(mf, text='View MF goal', fg_color='#3b4657', command=self.view_mf)
        view_btn.place(x=150, y=120)

#       --------------- others-------------------------------

        self.textbox = CTkTextbox(oi)
        self.textbox.configure(width=295, height=130, wrap='word', text_color=('#43605E', '#ffe5d4'),
                               fg_color=('#d6d6d2', '#121211'), border_color='#B76E79',  border_width=1,
                               font=('sans', 14))
        self.textbox.insert("0.0", text='')  # insert at line 0 character 0
        # text = textbox.get("0.0", "end")
        self.textbox.place(x=5, y=5)
        add_btn = CTkButton(oi, text='Add', fg_color='#3b4657', width=70, command=self.add_oi)
        add_btn.place(x=5, y=150)
        del_btn = CTkButton(oi, text='Delete', fg_color='#3b4657', width=70, command=self.del_oi)
        del_btn.place(x=80, y=150)
        # update_btn = CTkButton(oi, text='Update', fg_color='#3b4657', width=70)
        # update_btn.place(x=155, y=150)
        view_btn = CTkButton(oi, text='View', fg_color='#3b4657', width=70, command=self.view_oi)
        view_btn.place(x=155, y=150)

    def clear_st(self):
        self.name_entry_st.delete(0, END)
        self.quantity_entry.delete(0, END)
        self.ticker_entry.delete(0, END)
        self.price_entry_st.delete(0, END)

    def clear_mf(self):
        self.name_entry_mf.delete(0, END)
        self.price_entry_mf.delete(0, END)
        self.goal_entry.delete(0, END)

    def clear_oi(self):
        self.textbox.delete('0.0', 'end')

    def view_oi(self):
        small_window = CTkToplevel(self.window)
        small_window.title('Add Transaction')
        small_window.configure(fg_color=('#d6d6d2', '#121211'))
        small_window.after(10, small_window.lift)
        width = 400
        height = 350
        small_window.minsize(width, height)
        x = small_window.winfo_screenwidth() // 2 - width // 2
        y = small_window.winfo_screenheight() // 2 - height // 2
        small_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        f1 = CTkFrame(small_window, fg_color=('#d6d6d2', '#121211'))
        f1.pack()
        columns = ('Record')

        self.style = ttb.Style()
        if self.mode == 'mylight':
            self.style.configure("Treeview", background="#d6d6d2", foreground="#43605E", font=('Sans', 11))
        else:
            self.style.configure("Treeview", background="#000000", foreground="#ffffff", font=('Sans', 11))
        self.style.configure("Treeview", rowheight=50)
        self.style.configure("Treeview.Heading", font=('Sans', 13, 'bold'), background="#a6a6a2",
                             foreground="#073602")

        self.tree = ttb.Treeview(f1, columns=columns, show='headings')
        self.tree.column('#0')
        self.tree.column('Record', width=x-280, anchor='w', minwidth=x-300)
        # define headings
        self.tree.heading('Record', text='Record', anchor='w')
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)
        self.tree.pack()
        count = 1
        try:
            qry = " select * from other_investment where user_name=%s"
            rowcount = self.cur.execute(qry, self.un)
            data = self.cur.fetchall()
            if data:
                for row in data:
                    #print(row[0])
                    self.tree.insert('', END, values=row)
                    count += 1
            else:
                messagebox.showwarning("Empty", "No Record Found", parent=self.window)
        except Exception as e:
            messagebox.showerror("Error", "Error while fetching Data  : \n"+str(e), parent=self.window)

        small_window.mainloop()

    def del_oi(self):
        try:
            qry = "delete from other_investment where investment=%s and user_name=%s"
            print(self.textbox.get("0.0", 'end'))
            rowcount = self.cur.execute(qry, (str(self.textbox.get("0.0", 'end')), self.un))
            self.connection.commit()
            if rowcount == 1:
                messagebox.showinfo("Success", "Card Data Deleted Successfully", parent=self.window)
                self.clear_oi()
        except Exception as e:
            messagebox.showerror("Error", "Deletion Error : \n" + str(e), parent=self.window)

    def item_selected(self, event):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = item['values']
            # show a message
            self.textbox.insert('0.0', str(record[0]).strip())
            # messagebox.showinfo(title='Information', message=','.join(record))

    def item_selected_st(self, event):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = item['values']
            self.p_id = record[0]
            self.name_entry_st.insert(0, record[1])
            self.quantity_entry.insert(0, record[3])
            self.ticker_entry.insert(0, record[2])
            self.price_entry_st.insert(0, record[4])
            self.plot(record[2])
            self.st_meter(record[4], record[3], record[2])

    def item_selected_mf(self, event):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = item['values']
            self.name_entry_mf.insert(0, record[0])
            self.goal_entry.insert(0, record[2])
            self.price_entry_mf.insert(0, record[1])
            self.mf_meter()

    def add_oi(self):
        try:
            qry = "insert into other_investment values(%s,%s)"
            rowcount = self.cur.execute(qry, (self.un, self.textbox.get("0.0", "end")))
            self.connection.commit()
            if rowcount == 1:
                messagebox.showinfo("Success", "Data Added Successfully", parent=self.window)
                self.clear_oi()
        except Exception as e:
            messagebox.showerror("Error", "Insertion Error : \n" + str(e), parent=self.window)

    def view_mf(self):
        small_window = CTkToplevel(self.window)
        small_window.title('Add Transaction')
        small_window.configure(fg_color=('#d6d6d2', '#121211'))
        small_window.after(10, small_window.lift)
        width = 400
        height = 350
        small_window.minsize(width, height)
        x = small_window.winfo_screenwidth() // 2 - width // 2
        y = small_window.winfo_screenheight() // 2 - height // 2
        small_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.clear_mf()
        f1 = CTkFrame(small_window, fg_color=('#d6d6d2', '#121211'))
        f1.pack()
        columns = ('Name', 'Price', 'Goal')

        self.style = ttb.Style()
        # if self.mode == 'mylight':
        #     self.style.configure("Treeview", background="#d6d6d2", foreground="#43605E", font=('Sans', 11))
        # else:
        self.style.configure("Treeview", background="#000000", foreground="#ffffff", font=('Sans', 11))
        self.style.configure("Treeview", rowheight=50)
        self.style.configure("Treeview.Heading", font=('Sans', 13, 'bold'), background="#a6a6a2",
                             foreground="#073602")

        self.tree = ttb.Treeview(f1, columns=columns, show='headings')
        self.tree.column('#0', width=270, minwidth=270)
        self.tree.column('Name', width=120, minwidth=70, stretch=NO, anchor='center')
        self.tree.column('Price', width=120, minwidth=70, stretch=NO, anchor='center')
        self.tree.column('Goal', width=120, minwidth=70, stretch=NO, anchor='center')
        # define headings
        self.tree.heading('Name', text='Name', anchor='center')
        self.tree.heading('Price', text='Price', anchor='center')
        self.tree.heading('Goal', text='Goal', anchor='center')

        self.tree.bind('<<TreeviewSelect>>', self.item_selected_mf)
        self.tree.pack()
        count = 1
        try:
            qry = " select * from mutual_fund where user_name=%s"
            rowcount = self.cur.execute(qry, self.un)
            data = self.cur.fetchall()
            if data:
                for row in data:
                    ans = [row[1], row[3], row[2]]
                    self.tree.insert('', END, values=ans)
                    count += 1
            else:
                messagebox.showwarning("Empty", "No Record Found", parent=self.window)
        except Exception as e:
            messagebox.showerror("Error", "Error while fetching Data  : \n"+str(e), parent=self.window)

        small_window.mainloop()

    def add_mf(self):
        try:
            qry = "insert into mutual_fund values(%s,%s, %s, %s)"
            rowcount = self.cur.execute(qry, (
                                              self.un, self.name_mf.get(),
                                              self.goal.get(),
                                              self.price_mf.get()))
            self.connection.commit()
            if rowcount == 1:
                messagebox.showinfo("Success", "Mutual Fund Data Added Successfully", parent=self.window)
                self.clear_mf()
        except Exception as e:
            messagebox.showerror("Error", "Insertion Error : \n" + str(e), parent=self.window)

    def del_mf(self):
        try:
            qry = "delete from mutual_fund where fund_name=%s and price=%s and user_name=%s"
            rowcount = self.cur.execute(qry, (self.name_mf.get(), self.price_mf.get(), self.un))
            self.connection.commit()
            if rowcount == 1:
                messagebox.showinfo("Success", "Fund Record Deleted Successfully", parent=self.window)
                self.clear_mf()
        except Exception as e:
            messagebox.showerror("Error", "Deletion Error : \n" + str(e), parent=self.window)

    def view_st(self):
        small_window = CTkToplevel(self.window)
        small_window.title('Add Transaction')
        small_window.configure(fg_color=('#d6d6d2', '#121211'))
        small_window.after(10, small_window.lift)
        width = 400
        height = 350
        small_window.minsize(width, height)
        x = small_window.winfo_screenwidth() // 2 - width // 2
        y = small_window.winfo_screenheight() // 2 - height // 2
        small_window.geometry('{}x{}+{}+{}'.format(width+100, height, x, y))
        self.clear_st()
        f1 = CTkFrame(small_window, fg_color=('#d6d6d2', '#121211'))
        f1.pack()
        columns = ('P ID', 'Company', 'Ticker', 'Quantity', 'Price')

        self.style = ttb.Style()
        # if self.mode == 'mylight':
        #     self.style.configure("Treeview", background="#d6d6d2", foreground="#43605E", font=('Sans', 11))
        # else:
        self.style.configure("Treeview", background="#000000", foreground="#ffffff", font=('Sans', 11))
        self.style.configure("Treeview", rowheight=50)
        self.style.configure("Treeview.Heading", font=('Sans', 13, 'bold'), background="#a6a6a2",
                             foreground="#073602")

        self.tree = ttb.Treeview(f1, columns=columns, show='headings')
        self.tree.column('#0', width=270, minwidth=270)
        self.tree.column('P ID', width=120, minwidth=70, stretch=NO, anchor='center')
        self.tree.column('Company', width=120, minwidth=70, stretch=NO, anchor='center')
        self.tree.column('Ticker', width=120, minwidth=70, stretch=NO, anchor='center')
        self.tree.column('Quantity', width=120, minwidth=70, stretch=NO, anchor='center')
        self.tree.column('Price', width=120, minwidth=70, stretch=NO, anchor='center')
        # define headings
        self.tree.heading('P ID', text='P ID', anchor='center')
        self.tree.heading('Company', text='Company', anchor='center')
        self.tree.heading('Ticker', text='Ticker', anchor='center')
        self.tree.heading('Quantity', text='Quantity', anchor='center')
        self.tree.heading('Price', text='Price', anchor='center')

        self.tree.bind('<<TreeviewSelect>>', self.item_selected_st)
        self.tree.pack()
        count = 1
        try:
            qry = " select * from stocks where user_name=%s"
            rowcount = self.cur.execute(qry, self.un)
            data = self.cur.fetchall()
            if data:
                for row in data:
                    ans = [row[5], row[1], row[4], row[2], row[3]]
                    self.tree.insert('', END, values=ans)
                    count += 1
            else:
                messagebox.showwarning("Empty", "No Record Found", parent=self.window)
        except Exception as e:
            messagebox.showerror("Error", "Error while fetching Data  : \n"+str(e), parent=self.window)

        small_window.mainloop()

    def del_st(self):
        try:
            qry = 'delete from stocks where p_id = %s and user_name=%s'
            rowcount = self.cur.execute(qry, (str(self.p_id), self.un))
            if rowcount == 1:
                messagebox.showinfo("Success", "Stock Data Deleted Successfully", parent=self.window)
                self.clear_st()
        except Exception as e:
            messagebox.showerror("Error", "Error while deleting Data  : \n" + str(e), parent=self.window)

    def add_stock(self):
        import time
        var = str(time.time())
        var2 = (var.split("."))
        payment_id = var2[0][4:10]
        try:
            qry = "insert into stocks values(%s,%s, %s, %s, %s, %s)"
            rowcount = self.cur.execute(qry, (
                                              self.un, self.name_st.get(),
                                              self.quantity_st.get(),
                                              self.price_st.get(), self.ticker.get(),
                                              payment_id))
            self.connection.commit()
            if rowcount == 1:
                messagebox.showinfo("Success", "Stock Data Added Successfully", parent=self.window)
                self.clear_st()
        except Exception as e:
            messagebox.showerror("Error", "Insertion Error : \n" + str(e), parent=self.window)

    def update_stock(self):
        try:
            qry = " select * from stocks where ticker_name=%s and user_name=%s"
            rowcount = self.cur.execute(qry, (self.ticker.get(), self.un))
            data = self.cur.fetchone()
        except Exception as e:
            messagebox.showerror("Error", "Error while fetching Data  : \n"+str(e), parent=self.window)
        try:
            qry = "Update stocks set quantity=%s where ticker_name=%s and price=%s"
            rowcount = self.cur.execute(qry, (int(data[2]) + int(self.quantity_st.get()),
                                              self.ticker.get(), self.price_st.get()))
            self.connection.commit()
            if rowcount == 1:
                messagebox.showinfo("Success", "Stock Data Added Successfully", parent=self.window)
                self.clear_st()
        except Exception as e:
            messagebox.showerror("Error", "Insertion Error : \n" + str(e), parent=self.window)

    def del_stock(self):
        try:
            qry = "delete from stocks where ticker_name=%s and price=%s and user_name=%s"
            rowcount = self.cur.execute(qry, (self.ticker.get(), self.price_st.get(), self.un))
            self.connection.commit()
            if rowcount == 1:
                messagebox.showinfo("Success", "Stock Record Deleted Successfully", parent=self.window)
                self.clear_st()
        except Exception as e:
            messagebox.showerror("Error", "Deletion Error : \n" + str(e), parent=self.window)

    def plot(self, ticker):

        # the figure that will contain the plot
        fig = Figure(figsize=(10, 3), dpi=91, edgecolor='red') #facecolor='transparent'
        if self.mode == 'cyborg':
            fig.set_facecolor("black")
        if self.mode == 'mylight':
            fig.set_facecolor("#f2f2e9")

        plot1 = fig.add_subplot()

        self.Start = date.today() - timedelta(365)
        self.Start.strftime('%Y-%m-%d')

        self.End = date.today() + timedelta(2)
        self.End.strftime('%Y-%m-%d')

        # plotting the graph
        # TESLA = self.closing_price('TSLA')  # CALL THE FUNCTION
        # AMAZON = self.closing_price('TATASTEEL.NS')
        # AAPLE = self.closing_price('AAPL')

        graph = self.closing_price(ticker[0])

        # plot1.plot(TESLA)
        # plot1.plot(AMAZON)
        # plot1.plot(AAPLE)
        plot1.plot(graph)
        if self.mode == 'cyborg':
            plot1.set_facecolor("black")
            # plot1.xaxis.label.set_color('blue')
            # plot1.yaxis.label.set_color('blue')
            plot1.tick_params(axis='x', colors='pink')
            plot1.tick_params(axis='y', colors='pink')
        if self.mode == 'mylight':
            plot1.set_facecolor("#f2f2e9")

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.draw()

        # placing the canvas on the Tkinter window
       # canvas.get_tk_widget().place(x=10, y=15)

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().place(x=-60, y=610)

    def closing_price(self, ticker):
        Asset = pd.DataFrame(yf.download(ticker, start=self.Start, end=self.End)['Adj Close'])
        return Asset

    def back(self):
        self.window.destroy()

    def createwidgets_tp(self):

        img = CTkImage(Image.open("myimages//wel.png"), size=(400, 100))
        wel = CTkLabel(self.TopFrame, image=img, text='')

        sublabel = CTkLabel(self.TopFrame, text='Review your Portfolio track and progress', font=('Sans', 18, 'bold'),
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
            messagebox.showerror("Error", "Error while fetching Data  : \n" + str(e), parent=self.window)

        headings = ['Payment', 'Date', 'Card Number', 'Credit/Debit', 'Amount', 'Payment ID']
        pdf = my_cust_PDF()
        pdf.print_chapter(ls, headings)

        pdf.output('pdf_file1.pdf')
        os.system('explorer.exe "pdf_file1.pdf"')

    def news_default_search(self):
        if str(self.title.get()) == '':
            self.news(topic='business')
        else:
            self.news(str(self.title.get()))

    def news(self, topic='business'):
        print(topic)
        newsapi = NewsApiClient(api_key='2bc29605bf3846c2a02386020c847a4c')
        # Retrieve the top headlines
        top_headlines = newsapi.get_top_headlines(language='en')
        ar = newsapi.get_everything(q=topic,
                                    from_param='2024-01-11',
                                    to='2023-12-01',
                                    domains='moneycontrol.com')

        # Clear the text widget
        self.news_window.delete(1.0, 'end')

        # Display the top headlines
        for article in ar['articles']:
            self.news_window.insert('end', article['title'] + '\n\n')

    def create_display(self):
        self.f1 = CTkFrame(self.window, fg_color=('#f2f2e9', '#000000'), border_color='#B76E79',
                           border_width=1, corner_radius=10, width=400, height=165)
        self.f1.place(x=30, y=130)
        ls = []
        dic = defaultdict(int)
        try:
            qry = " select ticker_name from stocks where user_name=%s "
            rowcount = self.cur.execute(qry, self.un)
            data = self.cur.fetchall()

            for row in data:
                ls.append(str(row[0]))
            for item in ls:
                dic[item] += 1

        except Exception as e:
            messagebox.showerror("Error", "Error while fetching Data  : \n"+str(e), parent=self.window)

        quantity = 0
        try:
            qry = " select quantity, price from stocks where user_name=%s"
            rowcount = self.cur.execute(qry, self.un)
            data = self.cur.fetchall()
            print(data)
            for row in data:
                quantity += row[0]

        except Exception as e:
            messagebox.showerror("Error", "Error while fetching Data  : \n"+str(e), parent=self.window)

        meter = ttb.Meter(self.f1, metertype='semi', metersize=150, interactive=False, amounttotal=quantity,
                          amountused=quantity, stripethickness=2, textleft='Stocks:', arcrange=180,
                          arcoffset=180, subtext="Companies:" + str(len(dic)))
        meter.place(x=10, y=10)

    def st_meter(self, price, quantity, ticker):

        # tickerData = yf.Ticker(ticker)
        # todayData = tickerData.history(period='1d')
        # cp = (todayData['Close'][0])

        # data = yf.Ticker(ticker).history(period="1d", interval="1m")
        # cp = data["Close"].iloc[-1]
        # print(cp)

        stock = yf.Ticker(ticker)
       # print("hi--> ", stock.history(period='1d')['Close'][0])
        latest_price = stock.history(period='1d')['Close'][0]

        cp = round(latest_price, 2)

        pg1 = CTkProgressBar(self.f1, orientation='horizontal', width=200, height=20,
                             fg_color=('#f2f2e9', '#060606'), progress_color=('#333331', '#B76E79'),
                             border_color='#B76E79')
        pg1.set(price/cp)
        total = CTkLabel(self.f1, text='Total Investment: ' + str(price*quantity), text_color=('#43605E', '#ffe5d4'),
                         fg_color=('#f2f2e9', '#000000'), font=('sans', 16, 'bold'))
        total.place(x=180, y=30)
        pg1.place(x=180, y=10)

        pg2 = CTkProgressBar(self.f1, orientation='horizontal', width=200, height=20,
                             fg_color=('#f2f2e9', '#060606'), progress_color=('#333331', '#B76E79'),
                             border_color='#B76E79')
        pg2.set(cp*quantity)
        total2 = CTkLabel(self.f1, text='Current Value: ' + str(int(cp*quantity)), text_color=('#43605E', '#ffe5d4'),
                          fg_color=('#f2f2e9', '#000000'), font=('sans', 16, 'bold'))
        total2.place(x=180, y=80)
        pg2.place(x=180, y=60)

        roi = ((cp-price)/price)*100
        lb = CTkLabel(self.f1, text='R.O.I: ' + str(int(roi)) + '%', fg_color=('#f2f2e9', '#000000'),
                      font=('sans', 16,), width=40, text_color=('#43605E', '#ffe5d4'))
        lb.place(x=180, y=100)

    def mf_meter(self):
        self.f = CTkFrame(self.window, fg_color=('#f2f2e9', '#000000'), border_color='#B76E79',
                          border_width=1, corner_radius=10, width=400, height=165)
        self.f.place(x=30, y=310)
        lb = CTkLabel(self.f, text='Rate(%): ', fg_color=('#f2f2e9', '#000000'),
                      font=('sans', 16,), width=40, text_color=('#43605E', '#ffe5d4'))
        lb.place(x=10, y=10)

        self.rate = StringVar()
        self.rate_entry = CTkEntry(self.f, width=40, height=10, fg_color=('#f2f2e9', '#000000'), border_color='#B76E79',
                                   border_width=1, corner_radius=5, textvariable=self.rate)
        self.rate_entry.place(x=80, y=15)

        lb2 = CTkLabel(self.f, text='Time(Yr): ', fg_color=('#f2f2e9', '#000000'),
                       font=('sans', 16,), width=40, text_color=('#43605E', '#ffe5d4'))
        lb2.place(x=140, y=10)
        self.time = StringVar()
        self.time_entry = CTkEntry(self.f, width=40, height=10, fg_color=('#f2f2e9', '#000000'), border_color='#B76E79',
                                   border_width=1, corner_radius=5, textvariable=self.time)
        self.time_entry.place(x=210, y=15)

        self.search_button = CTkButton(self.f, text='Calculate', fg_color=('#f2f2e9', '#000000'),
                                       font=('sans', 16,), border_color='#B76E79', border_width=1, width=35, height=15,
                                       text_color=('#43605E', '#ffe5d4'), hover_color=('#333331', '#000000'),
                                       command=lambda: self.compute())
        self.search_button.place(x=290, y=12)

    def compute(self):
        print((self.price_mf.get() + " " + (self.time_entry.get())))
        prin = eval(self.price_mf.get()) * eval(self.time_entry.get())
        A = (prin) * (pow((1 + int(self.rate_entry.get()) / 100), int(self.time_entry.get())))

        A = int(self.price_mf.get())
        YR = int(self.rate_entry.get())
        Y = int(self.time_entry.get())


        #A = float(input("Enter the monthly SIP amount: "))
        #YR = float(input("Enter the yearly rate of return: "))
        #Y = int(input("Enter the number of years: "))

        MR = YR / 12 / 100
        M = Y * 12

        FV = A * ((((1 + MR) ** (M)) - 1) * (1 + MR)) / MR
        FV = round(FV)
        print("The expected amount you will get is:", FV)

        meter = ttb.Meter(self.f, metertype='semi', metersize=100, amounttotal=A*Y*20, amountused=A*Y*12, stepsize=1,
                          interactive=True, stripethickness=2, arcrange=180, subtextstyle='primary',
                          arcoffset=180, subtext='Investment', textfont=('Sans', 12), subtextfont=('Sans', 8))
        meter.place(x=80, y=60)

        meter2 = ttb.Meter(self.f, metertype='semi', metersize=100, amounttotal=100,
                           amountused=FV, stepsize=1, subtextstyle='primary',
                           interactive=True, stripethickness=2, arcrange=180,
                           arcoffset=180, subtext='Returns', textfont=('Sans', 12), subtextfont=('Sans', 8))
        meter2.place(x=270, y=60)


if __name__ == '__main__':
    obj = PortfolioClass('light')