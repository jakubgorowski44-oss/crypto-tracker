# Crypto Tracker CLI 🪙

A terminal-based cryptocurrency portfolio tracker and trading simulator written in Python. The application fetches live market prices via the CoinMarketCap API, stores historical and user data in a local SQLite database, and allows users to manage accounts and simulate buy/sell transactions.

> **Status:** 🚧 *Work in Progress — actively developed as part of my Computer Science studies and portfolio.*

---

## ✨ Features

* **User Authentication:** Account registration and login system with SHA-256 password hashing.
* **Live Market Data:** Fetches top 100 cryptocurrencies converted to PLN using the CoinMarketCap Pro API.
* **Resilient API Client:** Built-in `@retry` decorator handling network timeouts and transient HTTP errors.
* **Portfolio & Transactions:** Buy and sell cryptocurrencies, view current wallet valuation, and track transaction history.
* **Interactive Search:** Filter and search available cryptocurrencies by name or ticker symbol directly in the terminal.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Database:** SQLite3
* **Libraries:** `requests`, `python-dotenv`
* **External API:** CoinMarketCap API

---

## 🚀 Getting Started

1. Clone the repository
Bash
git clone [https://github.com/jakubgorowski44-oss/crypto-tracker.git](https://github.com/jakubgorowski44-oss/crypto-tracker.git)
cd crypto-tracker

2. Create and activate a virtual environment
Bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

3. Install dependencies
Bash
pip install -r requirements.txt

4. Configure environment variables
Copy the example environment file and add your free API key from CoinMarketCap:
Bash
cp .env.example .env
Edit .env:
API_KEY=your_api_key_here

5. Run the application
Bash
python main.py