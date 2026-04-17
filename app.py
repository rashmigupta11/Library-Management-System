import streamlit as st
import sqlite3
from datetime import date, timedelta


# ---------- DATABASE ----------
def run_query(query, params=()):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    data = cursor.fetchall()
    conn.close()
    return data


# ---------- LOGIN ----------
def login():
    st.title("Library Management System")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "" or password == "":
            st.error("Enter both fields")
        else:
            user = run_query(
                "SELECT * FROM users WHERE username=? AND password=?",
                (username, password)
            )
            if len(user) > 0:
                st.session_state.logged_in = True
                st.session_state.role = user[0][3]
                st.session_state.page = "Home"
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid login")


# ---------- HOME ----------
def home():
    st.title("Home")

    if st.session_state.role == "admin":
        page = st.selectbox("Select Page", ["Home", "Flow Chart", "Transactions", "Reports", "Maintenance"])
    else:
        page = st.selectbox("Select Page", ["Home", "Flow Chart", "Transactions", "Reports"])

    st.session_state.page = page

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()


# ---------- FLOW CHART ----------
def flow_chart():
    st.title("Application Flow")

    st.write("1. Login")
    st.write("↓")
    st.write("2. Home Page")
    st.write("↓")
    st.write("3. Select Module")

    st.write("---")

    st.write("Transactions:")
    st.write("- Search Book")
    st.write("- Issue Book")
    st.write("- Return Book")
    st.write("- Pay Fine")

    st.write("---")

    st.write("Reports:")
    st.write("- Books")
    st.write("- Members")
    st.write("- Active Issues")

    st.write("---")

    st.write("Maintenance (Admin only):")
    st.write("- Add Book")
    st.write("- Update Book")
    st.write("- Add Member")
    st.write("- Update Member")
    st.write("- Add User")


# ---------- TRANSACTIONS ----------
def transactions():
    st.title("Transactions")

    option = st.selectbox("Choose", ["Search Book", "Issue Book", "Return Book", "Pay Fine"])

    # SEARCH
    if option == "Search Book":
        name = st.text_input("Book Name")

        if st.button("Search"):
            data = run_query(
                "SELECT title, author, available FROM books WHERE title LIKE ?",
                ("%" + name + "%",)
            )

            if len(data) == 0:
                st.write("No books found")
            else:
                for d in data:
                    status = "Available" if d[2] == 1 else "Not Available"
                    st.write(d[0], "-", d[1], "-", status)

    # ISSUE
    elif option == "Issue Book":
        books = run_query("SELECT id, title FROM books WHERE available=1")
        members = run_query("SELECT id, name FROM members")

        if len(books) == 0 or len(members) == 0:
            st.write("No data available")
        else:
            b = {x[1]: x[0] for x in books}
            m = {x[1]: x[0] for x in members}

            book = st.selectbox("Book", list(b.keys()))
            member = st.selectbox("Member", list(m.keys()))

            if st.button("Issue"):
                issue_date = date.today()
                return_date = issue_date + timedelta(days=7)

                run_query(
                    "INSERT INTO issues (member_id, book_id, issue_date, return_date) VALUES (?,?,?,?)",
                    (m[member], b[book], str(issue_date), str(return_date))
                )

                run_query("UPDATE books SET available=0 WHERE id=?", (b[book],))

                st.write("Book Issued")

    # RETURN
    elif option == "Return Book":
        data = run_query("""
            SELECT issues.id, books.title, issues.return_date, books.id
            FROM issues
            JOIN books ON issues.book_id = books.id
        """)

        if len(data) == 0:
            st.write("No issued books")
        else:
            d = {x[1]: x for x in data}
            sel = st.selectbox("Select Book", list(d.keys()))
            rec = d[sel]

            if st.button("Return"):
                issue_id = rec[0]
                due = date.fromisoformat(rec[2])
                book_id = rec[3]

                today = date.today()
                fine = 0

                if today > due:
                    fine = (today - due).days

                run_query("UPDATE books SET available=1 WHERE id=?", (book_id,))

                if fine > 0:
                    run_query(
                        "INSERT INTO fines (issue_id, amount, paid) VALUES (?,?,0)",
                        (issue_id, fine)
                    )
                    st.write("Returned with fine:", fine)
                else:
                    st.write("Returned")

    # PAY FINE
    elif option == "Pay Fine":
        fines = run_query("SELECT id, amount FROM fines WHERE paid=0")

        if len(fines) == 0:
            st.write("No pending fines")
        else:
            f = {f"{x[0]} - {x[1]}": x[0] for x in fines}
            sel = st.selectbox("Select Fine", list(f.keys()))

            if st.button("Pay"):
                run_query("UPDATE fines SET paid=1 WHERE id=?", (f[sel],))
                st.write("Fine Paid")


# ---------- REPORTS ----------
def reports():
    st.title("Reports")

    option = st.selectbox("Choose", ["Books", "Members", "Active Issues"])

    if option == "Books":
        data = run_query("SELECT * FROM books")
        for d in data:
            st.write(d)

    elif option == "Members":
        data = run_query("SELECT * FROM members")
        for d in data:
            st.write(d)

    elif option == "Active Issues":
        data = run_query("SELECT * FROM issues")
        for d in data:
            st.write(d)


# ---------- MAINTENANCE ----------
def maintenance():
    st.title("Maintenance")

    option = st.selectbox(
        "Choose",
        ["Add Book", "Update Book", "Add Member", "Update Member", "Add User"]
    )

    # ADD BOOK
    if option == "Add Book":
        name = st.text_input("Book Name")
        author = st.text_input("Author")

        if st.button("Add"):
            run_query(
                "INSERT INTO books (title, author, available) VALUES (?,?,1)",
                (name, author)
            )
            st.write("Book Added")

    # UPDATE BOOK
    elif option == "Update Book":
        books = run_query("SELECT id, title FROM books")
        b = {x[1]: x[0] for x in books}

        sel = st.selectbox("Book", list(b.keys()))
        new_name = st.text_input("New Name")

        if st.button("Update"):
            run_query("UPDATE books SET title=? WHERE id=?", (new_name, b[sel]))
            st.write("Updated")

    # ADD MEMBER
    elif option == "Add Member":
        name = st.text_input("Name")

        if st.button("Add"):
            run_query(
                "INSERT INTO members (name, email, phone) VALUES (?,?,?)",
                (name, "", "")
            )
            st.write("Member Added")

    # UPDATE MEMBER
    elif option == "Update Member":
        members = run_query("SELECT id, name FROM members")
        m = {x[1]: x[0] for x in members}

        sel = st.selectbox("Member", list(m.keys()))
        new_name = st.text_input("New Name")

        if st.button("Update"):
            run_query("UPDATE members SET name=? WHERE id=?", (new_name, m[sel]))
            st.write("Updated")

    # ADD USER
    elif option == "Add User":
        username = st.text_input("Username")
        password = st.text_input("Password")
        role = st.selectbox("Role", ["admin", "user"])

        if st.button("Add"):
            run_query(
                "INSERT INTO users (username, password, role) VALUES (?,?,?)",
                (username, password, role)
            )
            st.write("User Added")


# ---------- SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.page = "Home"


# ---------- MAIN ----------
if not st.session_state.logged_in:
    login()
else:
    home()

    if st.session_state.page == "Flow Chart":
        flow_chart()

    elif st.session_state.page == "Transactions":
        transactions()

    elif st.session_state.page == "Reports":
        reports()

    elif st.session_state.page == "Maintenance":
        if st.session_state.role == "admin":
            maintenance()
        else:
            st.write("Access Denied")