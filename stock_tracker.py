"""
Stock Portfolio Tracker
========================
Goal: Calculate total investment based on manually defined stock prices.
Key Concepts: dictionary, input/output, basic arithmetic, file handling
"""

import csv
import os
from datetime import datetime

# ── Hardcoded stock price dictionary (USD) ────────────────────────────────────
STOCK_PRICES = {
    "AAPL":  180,   # Apple Inc.
    "TSLA":  250,   # Tesla Inc.
    "GOOGL": 140,   # Alphabet Inc.
    "MSFT":  380,   # Microsoft Corp.
    "AMZN":  185,   # Amazon.com Inc.
    "NVDA":  875,   # NVIDIA Corp.
    "META":  500,   # Meta Platforms
    "NFLX":  630,   # Netflix Inc.
}

# ── Helper utilities ──────────────────────────────────────────────────────────

def display_available_stocks():
    """Print all available stocks and their prices."""
    print("\n" + "=" * 45)
    print(f"  {'TICKER':<8} {'COMPANY / PRICE':>30}")
    print("=" * 45)
    labels = {
        "AAPL": "Apple Inc.",
        "TSLA": "Tesla Inc.",
        "GOOGL": "Alphabet Inc.",
        "MSFT": "Microsoft Corp.",
        "AMZN": "Amazon.com Inc.",
        "NVDA": "NVIDIA Corp.",
        "META": "Meta Platforms",
        "NFLX": "Netflix Inc.",
    }
    for ticker, price in STOCK_PRICES.items():
        name = labels.get(ticker, "")
        print(f"  {ticker:<8} {name:<22} ${price:>6}")
    print("=" * 45)


def get_portfolio_from_user():
    """
    Interactively ask the user for stock tickers and quantities.
    Returns a dict  {ticker: quantity}.
    """
    portfolio = {}
    print("\nEnter your stock holdings.")
    print("Type the ticker symbol and the quantity (e.g.  AAPL 10).")
    print("Press ENTER with no input when you are done.\n")

    while True:
        raw = input("  Stock (ticker qty) : ").strip().upper()
        if not raw:
            break

        parts = raw.split()
        if len(parts) != 2:
            print("  ⚠  Please enter exactly two values: TICKER QUANTITY")
            continue

        ticker, qty_str = parts
        if ticker not in STOCK_PRICES:
            print(f"  ⚠  '{ticker}' is not in our price list. Available: {', '.join(STOCK_PRICES)}")
            continue

        try:
            qty = int(qty_str)
            if qty <= 0:
                raise ValueError
        except ValueError:
            print("  ⚠  Quantity must be a positive whole number.")
            continue

        if ticker in portfolio:
            portfolio[ticker] += qty
            print(f"  ✔  Updated {ticker}: total {portfolio[ticker]} shares.")
        else:
            portfolio[ticker] = qty
            print(f"  ✔  Added {ticker} × {qty}.")

    return portfolio


def calculate_portfolio(portfolio):
    """
    Given {ticker: qty}, return a list of result rows and grand total.
    Each row: (ticker, qty, price_per_share, total_value)
    """
    rows = []
    grand_total = 0.0
    for ticker, qty in portfolio.items():
        price = STOCK_PRICES[ticker]
        value = price * qty
        grand_total += value
        rows.append((ticker, qty, price, value))
    return rows, grand_total


def display_results(rows, grand_total):
    """Pretty-print the portfolio summary."""
    print("\n" + "=" * 55)
    print("           📊  PORTFOLIO SUMMARY")
    print("=" * 55)
    print(f"  {'TICKER':<8} {'QTY':>6}  {'PRICE':>10}  {'VALUE':>12}")
    print("-" * 55)
    for ticker, qty, price, value in rows:
        print(f"  {ticker:<8} {qty:>6}  ${price:>9,}  ${value:>11,}")
    print("-" * 55)
    print(f"  {'TOTAL PORTFOLIO VALUE':.<38} ${grand_total:>11,.2f}")
    print("=" * 55)


# ── File saving ───────────────────────────────────────────────────────────────

def save_as_txt(rows, grand_total, filename="portfolio_result.txt"):
    """Save the portfolio summary to a plain-text file."""
    path = os.path.join(os.path.dirname(__file__), filename)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(path, "w", encoding="utf-8") as f:
        f.write("STOCK PORTFOLIO TRACKER — RESULT\n")
        f.write(f"Generated : {timestamp}\n")
        f.write("=" * 55 + "\n")
        f.write(f"  {'TICKER':<8} {'QTY':>6}  {'PRICE':>10}  {'VALUE':>12}\n")
        f.write("-" * 55 + "\n")
        for ticker, qty, price, value in rows:
            f.write(f"  {ticker:<8} {qty:>6}  ${price:>9,}  ${value:>11,}\n")
        f.write("-" * 55 + "\n")
        f.write(f"  TOTAL PORTFOLIO VALUE : ${grand_total:>,.2f}\n")
        f.write("=" * 55 + "\n")
    print(f"\n  ✅  Saved as TXT → {path}")


def save_as_csv(rows, grand_total, filename="portfolio_result.csv"):
    """Save the portfolio summary to a CSV file."""
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Ticker", "Quantity", "Price (USD)", "Total Value (USD)"])
        for ticker, qty, price, value in rows:
            writer.writerow([ticker, qty, price, value])
        writer.writerow([])
        writer.writerow(["", "", "GRAND TOTAL", grand_total])
    print(f"  ✅  Saved as CSV → {path}")


# ── Main program ──────────────────────────────────────────────────────────────

def main():
    print("\n" + "🌟 " * 15)
    print("       STOCK PORTFOLIO TRACKER")
    print("🌟 " * 15)

    # 1. Show available stocks
    display_available_stocks()

    # 2. Collect user input
    portfolio = get_portfolio_from_user()

    if not portfolio:
        print("\n  ℹ  No stocks entered. Exiting.")
        return

    # 3. Calculate values
    rows, grand_total = calculate_portfolio(portfolio)

    # 4. Display results
    display_results(rows, grand_total)

    # 5. Optionally save
    print("\nWould you like to save the results?")
    print("  [1] Save as TXT")
    print("  [2] Save as CSV")
    print("  [3] Save as both TXT and CSV")
    print("  [4] No, skip saving")

    choice = input("\n  Your choice (1/2/3/4) : ").strip()

    if choice == "1":
        save_as_txt(rows, grand_total)
    elif choice == "2":
        save_as_csv(rows, grand_total)
    elif choice == "3":
        save_as_txt(rows, grand_total)
        save_as_csv(rows, grand_total)
    else:
        print("\n  ℹ  Results not saved.")

    print("\n  Thanks for using Stock Portfolio Tracker! 🚀\n")


if __name__ == "__main__":
    main()
