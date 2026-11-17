from db import DatabaseManager

class Menu:
    db = DatabaseManager()
    user_logged = False
    db.update_data()
    def __init__(self):
        self.options =(
            {
            1: "Login",
            2: "Register",
            0: "Exit"
            }, 
            
            {
            1: "Show your portfolio",
            2: "Make transaction",
            3: "List of currencies",
            4: "History of transactions",
            0: "Exit"
            }
            )
            
    def show(self):
        for num,name in self.options[self.user_logged].items():
            print(f"{num}. {name}")
    

    def choice(self):
        while True:
            try:
                choice = int(input("\nSelect option: "))
                print()
                if choice in self.options[self.user_logged]:
                    return choice
                print("Invalid option. Try again.")

            except ValueError:
                print("Integer excpected. Try again. ")
                
    def option1(self):
        while True:
            print("Login menu")
            self.show()
            choice = self.choice()
            match choice:
                case 1:
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    current_user = self.db.login(username,password)
                case 2: 
                    username = input("Enter username: ")    
                    password = input("Enter password: ")                    
                    self.db.register(username,password)
                    current_user = self.db.login(username,password)
                case 0:
                    print("Bye")
                    return False
                
            if current_user:
                self.user_logged = True
                return current_user
            else:
                continue

    def option2(self,current_user):
        while True:
            print("Menu")
            self.show()
            choice = self.choice()
            match choice:
                case 1:
                    self.db.show_portfolio(current_user)
                case 2:
                    self.db.make_transaction(current_user)
                case 3:
                    self.db.show_currencies()
                case 4:
                    self.db.show_transactions(current_user)
                case 0:
                    print(f"Bye {current_user}!")
                    self.user_logged = False
                    break
            input()
            