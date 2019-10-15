import sqlite3, sys
from beautifultable import BeautifulTable

# SQL functions
def createTable(dbName, tableName, sql): # function to re-format a table
    with sqlite3.connect(dbName) as db:
        cursor = db.cursor()
        cursor.execute('select name from sqlite_master where name=?', (tableName,))
        result = cursor.fetchall()
        keepTable = True
        if len(result) == 1:
            response = input('The table {0} already exists, do you wish to recreate it (y/n): '.format(tableName))
            if response == 'y':
                keepTable = False
                print('\n' + 'The {0} table will be recreated - all existing data will be lost'.format(tableName))
                cursor.execute('drop table if exists {0}'.format(tableName))
                db.commit()
            else:
                print('\n' + 'The existing table was kept')
        else:
            print('\n' + 'The table "{0}" has been created'.format(tableName))
            keepTable = False

        if not keepTable:
            cursor.execute(sql)
            db.commit()

def insertItem(values, dbName, table): # function to insert an item into a table
    with sqlite3.connect(dbName) as db:
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

def editItem(data, dbName, table): # function to edit an item within a table
    with sqlite3.connect(dbName) as db:
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

def removeItem(data, table): # function to remove an item from a table
    dbName = 'vexInventory.db'
    with sqlite3.connect(dbName) as db:
        cursor = db.cursor()
        cursor.execute('delete from ' + table + ' where productID=?', (data,))
        db.commit()

def searchItem(table, data, query): # function to search for an item within a table
    dbName = 'vexInventory.db'
    with sqlite3.connect(dbName) as db:
        cursor = db.cursor()
        cursor.execute('select * from ' + table + ' where ' + query + '=?', (data,))
        results = cursor.fetchall()
        return results

# normal python functions
def gatherItemSearch(): # function to gather item to search for
    global tableList
    print(tableList)
    resultsPrint = BeautifulTable()
    resultsPrint.set_style(BeautifulTable.STYLE_COMPACT)
    resultsPrint.set_padding_widths(1)
    tableChoice = input('Input Choice : ')
    if tableChoice == '1':
        resultsPrint.column_headers = ['Index', 'Name', 'Size', 'Metal', 'Availability', 'Location']
        table = 'Parts'
        partData = ['Part Name', 'Part Size', 'Part Metal', 'Part Availability', 'Part Location']
        rawPartData = ['partName', 'partSize', 'partMetal', 'partAvailability', 'partLocation']
        i = 0
        for item in partData:
            print('Press enter to skip to next search option')
            searchData = input('Input {} : '.format(partData[i]))
            if len(searchData) > 0:
                query = rawPartData[i]
                break
            
            i = i + 1
        results = searchItem(table, searchData, query)

    elif tableChoice == '2':
        resultsPrint.column_headers = ['Index', 'Number', 'Condition', 'Competition', 'Location']
        table = 'Brains'
        brainData = ['Brain Number', 'Brain Condition', 'Brain Competition', 'Brain Location']
        rawBrainData = ['brainNumber', 'brainCondition', 'brainCompetition', 'brainLocation']
        i = 0
        for item in brainData:
            print('Press enter to skip to next search option')
            searchData = input('Input {} : '.format(brainData[i]))
            if len(searchData) > 0:
                query = rawBrainData[i]
                break
            
            i = i + 1
        results = searchItem(table, searchData, query)

    elif tableChoice == '3':
        resultsPrint.column_headers = ['Index', 'Strength', 'Teeth', 'Material', 'Quantity', 'Location']
        table = 'Gears'
        gearData = ['Gear Strength', 'Gear Teeth', 'Gear Material', 'Gear Quantity', 'Gear Location']
        rawGearData = ['gearStrength', 'gearTeeth', 'gearMaterial', 'gearQuanity', 'gearLocation']
        i = 0
        for item in gearData:
            print('Press enter to skip to next search option')
            searchData = input('Input {} : '.format(gearData[i]))
            if len(searchData) > 0:
                query = rawGearData[i]
                break
            
            i = i + 1
        results = searchItem(table, searchData, query)

    elif tableChoice == '4':
        resultsPrint.column_headers = ['Index', 'Size', 'Number', 'Condition', 'Speed', 'Location']
        table = 'Motors'
        motorData = ['Motor Size', 'Motor Number', 'Motor Condition', 'Motor Speed', 'Motor Location']
        rawMotorData = ['motorSize', 'motorNumber', 'motorCondition', 'motorSpeed', 'motorLocation']
        i = 0
        for item in motorData:
            print('Press enter to skip to next search option')
            searchData = input('Input {} : '.format(motorData[i]))
            if len(searchData) > 0:
                query = rawMotorData[i]
                break
            
            i = i + 1
        results = searchItem(table, searchData, query)

    elif tableChoice == '5':
        resultsPrint.column_headers = ['Index', 'Type', 'Quantity', 'Location']
        table = 'Wheels'
        wheelData = ['Wheel Type', 'Wheel Quantity', 'Wheel Location']
        rawWheelData = ['wheelType', 'wheelQuantity', 'wheelLocation']
        i = 0
        for item in wheelData:
            print('Press enter to skip to next search option')
            searchData = input('Input {} : '.format(wheelData[i]))
            if len(searchData) > 0:
                query = rawWheelData[i]
                break
            
            i = i + 1
        results = searchItem(table, searchData, query)

    elif tableChoice == '6':
        resultsPrint.column_headers = ['Index', 'Name', 'Description', 'Location']
        table = 'Others'
        otherData = ['Other Name', 'Other Description', 'Other Location']
        rawOtherData = ['otherName', 'otherDescription', 'otherLocation']
        i = 0
        for item in otherData:
            print('Press enter to skip to next search option')
            searchData = input('Input {} : '.format(otherData[i]))
            if len(searchData) > 0:
                query = rawOtherData[i]
                break
            
            i = i + 1
        results = searchItem(table, searchData, query)

    elif tableChoice == '7':
            userLogin()

    else:
        print('Error : Please input a number associated with an option')
        input('Enter to continue...')

    for row in results:
        memberList = []
        for member in row:
            memberList.append(member)
        resultsPrint.append_row(memberList)

    print('\n')
    print(resultsPrint)
        
def userLogin(): # function for a user log in to navigate the program
    global userOptionList
    while True:
        print(userOptionList)
        userOptionChoice = input('Input choice : ')
        if userOptionChoice == '1':
            operatorLevel = 'user'
            itemEditor(operatorLevel)

        elif userOptionChoice == '2':
            gatherItemSearch()
            
            
        elif userOptionChoice == '3':
            chooseLogin()
            
        elif userOptionChoice == '0':
            sys.exit()

        else:
            print('Error : Please input a number associated with an option')
            input('Enter to continue...')


def adminLogin(): # function for an admin log in to navigate the program
    global adminOptionList
    while True:
        print(adminOptionList)
        adminOptionChoice = input('Input choice : ')
        
        if adminOptionChoice == '1':
            recreateTable()

        elif adminOptionChoice == '2':
            addItem()

        elif adminOptionChoice == '3':
            operatorLevel = 'admin'
            itemEditor(operatorLevel)

        elif adminOptionChoice == '4':
            deleteItem()

        elif adminOptionChoice == '5':
            chooseLogin()

        elif adminOptionChoice == '0':
            sys.exit()

        else:
            print('Error : Please input a number associated with an option')
            input('Enter to continue...')
            
def deleteItem(): # function to gather item to delete from a table
    global tableList
    print (tableList)
    tableChoice = input('Table Choice : ')
    if tableChoice == '1':
        table = 'Parts'
        productID = input('Input Product ID of the item you wish to delete : ')
        while productID.isdigit() != True:
            print('Error : Please input an integer')
            productID = input('Input Product ID of the item you wish to delete : ')    
        removeItem(productID, table)
        print ('Item Removed...')
        adminLogin()

    elif tableChoice == '2':
        table = 'Brains'
        productID = input('Input Product ID of the item you wish to delete : ')
        while productID.isdigit() != True:
            print('Error : Please input an integer')
            productID = input('Input Product ID of the item you wish to delete : ')
        removeItem(productID, table)
        print ('Item Removed...')
        adminLogin()

    elif tableChoice == '3':
        table = 'Gears'
        productID = input('Input Product ID of the item you wish to delete : ')
        while productID.isdigit() != True:
            print('Error : Please input an integer')
            productID = input('Input Product ID of the item you wish to delete : ')
        removeItem(productID, table)
        print ('Item Removed...')
        adminLogin()

    elif tableChoice == '4':
        table = 'Motors'
        productID = input('Input Product ID of the item you wish to delete : ')
        while productID.isdigit() != True:
            print('Error : Please input an integer')
            productID = input('Input Product ID of the item you wish to delete : ')
        removeItem(productID, table)
        print ('Item Removed...')
        adminLogin()

    elif tableChoice == '5':
        table = 'Wheels'
        productID = input('Input Product ID of the item you wish to delete : ')
        while productID.isdigit() != True:
            print('Error : Please input an integer')
            productID = input('Input Product ID of the item you wish to delete : ')
        removeItem(productID, table)
        print ('Item Removed...')
        adminLogin()
        

    elif tableChoice == '6':
        table = 'Others'
        productID = input('Input Product ID of the item you wish to delete : ')
        while productID.isdigit() != True:
            print('Error : Please input an integer')
            productID = input('Input Product ID of the item you wish to delete : ')
        removeItem(productID, table)
        print ('Item Removed...')
        adminLogin()

    elif optionChoice == '7':
            adminLogin()

    else:
        print('Error : Please input a number associated with an option')
        input('Enter to continue...')

    

def addItem(): # function to gather item to add to a table
    dbName = 'vexInventory.db'
    while True:
        print('Please choose a category to append')
        print(tableList)
        tableChoice = input('Category : ')
        if tableChoice == '1':
            table = 'Parts'
            partName = input('Part Name : ')
            partSize = input('Part Size : ')
            partMetal = input('Part Metal : ')
            partAvailability = input('Part Availability : ')
            partLocation = input('Part Location : ')
            values = (partName, partSize, partMetal, partAvailability, partLocation)
            insertItem(values, dbName, table)
            break

        elif tableChoice == '2':
            table = 'Brains'
            while True:
                brainNumber = input('Brain Number : ')
                if brainNumber.isdigit() == True:
                    break

                else:
                    print('Error : Please input an integer')
                    input('Enter to continue...')
            
            while True:
                print (conditionChart)
                brainCondition = input('Brain Condition : ')
                if brainCondition in conditionList:
                    break

                else:
                    print('Error : Condition input does not match a variable on the chart')
                    input('Enter to continue...')
                    
            while True:
                competitionInput = input('Brain Competition (y/n) : ')
                if competitionInput == 'y':
                    brainCompetition = 'Yes'
                    break

                elif competitionInput == 'n':
                    brainCompetition = 'No'
                    break

                else:
                    print('Error : Please input either "y" or "n"')
                    input('Enter to continue...')

            brainLocation = input('Brain Location : ')
            values = (brainNumber, brainCondition, brainCompetition, brainLocation)
            insertItem(values, dbName, table)
            break

        elif tableChoice == '3':
            table = 'Gears'
            gearStrength = input('Gear Strength : ')
            gearTeeth = input('Gear Teeth : ')
            gearMaterial = input('Gear Material : ')
            gearQuantity = input('Gear Quantity : ')
            gearLocation = input('Gear Location : ')
            values = (gearStrength, gearTeeth, gearMaterial, gearQuantity, gearLocation)
            insertItem(values, dbName, table)

        elif tableChoice == '4':
            table = 'Motors'
            motorSize = input('Motor Size : ')
            motorNumber = input('Motor Number : ')
            motorCondition = input('Motor Condition : ')
            motorSpeed = input('Motor Speed : ')
            motorLocation = input('Motor Location : ')
            values = (motorSize, motorNumber, motorCondition, motorSpeed, motorLocation)
            insertItem(values, dbName, table)

        elif tableChoice == '5':
            table = 'Wheels'
            wheelType = input('Wheel Type : ')
            wheelQuantity = input('Wheen Quantity : ')
            wheelLocation = input('Wheel Location : ')
            values = (wheelType, wheelQuantity, wheelLocation)
            insertItem(values, dbName, table)

        elif tableChoice == '6':
            table = 'Others'
            otherName = input('Name : ')
            otherDescription = input('Description : ')
            otherLocation = input('Location : ' )
            values = (otherName, otherDescription, otherLocation)
            insertItem(values, dbName, table)

        elif tableChoice == '7':
            adminLogin()
            
        else:
            print('Error : Please input a number associated with an option')
            input('Enter to continue...')
    

def recreateTable(): # function to choose which table to re-create
    global tableList
    print (tableList)
    tableChoice = input('Table to recreate : ')
    if tableChoice == '1':
        dbName = 'vexInventory.db'
        sql = '''create table Parts
                (productID integer,
                partName text,
                partSize blob,
                partMetal text,
                partAvailability integer,
                partLocation text,
                primary key(productID))'''
        createTable(dbName, 'Parts', sql)

    elif tableChoice == '2':
        dbName = 'vexInventory.db'
        sql = '''create table Brains
                (productID integer,
                brainNumber integer,
                brainCondition text,
                brainCompetition text,
                brainLocation text,
                primary key(productID))'''
        createTable(dbName, 'Brains', sql)

    elif tableChoice == '3':
        dbName = 'vexInventory.db'
        sql = '''create table Gears
                (productID integer,
                gearStrength text,
                gearTeeth integer,
                gearMaterial text,
                gearQuantity integer,
                gearLocation text,
                primary key(productID))'''
        createTable(dbName, 'Gears', sql)

    elif tableChoice == '4':
        dbName = 'vexInventory.db'
        sql = '''create table Motors
                (productID integer,
                motorSize blob,
                motorNumber integer,
                motorCondition text,
                motorSpeed text,
                motorLocation text,
                primary key(productID))'''
        createTable(dbName, 'Motors', sql)

    elif tableChoice == '5':
        dbName = 'vexInventory.db'
        sql = '''create table Wheels
                (productID integer,
                wheelType text,
                wheelQuantity integer,
                wheelLocation text,
                primary key(productID))'''
        createTable(dbName, 'Wheels', sql)

    elif tableChoice == '6':
        dbName = 'vexInventory.db'
        sql = '''create table Others
                (productID integer,
                otherName text,
                otherDescription blob,
                otherLocation text,
                primary key(productID))'''
        createTable(dbName, 'Others', sql)

    elif tableChoice == '7':
            adminLogin()

    else:
        print('Error : Please input a valid number')
        input('Enter to continue...')
    

def chooseLogin(): # starting function to log in to the program with different permission levels
    global operatorLevelPrint
    while True:
        print(operatorLevelPrint)
        operatorChoice = input('Input choice : ')
        if operatorChoice == '1':
            while True:
                adminUser = input('Username : ')
                adminPass = input('Password : ')
                if adminUser == 'admin' and adminPass == 'admin':
                    print('Logging in as Admin...')
                    adminLogin()

                else:
                    print('Error : Username and/or password incorrect')
                    while True:
                        userChoice = input('Do you wish to retry? (y/n) : ')
                        if userChoice == 'y':
                            input('Enter to continue...')
                            break

                        if userChoice == 'n':
                            return

                        else:
                            print('Error : Please input either "y" or "n"')
                            input('Enter to continue...')


        elif operatorChoice == '2':
            print('Logging in as User...')
            userLogin()

        elif operatorChoice == '0':
            sys.exit()

        else:
            print('Error : Please input a number associated with an option')
            input('Enter to continue...')

def itemEditor(operatorLevel): # function to gather information to edit an item
    dbName = 'vexInventory.db'
    while True:
        print('Please choose a category to edit')
        print(tableList)
        optionChoice = input('Category : ')
        if optionChoice == '1':
            table = 'Parts'
            partName = input('Part Name : ')
            partSize = input('Part Size : ')
            partMetal = input('Part Metal : ')
            partAvailability = input('Part Quantity : ')
            partLocation = input('Part Location : ')
            productID = input('Product ID : ')
            data = (partName, partSize, partMetal, partAvailability, partLocation, productID)
            editItem(data, dbName, table)
            break

        elif optionChoice == '2':
            table = 'Brains'
            while True:
                brainNumber = input('Brain Number : ')
                if brainNumber.isdigit() == True:
                    break

                else:
                    print('Error : Please input an integer')
                    input('Enter to continue...')
            
            while True:
                print (conditionChart)
                brainCondition = input('Brain Condition : ')
                if brainCondition in conditionList:
                    break

                else:
                    print('Error : Condition input does not match a variable on the chart')
                    input('Enter to continue...')
                    
            while True:
                competitionInput = input('Brain Competition (y/n) : ')
                if competitionInput == 'y':
                    brainCompetition = 'Yes'
                    break

                elif competitionInput == 'n':
                    brainCompetition = 'No'
                    break

                else:
                    print('Error : Please input either "y" or "n"')
                    input('Enter to continue...')

            brainLocation = input('Brain Location : ')
            productID = input('Product ID : ')
            data = (brainNumber, brainCondition, brainCompetition, brainLocation, productID)
            editItem(data, dbName, table)
            break

        elif optionChoice == '3':
            table = 'Gears'
            gearStrengh = input('Gear Strength : ')
            gearTeeth = input('Gear Teeth : ')
            gearMaterial = input('Gear Material : ')
            gearQuantity = input('Gear Quantity : ')
            gearLocation = input('Gear Location : ')
            productID = input('Product ID : ')
            data = (gearStrength, gearTeeth, gearMaterial, gearQuantity, gearLocation, productID)
            editItem(data, dbName, table)

        elif optionChoice == '4':
            table = 'Motors'
            motorSize = input('Motor Size : ')
            motorNumber = input('Motor Number : ')
            motorCondition = input('Motor Condition : ')
            motorSpeed = input('Motor Speed : ')
            motorLocation = input('Motor Location : ')
            productID = input('Product ID : ')
            data = (motorSize, motorNumber, motorCondition, motorSpeed, motorLocation, productID)
            editItem(data, dbName, table)

        elif optionChoice == '5':
            table = 'Wheels'
            wheelType = input('Wheel Type : ')
            wheelQuantity = input('Wheen Quantity : ')
            wheelLocation = input('Wheel Location : ')
            productID = input('Product ID : ')
            data = (wheelType, wheelQuantity, wheelLocation, productID)
            editItem(data, dbName, table)

        elif optionChoice == '6':
            table = 'Others'
            otherName = input('Name : ')
            otherDescription = input('Description : ')
            otherLocation = input('Location : ' )
            productID = input('Product ID : ')
            data = (otherName, otherDescription, otherLocation, productID)
            editItem(data, dbName, table)


        elif optionChoice == '7':
            if operatorLevel == 'admin':
                adminLogin()

            elif operatorLevel == 'user':
                userLogin()
            
        else:
            print('Error : Please input a number associated with an option')
            input('Enter to continue...')

# Lists for global use
tableList = ('''
1. Parts
2. Brains
3. Gears
4. Motors
5. Wheels
6. Others
7. Back

''')

adminOptionList = ('''
Menu

1. Recreate Table
2. Add new item
3. Edit existing item
4. Delete existing item
5. Logout
0. Exit

''')
    
userOptionList = ('''
Menu

1. Edit existing item
2. Search for item
3. Logout
0. Exit
''')

operatorLevelPrint = ('''
Vex Inventory System

1. Admin
2. User
0. Exit
''')

conditionChart = ('''
Condition Chart

Perfect
Usable
Prolematic
Unusable
''')

conditionList = ['Perfect', 'Usable', 'Problematic', 'Unusable']

if __name__ == '__main__':
    chooseLogin()
