from api import ApiClient
import sqlite3
import hashlib


class DatabaseManager:

    def __init__(self, db=sqlite3.connect("crypto_tracker.db")):
        self.db = db
        self.cursor = db.cursor()

    def update_data(self):

        self.cursor.execute("""

            CREATE TABLE IF NOT EXISTS users

            (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                username TEXT UNIQUE NOT NULL,

                password_hash TEXT NOT NULL,
                
                balance REAL

            )

            """)

        self.cursor.execute("""



            CREATE TABLE IF NOT EXISTS currencies

            (

                id INTEGER PRIMARY KEY AUTOINCREMENT, 

                name TEXT, 

                symbol TEXT UNIQUE, 

                price REAL

            )

            """)

        self.cursor.execute("""

            CREATE TABLE IF NOT EXISTS transactions 

            (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                date TEXT DEFAULT (datetime('now', 'localtime')),

                currency_id INTEGER,

                current_price REAL,

                user_id INTEGER,

                amount REAL,
                
                FOREIGN KEY (user_id) REFERENCES users(id)

                FOREIGN KEY (currency_id) REFERENCES currencies(id)

            )

        """)

        self.db.commit()

        api = ApiClient()
        currencies = api.get_data()
        for curency in currencies["data"]:
            self.cursor.execute(
                "INSERT INTO currencies(name,symbol,price) VALUES(?,?,?) ON CONFLICT(symbol) DO UPDATE SET name = excluded.name, price = excluded.price",
                (curency["name"], curency["symbol"], curency["quote"]["PLN"]["price"]),
            )
            self.db.commit()
        print("Database is up to date.")

    def show_currencies(self):
        self.cursor.execute("SELECT name,symbol,price FROM currencies")
        rows = self.cursor.fetchall()
        for x, (name, symbol, price) in enumerate(rows):
            print(f"{x+1}. {name} | {symbol} | {price:.2f} PLN")
        while True:

            phrase = input("Enter phrase to search (enter to quit): ")
            if phrase:
                self.cursor.execute(
                    "SELECT name, symbol, price FROM currencies WHERE LOWER(name) LIKE LOWER(?) OR LOWER(symbol) like LOWER(?)",
                    (f"%{phrase}%", f"%{phrase}%"),
                )

                for x, (name, symbol, price) in enumerate(self.cursor.fetchall()):

                    print(f"{x+1}. {name} | {symbol} | {price:2f} PLN")
            else:
                break

    def make_transaction(self, current_user):
        while True:
            choice = input("Buy (b) / Sell (s): ").lower()
            match choice:
                case "b":
                    self.buy_currency(current_user)
                    break
                case "s":
                    self.sell_currency(current_user)
                    break
                case _:
                    print("That's not an option")
                    continue

    def buy_currency(self, current_user):
        symbol = input(
            "Enter currency symbol to buy(left empty for currency list): "
        ).strip()

        while symbol == "":
            self.show_currencies()
            symbol = input(
                "Enter currency symbol to buy(left empty for currency list): "
            ).strip()

        self.cursor.execute(
            "SELECT id, name, symbol, price FROM currencies WHERE symbol = ? COLLATE NOCASE",
            (symbol,),
        )

        currency = self.cursor.fetchone()

        if currency is None:
            print("Currency not found.")
            return

        curr_id = currency[0]
        curr_name = currency[1]
        curr_symbol = currency[2]
        curr_price = currency[3]
        print(f"{curr_name} | {curr_symbol} | {curr_price:.2f} PLN")

        try:
            amount = float(input("Enter amount to buy: "))
        except ValueError:
            print("Wrong value")
            return

        print(f"Your'e gonna buy {(amount*curr_price):.2f} worth of {curr_name}")
        while True:
            try:
                validate = (input("Accept? (y/n)")).lower()
                if validate == "y":
                    break
                elif validate == "n":
                    print("\nAborted")
                    return
                else:
                    continue
            except ValueError:
                pass

        self.cursor.execute(
            """
                INSERT INTO transactions
                (currency_id, current_price, user_id, amount)
                VALUES (?, ?, ?, ?)
            """,
            (
                curr_id,
                curr_price,
                self.get_user_id(current_user),
                amount,
            ),
        )

        self.db.commit()

    def sell_currency(self, current_user):
        self.show_portfolio(current_user)
        symbol = input("Enter currency symbol to sell: ").strip()

        self.cursor.execute(
            "SELECT id, name, symbol, price FROM currencies WHERE symbol = ? COLLATE NOCASE",
            (symbol,),
        )

        currency = self.cursor.fetchone()

        if currency is None:
            print("Currency not found.")
            return

        curr_id = currency[0]
        curr_name = currency[1]
        curr_symbol = currency[2]
        curr_price = currency[3]
        print(f"{curr_name} | {curr_symbol} | {curr_price:.2f} PLN")

        self.cursor.execute(
            "SELECT c.name, SUM(t.amount) AS amount FROM transactions AS t JOIN currencies as c ON t.currency_id = c.id JOIN users as u ON t.user_id = u.id WHERE c.symbol = ? COLLATE NOCASE AND t.user_id = ? GROUP BY name",
            (
                symbol,
                self.get_user_id(current_user),
            ),
        )

        check = self.cursor.fetchone()[1]
        print(check)

        try:
            amount = float(input("Enter amount to sell: "))
            if amount > check:
                print("Not enough resources to sell")
                return
            if amount < 0:
                print("You must enter positive number")
                return
            if amount == 0:
                return
        except ValueError:
            print("Wrong value")
            return

        amount = -amount

        print(f"Your'e gonna sell {(amount*curr_price):.2f} worth of {curr_name}")
        while True:
            try:
                validate = (input("Accept? (y/n)")).lower()
                if validate == "y":
                    break
                elif validate == "n":
                    print("\nAborted")
                    return
                else:
                    continue
            except ValueError:
                pass

        self.cursor.execute(
            """
            INSERT INTO transactions
            (currency_id, current_price, user_id,  amount)
            VALUES (?, ?, ?, ?)
        """,
            (curr_id, curr_price, self.get_user_id(current_user), amount),
        )

        self.db.commit()

    def show_portfolio(self, current_user):
        print(f"{current_user}'s wallet")
        self.cursor.execute(
            "SELECT c.name, c.symbol, SUM(t.amount), (c.price * SUM(t.amount)) as value FROM transactions AS t JOIN currencies as c ON t.currency_id = c.id JOIN users as u ON t.user_id = u.id WHERE user_id = ? GROUP BY name",
            (self.get_user_id(current_user),),
        )

        rows = self.cursor.fetchall()
        x = 1
        for name, symbol, amount, value in rows:
            if amount == 0:
                pass

            else:
                print(f"{x}. {name} | {symbol} | {amount} | {value:.2f} PLN")
                x += 1

    def show_transactions(self, current_user):
        print(f"{current_user}'s transactions")

        self.cursor.execute(
            "SELECT t. date, c.name, c.symbol, t.current_price, t.amount, (t.current_price * t.amount) as value FROM transactions AS t JOIN currencies as c ON t.currency_id = c.id JOIN users as u ON t.user_id = u.id WHERE user_id = ?",
            (self.get_user_id(current_user),),
        )

        rows = self.cursor.fetchall()

        for x, (date, name, symbol, price, amount, value) in enumerate(rows):

            print(
                f"{x+1}.{date} | {name} | {symbol} | {price:.2f} PLN | {amount} | {value:.2f} PLN"
            )
        else:
            return

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password):

        try:
            self.cursor.execute(
                """
                        INSERT INTO users (username, password_hash)
                        VALUES (?, ?)
                        """,
                (username, self.hash_password(password)),
            )
            self.db.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def login(self, username, password):

        user = self.cursor.execute(
            """
                        SELECT username FROM users WHERE username = ? AND password_hash = ?
                        """,
            (username, self.hash_password(password)),
        ).fetchone()
        return user

    def get_user_id(self, current_user):

        users_id = self.cursor.execute(
            """

                            SELECT * FROM users WHERE username = ?

                        """,
            (current_user,),
        ).fetchone()[0]

        return users_id
