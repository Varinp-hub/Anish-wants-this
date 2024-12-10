
import sqlite3

# Database setup
db = sqlite3.connect("mcdonalds_analytics.db")
cursor = db.cursor()

# Create tables
cursor.executescript("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    registration_date TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS menu_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
);
""")

print("Database and tables are ready.")

# Input functions
def add_customer():
    name = input("Enter customer name: ")
    email = input("Enter customer email: ")
    registration_date = input("Enter registration date (YYYY-MM-DD): ")
    try:
        cursor.execute("INSERT INTO customers (name, email, registration_date) VALUES (?, ?, ?)", 
                       (name, email, registration_date))
        db.commit()
        print("Customer added successfully.")
    except sqlite3.IntegrityError:
        print("Error: Email already exists.")

def add_menu_item():
    item_name = input("Enter menu item name: ")
    category = input("Enter menu item category: ")
    price = float(input("Enter menu item price: "))
    cursor.execute("INSERT INTO menu_items (item_name, category, price) VALUES (?, ?, ?)", 
                   (item_name, category, price))
    db.commit()
    print("Menu item added successfully.")

def add_order():
    customer_id = int(input("Enter customer ID: "))
    item_id = int(input("Enter menu item ID: "))
    order_date = input("Enter order date and time (YYYY-MM-DD HH:MM:SS): ")
    cursor.execute("INSERT INTO orders (customer_id, item_id, order_date) VALUES (?, ?, ?)", 
                   (customer_id, item_id, order_date))
    db.commit()
    print("Order added successfully.")

# Analytics queries
def top_menu_items():
    cursor.execute("""
    SELECT menu_items.item_name, COUNT(*) AS order_count
    FROM orders
    JOIN menu_items ON orders.item_id = menu_items.item_id
    GROUP BY menu_items.item_name
    ORDER BY order_count DESC
    LIMIT 5;
    """)
    print("Top 5 Menu Items:")
    for row in cursor.fetchall():
        print(f"{row[0]} - {row[1]} orders")

def avg_orders_per_customer():
    cursor.execute("""
    SELECT AVG(order_count) AS avg_orders
    FROM (
        SELECT customer_id, COUNT(*) AS order_count
        FROM orders
        GROUP BY customer_id
    ) AS customer_orders;
    """)
    avg_orders = cursor.fetchone()[0]
    print(f"Average orders per customer: {avg_orders:.2f}")

def orders_by_category():
    cursor.execute("""
    SELECT menu_items.category, COUNT(*) AS order_count
    FROM orders
    JOIN menu_items ON orders.item_id = menu_items.item_id
    GROUP BY menu_items.category
    ORDER BY order_count DESC;
    """)
    print("Orders by Category:")
    for row in cursor.fetchall():
        print(f"{row[0]} - {row[1]} orders")

def peak_ordering_times():
    cursor.execute("""
    SELECT strftime('%H', order_date) AS hour, COUNT(*) AS order_count
    FROM orders
    GROUP BY hour
    ORDER BY order_count DESC;
    """)
    print("Peak Ordering Times:")
    for row in cursor.fetchall():
        print(f"{row[0]}:00 - {row[1]} orders")

# Main menu
def main_menu():
    while True:
        print("""
        === McDonald's Customer Analytics ===
        1. Add Customer
        2. Add Menu Item
        3. Add Order
        4. Top Menu Items
        5. Average Orders Per Customer
        6. Orders by Category
        7. Peak Ordering Times
        8. Exit
        """)
        choice = input("Enter your choice: ")
        if choice == '1':
            add_customer()
        elif choice == '2':
            add_menu_item()
        elif choice == '3':
            add_order()
        elif choice == '4':
            top_menu_items()
        elif choice == '5':
            avg_orders_per_customer()
        elif choice == '6':
            orders_by_category()
        elif choice == '7':
            peak_ordering_times()
        elif choice == '8':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

# Start the program
if __name__ == "__main__":
    main_menu()
    db.close()
