from menu import Menu 

def main():
    
    menu = Menu()
    while True:
        current_user = menu.option1()
        if current_user:
            print(current_user[0])
            menu.option2(current_user[0])
        else:
            break

if __name__ == "__main__":
    main()