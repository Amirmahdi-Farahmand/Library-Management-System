# 📚 Library Management System

A **Python-based Library Management System** that uses **Linked Lists** for books, **Stacks** for operation history, and supports **user accounts** and **admin management**.  
Users can borrow and return books, while admins can add/edit/remove books and view system logs.  

---

## 🛠 Features

### For Users
- Create a new account with username and password.
- Login and manage account.
- Search for books by **name** or **author**.
- Borrow available books (checks duplicates).
- Return borrowed books.
- View all available books.
- View account information (borrowed books, password masked).

### For Admin
- Admin login (`username: admin`, `password: admin`).
- Search books.
- Edit book copies (add/remove/set to 0).
- Add or remove books.
- View all borrowed books by users.
- View **last 20 operations** (stack-based history).
- View all books in **Linked List structure** with statistics.

### Data Structures
- **Linked List**: Stores books for easy traversal and recursive operations.
- **Stack**: Maintains recent operations (max 20 entries).
- **CSV file**: Stores user account info (`acount_info.csv`).
- **JSON file**: Stores books data (`books.json`).
- **TXT file**: Optional initial books file (`books.txt`).

---

## 🗂 File Structure

library_system/
├── books.json # JSON database of books
├── books.txt # Optional initial books list
├── acount_info.csv # User accounts info
├── library.py # Main library management code
└── README.md # Project documentation


---

## ⚙️ Installation

1. Make sure **Python 3.8+** is installed.
2. Clone or download the repository.
3. Optional: Create virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows


