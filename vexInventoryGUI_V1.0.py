import tkinter as tk
import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import sqlite3, sys
from beautifultable import BeautifulTable

class Main(tk.Tk):
    def __init__(self, **kwargs):
        tk.Tk.__init__(self, **kwargs)

        #~ self.protocol('WM_DELETE_WINDOW', self.callback)
        self.geometry('1024x768')
        self.title('Vex Inventory System')
        self.resizable(0, 0)
        style = ttk.Style()
        style.configure('Courier.TButton', font=('Courier', 8))

        self.frames = {}
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        for frame in (homePage, searchPage, indexPage, insertDataPage): # all the frames in the stack here
            f = frame(self)
            f.grid(row=0, column=0, sticky='nsew')
            self.frames[frame] = f
        self.switch(homePage) # set the starting frame

    def switch(self, frame):
        self.frames[frame].tkraise()

    def callback(self):
        if tkinter.messagebox.askokcancel('Quit', 'Do you really wish to quit?'):
            self.destroy()

class homePage(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        # display title image
        self.vexTitle_img = tk.PhotoImage(file = 'vexTitle.png')
        vexTitlePack = tk.Label(self, image = self.vexTitle_img)
        vexTitlePack.pack()

        # goto search function button
        searchPageButton = tk.Button(self, text = 'Search', fg='red', font = 'arial, 15')
        searchPageButton.config(width = '10', height = '2')
        searchPageButton.config(command = lambda: master.switch(searchPage))
        searchPageButton.place(x = 210, y = 300)

        # goto index function button
        indexPageButton = tk.Button(self, text = 'Index', fg='red', font = 'arial, 15')
        indexPageButton.config(width = '10', height = '2')
        indexPageButton.config(command = lambda: master.switch(indexPage))
        indexPageButton.place(x = 335, y = 300)

        # goto insert data button
        insertDataPageButton = tk.Button(self, text = 'Insert Data', fg='red', font = 'arial, 15')
        insertDataPageButton.config(width = '10', height = '2')
        insertDataPageButton.config(command = lambda: master.switch(insertDataPage))
        insertDataPageButton.place(x = 460, y = 300)
        
        # quit program button
        quitButton = tk.Button(self, text = 'Quit', fg='red', font = 'arial, 15')
        quitButton.config(width = '10', height = '2')
        quitButton.config(command = self.quit)
        quitButton.place(x = 585, y = 300)

    def quit(self):
        exit()

class searchPage(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.vexTitle_img = tk.PhotoImage(file = 'vexTitle.png')
        vexTitlePack = tk.Label(self, image = self.vexTitle_img)
        vexTitlePack.pack()

        # back button
        back_button = tk.Button(self, text='Back')
        back_button.config(command=lambda: master.switch(homePage))
        back_button.place(x = 210, y = 300)

        self.chooseSearchCategory()

    def chooseSearchCategory(self):
        text = tk.Label(self, text='Choose category to search : ')
        text.place(x=250, y=300)
        self.box_value = tk.StringVar()
        self.comboBox = Combobox(self, textvariable=self.box_value)
        self.comboBox.bind('<<ComboboxSelected>>', self.searchTable)
        self.comboBox['values'] = ('Parts', 'Brains', 'Gears', 'Motors', 'Wheels', 'Others')
        self.comboBox.place(x=250, y=325)
        self.comboBox.current(0)

    def searchTable(self, event):
        global table, partValues, brainValues, gearValues, motorValues, wheelValues, otherValues
        tableChoice = self.comboBox.get()
        table = self.comboBox.get()
        self.box_value = tk.StringVar()
        self.comboBoxTwo = Combobox(self, textvariable=self.box_value)
        self.comboBoxTwo.bind('<<ComboboxSelected>>', self.getSearchQuery)
        if tableChoice == 'Parts':
            self.comboBoxTwo['values'] = (partValues)

        elif tableChoice == 'Brains':
            self.comboBoxTwo['values'] = (brainValues)

        elif tableChoice == 'Gears':
            self.comboBoxTwo['values'] = (gearValues)

        elif tableChoice == 'Motors':
            self.comboBoxTwo['values'] = (motorValues)

        elif tableChoice == 'Wheels':
            self.comboBoxTwo['values'] = (wheelValues)

        elif tableChoice == 'Others':
            self.comboBoxTwo['values'] = (otherValues)
            
        self.comboBoxTwo.place(x=250, y=350)
        self.comboBoxTwo.current(0)

    def getSearchQuery(self, event):
        global table, partsColumnHeaders, brainsColumnHeaders, gearsColumnHeaders, motorsColumnHeaders, wheelsColumnHeaders, othersColumnHeaders
        print('Table = ' + table)
        query = self.comboBoxTwo.get()
        print('Query = ' + query)
        text = tk.Label(self, text='Enter search query : ')
        text.place(x=425, y=300)
        textEntry = Entry(root, width=20)
        textEntry.place(x=425, y=325)
        def clicked():
            print(textEntry.get())
            searchData = textEntry.get()
            print('Search Data = ' + searchData)
            results = dbSearchItem(table, searchData, query)
            tablePrint = BeautifulTable()
            tablePrint.set_style(BeautifulTable.STYLE_COMPACT)
            if table == 'Parts':
                tablePrint.column_headers = ['Index', 'Name', 'Size', 'Metal', 'Availability', 'Location']

            elif table == 'Brains':
                tablePrint.column_headers = ['Index', 'Number', 'Condition', 'Competition', 'Location']

            elif table == 'Gears':
                tablePrint.column_headers = ['Index', 'Strength', 'Teeth', 'Material', 'Quantity', 'Location']

            elif table == 'Motors':
                tablePrint.column_headers = ['Index', 'Size', 'Number', 'Condition', 'Speed', 'Location']

            elif table == 'Wheels':
                tablePrint.column_headers = ['Index', 'Type', 'Quantity', 'Location']

            elif table == 'Others':
                tablePrint.column_headers = ['Index', 'Name', 'Description', 'Location']
            
            tablePrint.set_padding_widths(1)
            for row in results:
                memberList = []
                for member in row:
                    memberList.append(member)
                tablePrint.append_row(memberList)

            scrollBar = Scrollbar(self)
            scrollBar.pack(side=RIGHT, fill=Y)
            resultsText = Text(self, height=10, width=75)
            resultsText.place(x=250, y=500)
            scrollBar.config(command=resultsText.yview)
            resultsText.insert(END, tablePrint)
            print(tablePrint)
            
        clickedButton = tk.Button(root, text='Search', command=clicked)
        clickedButton.place(x=575, y=320)

class indexPage(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.vexTitle_img = tk.PhotoImage(file = 'vexTitle.png')
        vexTitlePack = tk.Label(self, image = self.vexTitle_img)
        vexTitlePack.pack()

        back_button = tk.Button(self, text='Back')
        back_button.config(command=lambda: master.switch(homePage))
        back_button.place(x = 210, y = 300)

        self.getIndexTable()

    def getIndexTable(self):
        text = Label(self, text='Choose category to display : ')
        text.place(x=250, y=300)
        self.box_value = tk.StringVar()
        self.comboBox = Combobox(self, textvariable=self.box_value)    
        self.comboBox.bind("<<ComboboxSelected>>", self.showIndexTable)
        self.comboBox['values'] = ('Parts', 'Brains', 'Gears', 'Motors', 'Wheels', 'Others')
        self.comboBox.place(x=250, y=325)
        self.comboBox.current(0)

    def showIndexTable(self, event):
        global partsColumnHeaders, brainsColumnHeaders, gearsColumnHeaders, motorsColumnHeaders, wheelsColumnHeaders, othersColumnHeaders
        columnHeadersList = [partsColumnHeaders, brainsColumnHeaders, gearsColumnHeaders, motorsColumnHeaders, wheelsColumnHeaders, othersColumnHeaders]
        tableList = ('Parts', 'Brains', 'Gears', 'Motors', 'Wheels', 'Others')
        table = self.comboBox.get()
        results = dbSearchAll(table)
        # creating the Beautiful Table for printing
        tablePrint = BeautifulTable()
        tablePrint.set_style(BeautifulTable.STYLE_COMPACT)
        i = 0
        for i in range(len(tableList)):
            if table == tableList[i]:
                columnHeaders = columnHeadersList[i]
                break

            else:
                i = i + 1
        tablePrint.column_headers = columnHeaders
        tablePrint.set_padding_widths(1)
        for row in results:
            memberList = []
            for member in row:
                memberList.append(member)
            tablePrint.append_row(memberList)

        # results text widget with scrollbar
        scrollBar = Scrollbar(self)
        scrollBar.pack(side=RIGHT, fill=Y)
        resultsText = Text(self, height=10, width=75)
        resultsText.place(x=250, y=500)
        scrollBar.config(command=resultsText.yview)
            
        resultsText.insert(END, tablePrint) # inserting data into text widget
        
        editSearchEntry = Entry(root, width=20)
        editSearchEntry.place(x=450, y=325)
        indexText = Label(root, text='Choose index number to edit : ')
        indexText.place(x=450, y=300)
        def clickedSearch():
            indexNumber = editSearchEntry.get()
            self.editItem(indexNumber, table, tablePrint, resultsText)

        clickedButton = Button(root, text='Search', command=clickedSearch)
        clickedButton.place(x=590, y=325)
        print(tablePrint)

        deleteItemSearchEntry = Entry(root, width=20)
        deleteItemSearchEntry.place(x=700, y=325)
        deleteText = Label(root, text='Choose index number to remove : ')
        deleteText.place(x=700, y=300)
        def clickedDelete():
            indexNumber = deleteItemSearchEntry.get()
            dbRemoveItem(indexNumber, table)
            tablePrint = BeautifulTable()
            tablePrint.set_style(BeautifulTable.STYLE_COMPACT)

            results = dbSearchAll(table)
            tablePrint.column_headers = columnHeaders
            tablePrint.set_padding_widths(1)
            for row in results:
                memberList = []
                for member in row:
                    memberList.append(member)
                tablePrint.append_row(memberList)
                
            resultsText.delete('1.0', END)
            resultsText.insert(END, tablePrint)
            resultsText.update()
            
        deleteButton = Button(root, text='Delete', command=clickedDelete)
        deleteButton.place(x=840, y=325)

    def editItem(self, indexNumber, table, tablePrint, resultsText): # function to edit items from a table
        global partsColumnHeaders, brainsColumnHeaders, gearsColumnHeaders, motorsColumnHeaders, wheelsColumnHeaders, othersColumnHeaders
        columnHeadersList = [partsColumnHeaders, brainsColumnHeaders, gearsColumnHeaders, motorsColumnHeaders, wheelsColumnHeaders, othersColumnHeaders]
        global partValues, brainValues, gearValues, motorValues, wheelValues, otherValues
        itemValuesList = [partValues, brainValues, gearValues, motorValues, wheelValues, otherValues]
        tableList = ['Parts', 'Brains', 'Gears', 'Motors', 'Wheels', 'Others']
        data = []
        i = 0
        print(table)
        var = IntVar()
        for i in range(len(tableList)):
            if tableList[i] == table:
                itemValues = itemValuesList[i]
                columnHeaders = columnHeadersList[i]
                break
            
            else:
                i = i + 1
                
        def clicked():
            value = valueEntryBox.get()
            var.set(1)
            if value.lower() == 'keep':
                value = tablePrint[int(indexNumber) - 1]['{}'.format(columnHeaders[i + 1])]
                
            print(value)    
            data.append(value)
            
        i = 0
        for i in range(len(itemValues)):
            valueForEditText = Label(self, text='Input "keep" to keep the same value or input new value for : ')
            valueForEditText.place(x=250, y=350)
            valueForEdit = Text(self, height=1, width=20)
            valueForEdit.insert(END, itemValues[i])
            valueForEdit.place(x=575, y=350)
            valueEntryBox = Entry(root, width=20)
            valueEntryBox.place(x=250, y=375)
            confirmValueButton = Button(self, text='Enter')
            confirmValueButton.config(command=clicked)
            confirmValueButton.place(x=400, y=375)
            confirmValueButton.wait_variable(var)
                
            i = i + 1
            
        data.append(indexNumber)
        print(data)
        dbEditItem(data, table)
        successEditLabel = Label(self, text='Edit was successful')
        successEditLabel.place(x=250, y=400)
        results = dbSearchAll(table)
        
        tablePrint = BeautifulTable()
        tablePrint.set_style(BeautifulTable.STYLE_COMPACT)
        tablePrint.column_headers = columnHeaders
        tablePrint.set_padding_widths(1)
        for row in results:
            memberList = []
            for member in row:
                memberList.append(member)
            tablePrint.append_row(memberList)
        
        resultsText.delete('1.0', END)
        resultsText.insert(END, tablePrint)
        resultsText.update()


class insertDataPage(tk.Frame): 
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.vexTitle_img = tk.PhotoImage(file = 'vexTitle.png')
        vexTitlePack = tk.Label(self, image = self.vexTitle_img)
        vexTitlePack.pack()

        back_button = tk.Button(self, text='Back')
        back_button.config(command=lambda: master.switch(homePage))
        back_button.place(x = 210, y = 300)

        self.getInsertTable()

    def getInsertTable(self): # function to get the table for inserting data into
        text = Label(self, text='Choose category to insert data into : ')
        text.place(x=250, y=300)
        self.box_value = tk.StringVar()
        self.comboBox = Combobox(self, textvariable=self.box_value)    
        self.comboBox.bind("<<ComboboxSelected>>", self.insertData)
        self.comboBox['values'] = ('Parts', 'Brains', 'Gears', 'Motors', 'Wheels', 'Others')
        self.comboBox.place(x=250, y=325)
        self.comboBox.current(0)

    def insertData(self, event):
        table = self.comboBox.get()
        global partsColumnHeaders, brainsColumnHeaders, gearsColumnHeaders, motorsColumnHeaders, wheelsColumnHeaders, othersColumnHeaders
        columnHeadersList = [partsColumnHeaders, brainsColumnHeaders, gearsColumnHeaders, motorsColumnHeaders, wheelsColumnHeaders, othersColumnHeaders]
        global partValues, brainValues, gearValues, motorValues, wheelValues, otherValues
        itemValuesList = [partValues, brainValues, gearValues, motorValues, wheelValues, otherValues]
        tableList = ('Parts', 'Brains', 'Gears', 'Motors', 'Wheels', 'Others')
        table = self.comboBox.get()
        results = dbSearchAll(table)
        tablePrint = BeautifulTable()
        tablePrint.set_style(BeautifulTable.STYLE_COMPACT)
        i = 0
        for i in range(len(tableList)):
            if table == tableList[i]:
                itemValues = itemValuesList[i]
                columnHeaders = columnHeadersList[i]
                break

            else:
                i = i + 1
        tablePrint.column_headers = columnHeaders
        tablePrint.set_padding_widths(1)
        for row in results:
            memberList = []
            for member in row:
                memberList.append(member)
            tablePrint.append_row(memberList)

        scrollBar = Scrollbar(self)
        scrollBar.pack(side=RIGHT, fill=Y)
        resultsText = Text(self, height=10, width=75)
        resultsText.place(x=250, y=500)
        scrollBar.config(command=resultsText.yview)
            
        resultsText.insert(END, tablePrint)
        data = []
        var = IntVar()

        def clicked():
            value = valueEntryBox.get()
            data.append(value)
            var.set(1)

        i = 0
        for i in range(len(itemValues)):
            valueForEditText = Label(self, text='Input value for : ')
            valueForEditText.place(x=250, y=350)
            valueForEdit = Text(self, height=1, width=20)
            valueForEdit.insert(END, itemValues[i])
            valueForEdit.place(x=350, y=350)
            valueEntryBox = Entry(root, width=20)
            valueEntryBox.place(x=250, y=375)
            confirmValueButton = Button(self, text='Enter')
            confirmValueButton.config(command=clicked)
            confirmValueButton.place(x=400, y=375)
            confirmValueButton.wait_variable(var)
                
            i = i + 1

        dbInsertItem(data, table)
        
        results = dbSearchAll(table)
        tablePrint = BeautifulTable()
        tablePrint.set_style(BeautifulTable.STYLE_COMPACT)
        tablePrint.column_headers = columnHeaders
        tablePrint.set_padding_widths(1)
        for row in results:
            memberList = []
            for member in row:
                memberList.append(member)
            tablePrint.append_row(memberList)
            
        resultsText.delete('1.0', END)
        resultsText.insert(END, tablePrint)
        resultsText.update()

#SQL Database functions
def dbSearchItem(table, data, query):
    with sqlite3.connect('vexInventory.db') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute('select * from ' + table + ' where ' + query + '=?', (data,))
        results = cursor.fetchall()
        return results

def dbSearchAll(table):
    with sqlite3.connect('vexInventory.db') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute('select * from ' + table)
        results = cursor.fetchall()
        return results

def dbEditItem(data, table):
    with sqlite3.connect('vexInventory.db') as db:
        cursor = db.cursor()
        if table == 'Parts':
            sql = 'update Parts set partName=?, partSize=?, partMetal=?, partAvailability=?, partLocation=? where productID=?'

        elif table == 'Brains':
            sql = 'update Brains set brainNumber=?, brainCondition=?, brainCompetition=?, brainLocation=? where productID=?'

        elif table == 'Gears':
            sql = 'update Gears set gearStrength=?, gearTeeth=?, gearMaterial=?, gearQuantity=?, gearLocation=? where productID=?'

        elif table == 'Motors':
            sql = 'update Motors set motorSize=?, motorNumber=?, motorCondition=?, motorSpeed=?, motorLocation=? where productID=?'

        elif table == 'Wheels':
            sql = 'update Wheels set wheelType=?, wheelQuantity=?, wheelLocation=? where productID=?'

        elif table == 'Others':
            sql = 'update Others set otherName=?, otherDescription=?, otherLocation=? where productID=?'

        cursor.execute(sql, data)
        db.commit()

def dbRemoveItem(data, table):
    with sqlite3.connect('vexInventory.db') as db:
        cursor = db.cursor()
        cursor.execute('delete from ' + table + ' where productID=?', (data,))
        db.commit()

def dbInsertItem(values, table):
    with sqlite3.connect('vexInventory.db') as db:
        cursor = db.cursor()
        if table == 'Parts':
            sql = 'insert into Parts (partName, partSize, partMetal, partAvailability, partLocation) values (?, ?, ?, ?, ?)'

        elif table == 'Brains':
            sql = 'insert into Brains (brainNumber, brainCondition, brainCompetition, brainLocation) values (?, ?, ?, ?)'

        elif table == 'Gears':
            sql = 'insert into Gears (gearStrength, gearTeeth, gearMaterial, gearQuantity, gearLocation) values (?, ?, ?, ?, ?)'

        elif table == 'Motors':
            sql = 'insert into Motors (motorSize, motorNumber, motorCondition, motorSpeed, motorLocation) values (?, ?, ?, ?, ?)'

        elif table == 'Wheels':
            sql = 'insert into Wheels (wheelType, wheelQuantity, wheelLocation) values (?, ?, ?)'

        elif table == 'Others':
            sql = 'insert into Others (otherName, otherDescription, otherLocation) values (?, ?, ?)'
        
        cursor.execute(sql, values)
        db.commit()

# variables for global use
partsColumnHeaders = ['Index', 'Name', 'Size', 'Metal', 'Availability', 'Location']
brainsColumnHeaders = ['Index', 'Brain Number', 'Condition', 'Competition', 'Location']
gearsColumnHeaders = ['Index', 'Strength', 'Teeth', 'Material', 'Quantity', 'Location']
motorsColumnHeaders = ['Index', 'Size', 'Motor Number', 'Condition', 'Motor Speed', 'Location']
wheelsColumnHeaders = ['Index', 'Type', 'Quantity', 'Location']
othersColumnHeaders = ['Index', 'Name', 'Description', 'Location']

partValues = ('partName', 'partSize', 'partMetal', 'partAvailability', 'partLocation')
brainValues = ('brainNumber', 'brainCondition', 'brainCompetition', 'brainLocation')
gearValues = ('gearStrength', 'gearTeeth', 'gearMaterial', 'gearQuanity', 'gearLocation')
motorValues = ('motorSize', 'motorNumber', 'motorCondition', 'motorSpeed', 'motorLocation')
wheelValues = ('wheelType', 'wheelQuantity', 'wheelLocation')
otherValues = ('otherName', 'otherDescription', 'otherLocation')
        
root = Main()
root.mainloop()
