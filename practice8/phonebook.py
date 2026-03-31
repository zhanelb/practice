from connect import get_connection
conn = get_connection()
cur = conn.cursor()
while True:
    print("\n1. Add/Update contact")
    print("2. Search")
    print("3. Show paginated")
    print("4. Delete")
    print("5. Exit")
    choice = input("Choose: ")
    if choice == "1":
        name = input("Name: ")
        surname = input("Surname: ")
        phone = input("Phone: ")
        cur.execute("CALL upsert_contact(%s, %s, %s)",
                    (name, surname, phone))
        conn.commit()
    elif choice == "2":
        pattern = input("Search: ")
        cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
        for row in cur.fetchall():
            print(row)
    elif choice == "3":
        limit = int(input("Limit: "))
        offset = int(input("Offset: "))
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)",
                    (limit, offset))
        for row in cur.fetchall():
            print(row)
    elif choice == "4":
        value = input("Delete by name/surname/phone: ")
        cur.execute("CALL delete_contact(%s)", (value,))
        conn.commit()
    elif choice == "5":
        break
cur.close()
conn.close()