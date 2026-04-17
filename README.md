#  Library Management System (Streamlit + SQLite)

##  Project Overview

This is a simple Library Management System built using **Python, Streamlit, and SQLite**.

The application allows users to:

* Search books
* Issue books
* Return books
* Pay fines
* View reports
* Admin can manage books, members, and users

---

##  Technologies Used

* Python
* Streamlit (UI)
* SQLite (Database)

---

##  Demo Login Credentials

This project uses predefined users for demonstration purposes.

**Admin Access**
- Username: adm
- Password: adm

**User Access**
- Username: user
- Password: user

> Note: In a real-world application, authentication would be implemented using secure password hashing and user registration.
---

##  How to Run the Project

### Step 1: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the application

```bash
streamlit run app.py
```

---

##  Features

### 1. Authentication

* Login system with roles (Admin/User)

### 2. Transactions

* Search Book
* Issue Book
* Return Book
* Pay Fine

### 3. Reports

* Books List
* Members List
* Active Issues

### 4. Maintenance (Admin Only)

* Add / Update Books
* Add / Update Members
* Add Users

---

##  Database

* SQLite database (`library.db`)
* Tables:

  * users
  * members
  * books
  * issues
  * fines


---


