import json
from connect import connect

conn = connect()
cur = conn.cursor()
#add contact
def add_contact(name, email, birthday):
    cur.execute("""
        INSERT INTO contacts(name, email, birthday)
        VALUES (%s,%s,%s)
    """, (name, email, birthday))
    conn.commit()
#import cvs
def import_csv(conn, filename="contacts.csv"):
    cur = conn.cursor()
    with open(filename, "r", encoding="utf-8") as file:
        next(file)
        for line in file:
            name, email, birthday, group_name, phone, phone_type = line.strip().split(",")

            #group
            cur.execute("SELECT id FROM groups WHERE name=%s", (group_name,))
            group = cur.fetchone()
            if group:
                group_id = group[0]
            else:
                cur.execute(
                    "INSERT INTO groups(name) VALUES(%s) RETURNING id",
                    (group_name,)
                )
                group_id = cur.fetchone()[0]

            #contact
            cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
            contact = cur.fetchone()
            if contact:
                contact_id = contact[0]
            else:
                cur.execute("""
                    INSERT INTO contacts(name, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (name, email, birthday, group_id))
                contact_id = cur.fetchone()[0]
            # phone
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (contact_id, phone, phone_type))
    conn.commit()
    print("CSV import done") #done
#search
def search(query):
    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    for row in cur.fetchall():
        print(row)
#filter 
def filter_group(group):
    cur.execute("""
        SELECT c.name, c.email
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name = %s
    """, (group,))
    for row in cur.fetchall():
        print(row)
#sort
def sort_contacts(by):
    order = {
        "name": "name",
        "birthday": "birthday",
        "id": "id"
    }.get(by, "id")
    cur.execute(f"""
        SELECT name, email, birthday
        FROM contacts
        ORDER BY {order} ASC
    """)
    for row in cur.fetchall():
        print(row)
#pagination
def pagination():
    limit = 5
    offset = 0
    while True:
        cur.execute("""
            SELECT name, email
            FROM contacts
            LIMIT %s OFFSET %s
        """, (limit, offset))

        rows = cur.fetchall()
        print("\nOUR PAGE ")
        for r in rows:
            print(r)
        cmd = input("next / prev / quit: ")
        if cmd == "next":
            offset += limit
        elif cmd == "prev" and offset >= limit:
            offset -= limit
        elif cmd == "quit":
            break
#export json
def export_json():
    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
    """)

    contacts = cur.fetchall()
    data = []

    for c in contacts:
        cur.execute("""
            SELECT phone, type FROM phones
            WHERE contact_id=%s
        """, (c[0],))

        phones = cur.fetchall()

        data.append({
            "name": c[1],
            "email": c[2],
            "birthday": str(c[3]),
            "group": c[4],
            "phones": [{"phone": p[0], "type": p[1]} for p in phones]
        })

    with open("contacts.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("Export done")
#import json
def import_json():
    with open("contacts.json", encoding="utf-8") as f:
        data = json.load(f)

    for c in data:
        cur.execute("SELECT id FROM groups WHERE name=%s", (c["group"],))
        group = cur.fetchone()

        if group:
            group_id = group[0]
        else:
            cur.execute(
                "INSERT INTO groups(name) VALUES(%s) RETURNING id",
                (c["group"],)
            )
            group_id = cur.fetchone()[0]

        # contact check
        cur.execute("SELECT id FROM contacts WHERE name=%s", (c["name"],))
        exists = cur.fetchone()

        if exists:
            choice = input(f"{c['name']} exists (skip/overwrite): ")
            if choice == "skip":
                continue
            cur.execute("DELETE FROM contacts WHERE id=%s", (exists[0],))

        cur.execute("""
            INSERT INTO contacts(name,email,birthday,group_id)
            VALUES (%s,%s,%s,%s)
            RETURNING id
        """, (c["name"], c["email"], c["birthday"], group_id))

        cid = cur.fetchone()[0]

        for p in c["phones"]:
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s,%s,%s)
            """, (cid, p["phone"], p["type"]))

    conn.commit()
    print("Import done")
#menu
def menu():
    while True:
        print("""
1. Search
2. Filter group
3. Sort
4. Pagination
5. Export JSON
6. Import JSON
7. Import CSV
8. Add Contact             
0. Exit
        """)

        choice = input("> ")

        if choice == "1":
            search(input("query: "))
        elif choice == "2":
            filter_group(input("group: "))
        elif choice == "3":
            sort_contacts(input("name/birthday/id: "))
        elif choice == "4":
            pagination()
        elif choice == "5":
            export_json()
        elif choice == "6":
            import_json()
        elif choice == "7":
            import_csv(conn)
        elif choice == "8":
            name = input("name: ")
            email = input("email: ")
            birthday = input("birthday: ")
            add_contact(name, email, birthday)
        elif choice == "0":
            break
menu()