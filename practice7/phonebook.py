import csv
from connect import get_connection
def create_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS phonebook (
                    name VARCHAR(50) PRIMARY KEY,
                    phone VARCHAR(20)
                );
            """)
            conn.commit()
    print("✅ Table created")
def insert_from_csv(file_name):
    with get_connection() as conn:
        with conn.cursor() as cur:
            with open(file_name, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    cur.execute("""
                        INSERT INTO phonebook (name, phone)
                        VALUES (%s, %s)
                        ON CONFLICT (name) DO NOTHING
                    """, row)
            conn.commit()
    print("✅ CSV loaded")
def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO phonebook (name, phone)
                VALUES (%s, %s)
                ON CONFLICT (name) DO NOTHING
            """, (name, phone))
            conn.commit()
    print("✅ Contact added")
def update_contact(name, new_name=None, new_phone=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            if new_name:
                cur.execute("UPDATE phonebook SET name=%s WHERE name=%s", (new_name, name))
            if new_phone:
                cur.execute("UPDATE phonebook SET phone=%s WHERE name=%s", (new_phone, name))
            conn.commit()

    print("✅ Updated")
def search_contacts(value):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM phonebook
                WHERE name ILIKE %s OR phone LIKE %s
            """, (f"%{value}%", f"{value}%"))
            rows = cur.fetchall()
            print("🔍 Results:")
            for row in rows:
                print(row)
def delete_contact(value):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM phonebook
                WHERE name=%s OR phone=%s
            """, (value, value))
            conn.commit()
    print("🗑 Deleted")
def menu():
    while True:
        print("\n--- PHONEBOOK ---")
        print("1. Add contact")
        print("2. Load from CSV")
        print("3. Search")
        print("4. Update")
        print("5. Delete")
        print("6. Exit")
        choice = input("Choose: ")
        if choice == "1":
            insert_from_console()
        elif choice == "2":
            insert_from_csv("contacts.csv")
        elif choice == "3":
            val = input("Enter name or phone prefix: ")
            search_contacts(val)
        elif choice == "4":
            name = input("Enter current name: ")
            new_name = input("New name (or press Enter): ")
            new_phone = input("New phone (or press Enter): ")
            update_contact(
                name,
                new_name if new_name else None,
                new_phone if new_phone else None
            )
        elif choice == "5":
            val = input("Enter name or phone to delete: ")
            delete_contact(val)
        elif choice == "6":
            break
        else:
            print("❌ Invalid choice")
if __name__ == "__main__":
    create_table()
    menu()