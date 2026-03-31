from connect import get_connection
def main():
    conn = get_connection()
    cur = conn.cursor()
    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Add/Update contact")
        print("2. Search (by name, surname, or phone)")
        print("3. Show paginated (Limit & Offset)")
        print("4. Delete contact")
        print("5. Exit")
        print("6. Bulk Insert (Many users at once)")
        choice = input("Choose: ")
        if choice == "1":
            name = input("Name: ")
            surname = input("Surname: ")
            phone = input("Phone: ")
            cur.execute("CALL upsert_contact(%s, %s, %s)", (name, surname, phone))
            conn.commit()
            print("✅ Success: Contact added or updated.")
        elif choice == "2":
            pattern = input("Search pattern: ")
            cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
            rows = cur.fetchall()
            print("\nResults:")
            for row in rows:
                print(f"Name: {row[0]}, Surname: {row[1]}, Phone: {row[2]}")
        elif choice == "3":
            try:
                limit = int(input("Limit (how many to show): "))
                offset = int(input("Offset (how many to skip): "))
                cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
                rows = cur.fetchall()
                print(f"\nShowing {len(rows)} contacts:")
                for row in rows:
                    print(f"Name: {row[0]}, Surname: {row[1]}, Phone: {row[2]}")
            except ValueError:
                print("❌ Error: Please enter numbers for limit and offset.")
        elif choice == "4":
            value = input("Delete by name/surname/phone: ")
            cur.execute("CALL delete_contact(%s)", (value,))
            conn.commit()
            print(f"✅ Delete command for '{value}' executed.")
        elif choice == "6":
            print("\nEnter data separated by commas (e.g. A, B, C)")
            names_in = input("Names: ").split(",")
            surnames_in = input("Surnames: ").split(",")
            phones_in = input("Phones: ").split(",")
            names = [n.strip() for n in names_in]
            surnames = [s.strip() for s in surnames_in]
            phones = [p.strip() for p in phones_in]
            try:
                cur.execute("CALL insert_many_users(%s, %s, %s)", (names, surnames, phones))
                conn.commit()
                print("✅ Bulk insert processed. Check terminal for validation notices.")
            except Exception as e:
                print(f"❌ Error during bulk insert: {e}")
                conn.rollback()

        elif choice == "5":
            print("Goodbye! ✨")
            break
        else:
            print("❌ Invalid choice, try again.")
    cur.close()
    conn.close()
if __name__ == "__main__":
    main()