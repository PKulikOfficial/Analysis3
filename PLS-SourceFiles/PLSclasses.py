#Classes of the PLS

import json, csv
from random import randint


#BEGIN ID-Generator
b_currentid = 100000
bi_currentid = 100000
c_currentid = 100000
def generateid(t):
    global b_currentid, bi_currentid, c_currentid
    if t == "B":
        b_currentid +=1
        return t+str(b_currentid)
    elif t == "BI":
        bi_currentid += 1
        return t+str(bi_currentid)
    elif t == "C":
        c_currentid += 1
        return t+str(c_currentid)
#END ID-Generator

#BEGIN PublicLibrary Class
class PublicLibrary:
    def __init__(self):
        self.catalog = Catalog()
        self.loanadministration = LoanAdministration()

    #BEGIN startProgram Method (Initializer)
    def startProgram(self,bookfile,customerfile):
        booklist = json.load(bookfile)
        for d in booklist:
            book = Book(**d)
            self.catalog.bookdict[book.id] = book
            aantalbookitems = randint(1, 6)
            for n in range(aantalbookitems):
                bookattr = dict(book.__dict__)
                del bookattr['id']
                self.catalog.addbookitem(**bookattr)
                
        csvdictreader = csv.DictReader(customerfile)
        for csvline in csvdictreader:
            customer = Customer(**csvline)
            self.loanadministration.customerdict[customer.id] = customer
    #END startProgram Method (Initializer)

    #Begin makebackup Method
    def makeBackup(self):
        #BEGIN Backup Bookset to JSON
        bd = self.catalog.bookdict
        bdforjson = {bookid: dict(bd[bookid].__dict__) for bookid in bd}
        bid = self.catalog.bookitemdict
        bidforjson = {bookitemid: bid[bookitemid].book.__dict__ for
                      bookitemid in bid}        
        bidpbd = self.catalog.bookitemsperbookdict
        json.dump([bdforjson,bidforjson,bidpbd], open('backup/BackupBooks.json', 'w', encoding = 'UTF-8'))
        #END Backup Bookset to JSON

        #Begin Backup LoanAdministraion to JSON
        lb = self.loanadministration.loanitemdict
        lbi = self.loanadministration.loanitemsperbookitem
        lbc = self.loanadministration.loanitemspercustomer
        json.dump([lb,lbi,lbc], open("backup/BackupLoanAdministration.json", 'w', encoding = 'UTF-8'))
        #END Backup LoanAdministration to JSON
        #BEGIN Backup Customer to CSV
        with open('backup/BackupCustomers.csv', 'w', newline='') as new_file:
            fieldnames = ['id','Number', 'Gender', 'NameSet','GivenName',
                          'Surname','StreetAddress','ZipCode','City',
                          'EmailAddress','Username','TelephoneNumber']
            csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames)
            csv_writer.writeheader()

            counter = 1
            while counter < len(self.loanadministration.customerdict)+1:
                show = "C" + str(100000+counter)
                load_customer = self.loanadministration.customerdict[show]
                csv_writer.writerow({'id': load_customer.id, 'Number': load_customer.Number,
                                     'Gender': load_customer.Gender,'NameSet': load_customer.NameSet,
                                     'GivenName': load_customer.GivenName,'Surname': load_customer.Surname,
                                     'StreetAddress': load_customer.StreetAddress,'ZipCode': load_customer.ZipCode,
                                     'City': load_customer.City,'EmailAddress': load_customer.EmailAddress,
                                     'Username': load_customer.Username,'TelephoneNumber': load_customer.TelephoneNumber})
                counter += 1
        #END Backup Customer to CSV
    #END makebackup Method

                
    #BEGIN restore backup Method
    def restoreBackup(self):
        #BEGIN Value resetting
        global b_currentid, bi_currentid, c_currentid
        b_currentid = 100000
        bi_currentid = 100000
        c_currentid = 100000

        self.catalog.bookdict = {}
        self.catalog.bookitemdict = {}
        self.catalog.bookitemsperbookdict = {}

        self.loanadministration.customerdict = {}
        self.loanadministration.loanitemdict = {}
        self.loanadministration.loanitemsperbookitem = {}
        self.loanadministration.loanitemspercustomer = {}
        #END Value resetting
        
        #BEGIN BOOKS restore
        with open("backup/BackupBooks.json") as book_json:
            restorebooks = json.load(book_json)
            b = restorebooks[0]
            amountofbid = restorebooks[2]
            for d in b:
                temp_book = dict(b[d])
                book = Book(**temp_book)
                self.catalog.bookdict[book.id] = book
                for amount in range(len(amountofbid[book.id])):
                    bookattr = dict(book.__dict__)
                    del bookattr['id']
                    self.catalog.addbookitem(**bookattr)                    
        #END BOOKS restore
        #Begin Customers restore
        with open("backup/BackupCustomers.csv") as customer_csv:                
            csvdictreader = csv.DictReader(customer_csv, delimiter=',')
            for csvline in csvdictreader:
                customer = Customer(**csvline)
                self.loanadministration.customerdict[customer.id] = customer
        #END Customers restore
        #Begin Loan Administration restore
        with open("backup/BackupLoanAdministration.json") as loan_json:            
            restoreadmin = json.load(loan_json)
            self.loanadministration.loanitemdict = restoreadmin[0]
            self.loanadministration.loanitemsperbookitem = restoreadmin[1]
            self.loanadministration.loanitemspercustomer = restoreadmin[2]
        #END Loan Administration restore
    #END restore backup Method
#END PublicLibrary Class

#BEGIN Book Class
class Book:
    def __init__(self, **attributedict):
        self.id = generateid('B')
        for key in attributedict:
            setattr(self, key, attributedict[key])
#END Book Class

#Begin BookItem Class        
class BookItem:
    def __init__(self, book):
        self.id = generateid('BI')
        self.book = book
#END BookItem Class

#BEGIN Catalog Class
class Catalog:
    def __init__(self):
        self.bookdict = {}
        self.bookitemdict = {}
        self.bookitemsperbookdict = {}
        
    #BEGIN searchbook Method
    def searchbook(self, **searchattributes):
        return [id for id in self.bookdict if
                all(searchattributes[k] == getattr(self.bookdict[id], k) for
                    k in searchattributes)]
    #END searchbook Method

    #BEGIN addbookitem Method
    def addbookitem(self, **bookattributes):
        bookpresentlist = self.searchbook(**bookattributes)
        if bookpresentlist == []:
            book = Book(**bookattributes)
            self.bookdict[book.id] = book
        else:
            bookid = bookpresentlist[0]
            book = self.bookdict[bookid]
        bookitem = BookItem(book)
        self.bookitemdict[bookitem.id] = bookitem
        bookitemid = bookitem.id
        bookid = book.id
        if bookid in self.bookitemsperbookdict:
            self.bookitemsperbookdict[bookid].append(bookitemid)
        else:
            self.bookitemsperbookdict[bookid] = [bookitemid]
    #END addbookitem Method

    #BEGIN newBookItem Method
    def newBookItem(self):
        for bookinfo in self.bookdict:
            print("Book ID: " + self.bookdict[bookinfo].id + "     Book Name: " +
                  self.bookdict[bookinfo].title)
        print("\n\nWhich book has a new copy?")
        book = input("Input: ")
        if book in self.bookdict:
            book = self.bookdict[book]
            bookattr = dict(book.__dict__)
            del bookattr['id']
            self.addbookitem(**bookattr)
            print("A new copy has been added succesfully")
        else:
            print("Please try again")
            newbookItem()
    #END newBookItem Method

    #BEGIN searchspecificbook Method
    def searchSpecificBook(self, loanadministration):
        print("Please fill in the field to search with that value.\nIf you don't want to search with that criteria then\n"+
              "Please click on ENTER\n\n")
        
        idinput = input("BOOK ID: ")
        author = input("Author: ")
        country = input("Country: ")
        language = input("Language: ")
        title = input("Title: ")
        year = input("Year: ")

        #BEGIN Value Checker
        searcher = {}
        if idinput == '':
            pass
        else:
            searcher['id'] = idinput

        if author == '':
            pass
        else:
            searcher['author'] = author

        if country == '':
            pass
        else:
            searcher['country'] = country

        if language == '':
            pass
        else:
            searcher['language'] = language

        if title == '':
            pass
        else:
            searcher['title'] = title

        if year == '':
            pass
        else:
            searcher['year'] = year
        #END Value Checker
            
        print(5* "\n")
        counter = 0
        for bookinfo in self.bookdict:
            if searcher.items() <= self.bookdict[bookinfo].__dict__.items():
                print("Book ID: " + self.bookdict[bookinfo].id + "     Book Name: " +
                      self.bookdict[bookinfo].title)
                counter += 1
        if counter == 0:
            print("No Book Found")
        else:   
            print("\n\nPlease type the ID of the book that you want to see the availability from.\n")

            self.booktoloan = input("\nInput: ")
            def book_checker(inp):
                global booktoloan
                if self.booktoloan in self.bookdict:
                    return self.booktoloan
                self.booktoloan = input("\nPlease Choose a valid book.\nInput: ")
                return book_checker(self.booktoloan)
            book_checker(self.booktoloan)

            print("\n\nBook ID: " + self.bookdict[self.booktoloan].id + "     Book Name: " + self.bookdict[self.booktoloan].title)
            for bookitem in self.bookitemsperbookdict[self.booktoloan]:
                if bookitem in loanadministration.loanitemdict:
                    print("Book Copy: " + bookitem + "      Status: Loaned")
                else:
                    print("Book Copy: " + bookitem + "      Status: Not Loaned")
    #END searchspecificbook Method
#END Catalog Class
                
#BEGIN LoanAdministration Class
class LoanAdministration:
    def __init__(self):
        self.loanitemdict = {}
        self.customerdict = {}
        self.loanitemsperbookitem = {}
        self.loanitemspercustomer = {}

    #BEGIN showLoaned
    def showloaned(self):
        print("Loaned Book Copies:\n")
        print(self.loanitemdict)
        print("\nLoaned Book Copies per Book:\n")
        print(self.loanitemsperbookitem)
        print("\nLoaned Book Copies per Customer:\n")
        print(self.loanitemspercustomer)
    #END showLoaned
        
    #BEGIN loanbook 
    def loanbook(self, catalog):
        #BEGIN Book Selection
        for bookinfo in catalog.bookdict:
            print("Book ID: " + catalog.bookdict[bookinfo].id + "     Book Name: " +
                  catalog.bookdict[bookinfo].title)
        print("Please type the ID of that book that you want to loan")
        self.booktoloan = input("\nInput: ")

        def book_checker(inp):
            global booktoloan
            if self.booktoloan in catalog.bookdict:
                return self.booktoloan
            self.booktoloan = input("\nPlease Choose a valid book.\nInput: ")
            return book_checker(self.booktoloan)
        book_checker(self.booktoloan)
        #END Book Selection

        #BEGIN Bookitem Selection
        print("\n\nBook ID: " + catalog.bookdict[self.booktoloan].id + "     Book Name: " + catalog.bookdict[self.booktoloan].title)
        for bookitem in catalog.bookitemsperbookdict[self.booktoloan]:
            if bookitem in self.loanitemdict:
                print("Book Copy: " + bookitem + "      Status: Loaned")
            else:
                print("Book Copy: " + bookitem + "      Status: Not Loaned")
        print("\n\nPlease select the book copy that you want to loan")
        print("\nPress '1' if you want to choose a different book.")
        self.booktoloanitem = input("\nInput: ")
        if self.booktoloanitem == '1':
            self.loanbook()
        
        def bookitem_checker(inp):
            global booktoloanitem
            if self.booktoloanitem in self.loanitemdict:
                print("Book is already loaned.Please choose another copy.")
                self.booktoloanitem = input("\nInput: ")
                return bookitem_checker(self.booktoloanitem)
            if self.booktoloanitem in catalog.bookitemsperbookdict[self.booktoloan]:
                return self.booktoloanitem    
            self.booktoloanitem = input("\nPlease Choose a valid book copy.\nInput: ")
            return bookitem_checker(self.booktoloanitem)
        bookitem_checker(self.booktoloanitem)
        #END Bookitem Selection
        
        #BEGIN Username selection
        print("##NOTE##\nA few usernames: Reech1950,Othed1997,Ressoare")
        print("\n\nPlease fill in your username")
        self.username = input("\nUsername: ")
        
        def user_checker(inp):
            global username
            for customer in self.customerdict:
                if self.username in self.customerdict[customer].Username:
                    print("Succes")
                    return self.username
            self.username = input("\nPlease write your username correctly.\nUsername: ")
            return user_checker(self.username)
        user_checker(self.username)
        #END Username selection
        
        #BEGIN Turning username to Real Name
        for customer in self.customerdict:
            if self.username in self.customerdict[customer].Username:
                self.fullname = self.customerdict[customer].GivenName + " " + self.customerdict[customer].Surname
        #END Turning username to real Name
        
        #BEGIN creating object & adding to dictionaries
        temploan = LoanItem(self.booktoloan,self.booktoloanitem,self.fullname)

        self.loanitemdict[temploan.bookitem] = temploan.bookitem
        if temploan.book in self.loanitemsperbookitem:
            self.loanitemsperbookitem[temploan.book].append(temploan.bookitem)
        else:
            self.loanitemsperbookitem[temploan.book] = [temploan.bookitem]

        if temploan.customer in self.loanitemspercustomer:
            self.loanitemspercustomer[temploan.customer].append(temploan.bookitem)
        else:
            self.loanitemspercustomer[temploan.customer] = [temploan.bookitem]
        #BEGIN creating object & adding to dictionaries
    #END loanbook Method
#END LoanAdministration Class

#BEGIN LoanItem Class

class LoanItem:
    def __init__(self, book, bookitem, customer):
        self.book = book
        self.bookitem = bookitem
        self.customer = customer

#END LoanItem Class
                
#BEGIN <<Person>> Class 
class Person:
    def __init__(self):
        self.Gender = input("Gender: ")
        self.NameSet = input("Language: ")
        self.GivenName = input("Firstname: ")
        self.Surname = input("Surname: ")
        self.StreetAddress = input("Street address: ")
        self.ZipCode = input("ZipCode: ")
        self.City = input("City: ")
        self.Email = input("E-mail: ")
        self.Tel = input("Telephone Number: ")

    #Begin addCustomer Method
    def addCustomer(loanadministration):
        Number = len(loanadministration.customerdict) + 1
        tempp = Person()
        new_customerd = {"Number":Number,"Gender":tempp.Gender,"NameSet":tempp.NameSet,
                         "GivenName":tempp.GivenName,"Surname":tempp.Surname,
                         "StreetAddress":tempp.StreetAddress,"ZipCode":tempp.ZipCode,"City":tempp.City,
                         "EmailAddress":tempp.Email,"Username":input("Username: "),"TelephoneNumber":tempp.Tel}
        new_customer = Customer(**new_customerd)
        loanadministration.customerdict[new_customer.id] = new_customer
    #END addCustomer Method
#END <<Person>> Class


#BEGIN Customer Class
class Customer(Person):
    def __init__(self, **attributedict):
        self.id = generateid('C')
        for key in attributedict:
                setattr(self, key, attributedict[key])

#END Customer Class

#BEGIN Librarian Class
class Librarian(Person):
    def __init__(self,lid,username):
        self.librarianID = lid
        self.username = username
#END Librarian Class


