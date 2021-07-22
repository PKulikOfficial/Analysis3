#PLS main source file
import PLSclasses

#BEGIN Menu's
def startMenu():
    print("Welcome to the Public library system.\n\nPress '1': Create Backup\nPress '2': Restore Backup\nPress '3': Continue as customer\nPress '4': Continue as librarian\nPress '5': Exit\n")

    #BEGIN User Input & Check
    case = input("Input: ")
    intcase = 0
    if (case.isdigit()):
        intcase = int(case)
    
    if intcase == 1:
        print(5*"\n" + "Backup created at /backup/...")
        pub.makeBackup()
        print(5*"\n")
        return startMenu()
    elif intcase == 2:
        print(5*"\n" + "Backup restored from /backup/...")
        pub.restoreBackup()
        print(5*"\n")
        return startMenu()
    elif intcase == 3:
        print(5*"\n")
        return customerMenu()
    elif intcase == 4:
        print(5*"\n")
        return librarianMenu("1")
    elif intcase == 5:
        quit
    else:
        print("\n WRONG INPUT!" + 5*"\n")
        return startMenu()
    #END User Input & Check


def customerMenu():
    print("Customer Menu\n\nPress '1': Browse Catalog\nPress '2': Loan Book\nPress '3': Back\n")
    
    #BEGIN User Input & Check
    case = input("Input: ")
    intcase = 0
    if (case.isdigit()):
        intcase = int(case)
    
    if intcase == 1:
        print(5*"\n")
        pub.catalog.searchSpecificBook(pub.loanadministration)
        print(5*"\n")
        return customerMenu()
    elif intcase == 2:
        print(5*"\n")
        pub.loanadministration.loanbook(pub.catalog)
        print(5*"\n")
        return customerMenu()
    elif intcase == 3:
        print(5*"\n")
        return startMenu()
    else:
        print("\n WRONG INPUT!" + 5*"\n")
        return customerMenu()
    #END User Input & Check

def librarianMenu(login):
    
    if login == "1":
        login = input("\n\n##NOTE##\n login = librarian1\n\nPlease login: ")

        while login != librarian.username:
            login = input("\n\n##ERROR & NOTE##\n login = librarian1\n\nPlease login: ")
        print("\n\nLibrarian Menu\n\nPress '1' Browse Catalog\nPress '2': Add Customer\nPress '3': Add Book\nPress '4': See Loan Administration\nPress '5': Back")
    else:
        print("\n\nLibrarian Menu\n\nPress '1' Browse Catalog\nPress '2': Add Customer\nPress '3': Add Book\nPress '4': See Loan Administration\nPress '5': Back")
    
    #BEGIN User Input & Check
    case = input("Input: ")
    intcase = 0
    if (case.isdigit()):
        intcase = int(case)
    
    if intcase == 1:
        print(5*"\n")
        pub.catalog.searchSpecificBook(pub.loanadministration)
        print(5*"\n")
        return librarianMenu("librarian1")
    elif intcase == 2:
        print(5*"\n")
        PLSclasses.Person.addCustomer(pub.loanadministration)
        print(5*"\n")
        return librarianMenu("librarian1")
    elif intcase == 3:
        print(5*"\n")
        pub.catalog.newBookItem()
        print(5*"\n")
        return librarianMenu("librarian1")
    elif intcase == 4:
        print(5*"\n")
        pub.loanadministration.showloaned()
        print(5*"\n")
        return librarianMenu("librarian1")
    elif intcase == 5:
        print(5*"\n")
        return startMenu()
    else:
        print("\n WRONG INPUT!" + 5*"\n")
        return librarianMenu("librarian1")
    #END User Input & Check
#END Menu's

#BEGIN Initializing Program
librarian = PLSclasses.Librarian("1","librarian1")
pub = PLSclasses.PublicLibrary()

pub.startProgram(open('CurrentBookset.json', 'r',encoding = 'UTF-8'), open('CurrentCustomers.csv', 'r',encoding = 'UTF-8'))

startMenu()
#END Initializing Program


    
        


                    
