# ============ imports ============
import os
import json


# ============== Linked List for Books =============
class BookNode:
    """Node for book linked list"""
    def __init__(self, book_data):
        self.book_data = book_data
        self.next = None


class BookLinkedList:
    """Linked list for managing books"""
    def __init__(self):
        self.head = None
        self.size = 0
    
    def add_book(self, book_data):
        """Add book to linked list"""
        new_node = BookNode(book_data)
        
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        
        self.size += 1
    
    def find_all_books_recursive(self, current_node, keyword, results=None):
        """Recursive function to search for ALL books matching keyword"""
        if results is None:
            results = []
        
        if current_node is None:
            return results
        
        book = current_node.book_data
        if (keyword.lower() in book['name'].lower() or 
            keyword.lower() in book['author'].lower()):
            results.append(current_node)
        
        return self.find_all_books_recursive(current_node.next, keyword, results)
    
    def display_all_recursive(self, current_node, count=1):
        """Recursive function to display all books"""
        if current_node is None:
            return
        
        book = current_node.book_data
        status = "Available" if book['available_copies'] > 0 else "Borrowed"
        print(f"{count}. {book['name']} - {book['author']} ({book['year']}) - {status}")
        
        self.display_all_recursive(current_node.next, count + 1)
    
    def count_available_recursive(self):
        """Count available books recursively"""
        def _helper(node):
            if node is None:
                return 0
            count = 1 if node.book_data['available_copies'] > 0 else 0
            return count + _helper(node.next)
        
        return _helper(self.head)
    
    def traverse(self):
        """Traverse linked list to get all books"""
        books_list = []
        current = self.head
        while current:
            books_list.append(current.book_data)
            current = current.next
        return books_list


# ============== Stack for operation history =============
class OperationStack:
    """Stack for operation history"""
    def __init__(self):
        self.stack = []
    
    def push(self, operation):
        """Push operation to stack"""
        self.stack.append(operation)
        if len(self.stack) > 20:
            self.stack.pop(0)
    
    def pop(self):
        """Pop operation from stack"""
        if not self.is_empty():
            return self.stack.pop()
        return None
    
    def is_empty(self):
        return len(self.stack) == 0
    
    def display(self):
        """Display operation history"""
        if self.is_empty():
            print("Operation history is empty")
        else:
            print("Recent Operations:")
            for i, op in enumerate(reversed(self.stack), 1):
                print(f"  {i}. {op}")


# ============== users acount =============
class UsersAcount:
    def __init__(self, filepath="acount_info.csv"):
        self.save_acc_info = filepath
        
        if not os.path.exists(self.save_acc_info):
            directory = os.path.dirname(self.save_acc_info)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            with open(self.save_acc_info, "w", encoding="utf-8") as f:
                pass

    def save(self, Username, Password, Borrowed_books):
        Users = self.loadUser()
        Users[Username] = {
            "Password": Password,
            "Borrowed_books": ",".join([b.strip() for b in Borrowed_books]) if isinstance(Borrowed_books, list) else Borrowed_books
        }
        with open(self.save_acc_info, "w", encoding="utf-8") as csv:
            for user, data in Users.items():
                csv.write(f"{user},{data['Password']},{data['Borrowed_books']}\n")

    def loadUser(self):
        Users = {}
        if not os.path.exists(self.save_acc_info):
            return Users
        
        try:
            with open(self.save_acc_info, "r", encoding="utf-8") as csv:
                for line in csv:
                    line = line.strip()
                    if line:
                        parts = line.split(",", 2)
                        if len(parts) == 3:
                            Username, Password, Borrowed_books = [x.strip() for x in parts]
                            Users[Username] = {
                                "Password": Password,
                                "Borrowed_books": Borrowed_books
                            }
                        elif len(parts) == 2:
                            Username, Password = [x.strip() for x in parts]
                            Users[Username] = {
                                "Password": Password,
                                "Borrowed_books": ""
                            }
        except Exception as e:
            print(f"Error loading users: {e}")
        
        return Users

    def createAcount(self, library=None):
        print("\n=== Create New Account ===")
        print("(Enter '0' at any time to go back)")
        Borrowed_books = []
        
        while True:
            Users = self.loadUser()
            Username = input("\nEnter your Username (or 0 to go back): ").strip()
            
            if Username == "0":
                print("Returning to main menu...")
                return  # بازگشت به منوی اصلی
            
            if not Username:
                print("Username cannot be empty!")
                continue
            
            if Username in Users:
                print("This username already exists ❌")
                print("\n1. Login with existing account")
                print("2. Try another username")
                print("0. Go back to main menu")
                
                choice = input("Enter your choice: ").strip()
                
                if choice == "1":
                    self.login(library)
                    return
                elif choice == "2":
                    continue
                elif choice == "0":
                    print("Returning to main menu...")
                    return
                else:
                    print("Invalid choice! Please try again.")
                    continue
            else:
                break

        while True:
            Password = input("\nEnter your password (min 8 chars, or 0 to go back): ")
            
            if Password == "0":
                print("Account creation cancelled.")
                return
            
            if len(Password) >= 8:
                break
            print("Password is too short ❌ (must be at least 8 characters)")

        self.save(Username, Password, Borrowed_books)
        print(f"\n✅ User '{Username}' created successfully!")
        print("You will now be logged in automatically...")
        
        self.login(library)

    def login(self, library=None):
        print("\n=== User Login ===")
        print("(Enter '0' at any time to go back)")
        
        while True:
            Users = self.loadUser()
            Username = input("\nEnter your username (or 0 to go back): ").strip()
            
            if Username == "0":
                print("Returning to main menu...")
                return
            
            if Username not in Users:
                print("Username not found ❌")
                print("\n1. Try again")
                print("2. Create new account")
                print("0. Go back to main menu")
                
                choice = input("Enter your choice: ").strip()
                
                if choice == "1":
                    continue
                elif choice == "2":
                    self.createAcount(library)
                    return
                elif choice == "0":
                    return
                else:
                    print("Invalid choice!")
                continue
            
            attempts = 3
            while attempts > 0:
                Password = input(f"Enter your password (attempts left: {attempts}): ")
                
                if Password == "0":
                    print("Login cancelled.")
                    return
                
                if Password == Users[Username]["Password"]:
                    print(f"\n✅ Successfully logged in as '{Username}'")
                    self.acountMenu(Username, Users, library)
                    return
                else:
                    attempts -= 1
                    if attempts > 0:
                        print(f"Incorrect password ❌ (attempts left: {attempts})")
                    else:
                        print("Too many failed attempts. Returning to main menu...")
                        return
            
            retry = input("\nForgot password? (y/n): ").strip().lower()
            if retry == 'y':
                # در واقعیت باید سیستم بازیابی رمز عبور داشته باشیم
                print("Please contact administrator to reset your password.")
                return

    def acountMenu(self, Username, Users, library=None):
        while True:
            print(f"\n{'='*50}")
            print(f"User Panel - Welcome {Username}")
            print(f"{'='*50}")
            print("1. 📋 Show account info")
            print("2. 🔍 Search & Borrow a book")
            print("3. ↩️  Return a book")
            print("4. 📚 View all available books")
            print("5. 🚪 Log out")
            print(f"{'='*50}")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.username_info(Username, Users)
                input("\nPress Enter to continue...")
            elif choice == "2":
                if library is None:
                    print("Library not connected ❌")
                    continue
                self.borrow_book_menu(Username, Users, library)
            elif choice == "3":
                if library is None:
                    print("Library not connected ❌")
                    continue
                self.return_book(Username, Users, library)
            elif choice == "4":
                if library is None:
                    print("Library not connected ❌")
                    continue
                self.view_all_books(library)
            elif choice == "5":
                print(f"\n👋 Logging out '{Username}'...")
                return
            else:
                print("Invalid choice ❌")

    def borrow_book_menu(self, Username, Users, library=None):
        print("\n====== Search & Borrow Books ======")
        print("(Enter '0' at any time to go back)")
        
        keyword = input("\nEnter book name or author to search (or 0 to go back): ").strip()
        
        if keyword == "0":
            return
        
        found_nodes = []
        if library.book_linked_list and library.book_linked_list.head:
            found_nodes = library.book_linked_list.find_all_books_recursive(
                library.book_linked_list.head, keyword
            )
        
        if not found_nodes:
            results = library.search_books(keyword, False)
            if not results:
                print("No books found with that keyword ❌")
                input("\nPress Enter to continue...")
                return
            else:
                print(f"\nFound {len(results)} book(s):")
                for idx, (i, book) in enumerate(results, 1):
                    print(f"{idx}. {book['name']} by {book['author']} ({book['year']}) - Copies left: {book['available_copies']}")
                
                self.process_borrow_selection(results, Username, Users, library)
        else:
            print(f"\nFound {len(found_nodes)} book(s):")
            for idx, node in enumerate(found_nodes, 1):
                book = node.book_data
                print(f"{idx}. {book['name']} by {book['author']} ({book['year']}) - Available copies: {book['available_copies']}")
            
            self.process_borrow_selection_found(found_nodes, Username, Users, library)

    def process_borrow_selection(self, results, Username, Users, library):
        while True:
            bookIndex = input(f"\nEnter number of book to borrow (1 to {len(results)}), 0 to go back: ")
            
            if bookIndex == "0":
                print("Returning to user menu...")
                return
            
            if bookIndex.isdigit() and 1 <= int(bookIndex) <= len(results):
                selected_index = results[int(bookIndex)-1][0]
                borrowed_books = Users[Username]["Borrowed_books"].split(",") if Users[Username]["Borrowed_books"] else []
                
                if f"{library.books[selected_index]['name']} ({library.books[selected_index]['author']})" in [b.strip() for b in borrowed_books]:
                    print("You already have this book borrowed ❌")
                    continue
                
                confirm = input(f"Do you want to borrow '{library.books[selected_index]['name']}'? (y/n): ").strip().lower()
                if confirm == "y":
                    library.borrow_book(selected_index, Username, self)
                    Users = self.loadUser()
                    break
                elif confirm == "n":
                    print("Borrow cancelled.")
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
            else:
                print("Invalid selection ❌")

    def process_borrow_selection_found(self, found_nodes, Username, Users, library):
        while True:
            book_choice = input(f"\nEnter number of book to borrow (1 to {len(found_nodes)}), 0 to go back: ")
            
            if book_choice == "0":
                print("Returning to user menu...")
                return
            
            if book_choice.isdigit() and 1 <= int(book_choice) <= len(found_nodes):
                selected_node = found_nodes[int(book_choice) - 1]
                selected_book = selected_node.book_data
                
                borrowed_books = Users[Username]["Borrowed_books"].split(",") if Users[Username]["Borrowed_books"] else []
                if f"{selected_book['name']} ({selected_book['author']})" in [b.strip() for b in borrowed_books]:
                    print("You already have this book borrowed ❌")
                    continue
                
                confirm = input(f"Do you want to borrow '{selected_book['name']}'? (y/n): ").strip().lower()
                if confirm == "y":
                    for i, book in enumerate(library.books):
                        if book['name'] == selected_book['name'] and book['author'] == selected_book['author']:
                            library.borrow_book(i, Username, self)
                            Users = self.loadUser()
                            break
                    break
                elif confirm == "n":
                    print("Borrow cancelled.")
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
            else:
                print("Invalid selection ❌")

    def view_all_books(self, library):
        print("\n=== All Available Books ===")
        if library.book_linked_list and library.book_linked_list.head:
            available_count = 0
            current = library.book_linked_list.head
            count = 1
            
            while current:
                book = current.book_data
                if book['available_copies'] > 0:
                    print(f"{count}. {book['name']} by {book['author']} ({book['year']}) - Available: {book['available_copies']}")
                    available_count += 1
                    count += 1
                current = current.next
            
            if available_count == 0:
                print("No books available at the moment.")
            else:
                print(f"\nTotal available books: {available_count}")
        else:
            print("No books in the library.")
        
        input("\nPress Enter to continue...")

    def username_info(self, Username, Users):
        borrowed = Users[Username]['Borrowed_books']
        borrowed_list = [b.strip() for b in borrowed.split(",") if b.strip()] if borrowed else []
        
        print(f"\n{'='*50}")
        print(f"Account Information for: {Username}")
        print(f"{'='*50}")
        print(f"👤 Username: {Username}")
        print(f"🔒 Password: {'*' * len(Users[Username]['Password'])}")
        print(f"\n📚 Borrowed Books:")
        
        if borrowed_list:
            for idx, book in enumerate(borrowed_list, 1):
                print(f"   {idx}. {book}")
        else:
            print("   No books borrowed yet")
        print(f"{'='*50}")

    def return_book(self, username, Users, library):
        borrowed = Users[username]['Borrowed_books']
        borrowed_list = [b.strip() for b in borrowed.split(",") if b.strip()] if borrowed else []
        
        if not borrowed_list:
            print("\n📭 You have no books to return.")
            input("\nPress Enter to continue...")
            return

        print(f"\n{'='*50}")
        print("Your Borrowed Books:")
        print(f"{'='*50}")
        
        for idx, book in enumerate(borrowed_list, 1):
            print(f"{idx}. {book}")
        
        print(f"{'='*50}")
        
        while True:
            sel = input(f"\nEnter number of book to return (1 to {len(borrowed_list)}), 0 to cancel: ")
            
            if sel == "0":
                print("Return cancelled.")
                return
            
            if sel.isdigit() and 1 <= int(sel) <= len(borrowed_list):
                book_name = borrowed_list[int(sel)-1]
                found = False
                
                for b in library.books:
                    full_name = f"{b['name']} ({b['author']})"
                    if full_name == book_name:
                        b['available_copies'] += 1
                        found = True
                        break
                
                if found:
                    borrowed_list.pop(int(sel)-1)
                    Users[username]["Borrowed_books"] = ", ".join(borrowed_list)
                    self.save(username, Users[username]["Password"], borrowed_list)
                    library.save_books()
                    library.operation_stack.push(f"Return book: {book_name} by {username}")
                    print(f"\n✅ Book '{book_name}' returned successfully!")
                    input("\nPress Enter to continue...")
                    return
                else:
                    print("Book not found in library database ❌")
            else:
                print("Invalid selection ❌")


# -------------------- Library --------------------
class Library:
    def __init__(self, filepath="books.json", txtfile="books.txt"):
        self.filepath = filepath
        self.txtfile = txtfile
        self.books = []
        self.book_linked_list = BookLinkedList()
        self.operation_stack = OperationStack()

        if not os.path.exists(self.txtfile):
            with open(self.txtfile, "w", encoding="utf-8") as f:
                pass

        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump([], f)

        self.load_books(False)

    def load_books(self, isAdmin=False):
        self.filepath = "books.json"
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                self.books = json.load(f)
        
        if not self.books and os.path.exists(self.txtfile):
            with open(self.txtfile, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 4:
                        name, author, year, total_copies = parts
                        self.books.append({
                            "name": name.strip(),
                            "author": author.strip(),
                            "year": int(year),
                            "total_copies": int(total_copies),
                            "available_copies": int(total_copies),
                            "borrowed": False
                        })
        
        self.book_linked_list = BookLinkedList()
        for book in self.books:
            self.book_linked_list.add_book(book)
        
        if isAdmin:
            print("\n=== Books in Linked List (Recursive Display) ===")
            if self.book_linked_list.head:
                self.book_linked_list.display_all_recursive(self.book_linked_list.head)
            else:
                print("No books in the library")
            
            total_books = self.book_linked_list.size
            available_books = self.book_linked_list.count_available_recursive()
            print(f"\n=== Library Statistics ===")
            print(f"📚 Total books: {total_books}")
            print(f"✅ Available books: {available_books}")
            print(f"📖 Borrowed books: {total_books - available_books}")

    def save_books(self):
        self.books = self.book_linked_list.traverse()
        
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.books, f, indent=4)
        
        self.operation_stack.push("Save all books")

    def search_books(self, keyword, isAdmin=False):
        keyword = keyword.lower()
        results = []
        for i, book in enumerate(self.books):
            if keyword in book["name"].lower() or keyword in book["author"].lower():
                results.append((i, book))
        if isAdmin:
            for idx, (i, book) in enumerate(results, 1):
                print(f"{idx}. {book['name']} by {book['author']} ({book['year']}) - Copies left: {book['available_copies']}")
        
        self.operation_stack.push(f"Search books with keyword: {keyword}")
        return results

    def adminSearch(self):
        print("\n=== Admin Search Books ===")
        print("(Enter '0' to go back)")
        
        keyword = input("\nEnter book name or author to search: ").strip()
        
        if keyword == "0":
            return
        
        results = self.search_books(keyword, True)
        
        if not results:
            print("\nNo books found with that keyword.")
        
        return results

    def borrow_book(self, book_index, username, UsersAcount):
        if book_index < 0 or book_index >= len(self.books):
            print("Invalid book index ❌")
            return
            
        book = self.books[book_index]
        Users = UsersAcount.loadUser()
        
        if username not in Users:
            print("User not found ❌")
            return
            
        borrowed_books = Users[username]["Borrowed_books"].split(",") if Users[username]["Borrowed_books"] else []

        if f"{book['name']} ({book['author']})" in [b.strip() for b in borrowed_books]:
            print(f"You already have this book '{book['name']}' ❌")
            return

        if book["available_copies"] > 0:
            book["available_copies"] -= 1
            if book["available_copies"] == 0:
                book["borrowed"] = True

            self.book_linked_list = BookLinkedList()
            for b in self.books:
                self.book_linked_list.add_book(b)

            borrowed_books.append(f"{book['name']} ({book['author']})")
            Users[username]["Borrowed_books"] = ", ".join(borrowed_books)
            UsersAcount.save(username, Users[username]["Password"], borrowed_books)
            self.save_books()
            
            self.operation_stack.push(f"Borrow book: {book['name']} by {username}")
            print(f"\n✅ {username} successfully borrowed '{book['name']}'")
        else:
            print("❌ No available copies left for this book")

    def adminEdit(self, book_index):
        if book_index < 1 or book_index > len(self.books):
            print("Invalid book index ❌")
            return
            
        book = self.books[book_index - 1]
        print(f"\n📖 Editing: {book['name']} by {book['author']} ({book['year']})")
        print(f"   Current copies: {book['available_copies']}")
        print(f"\n1. Add or remove copies")
        print("2. Set copies to 0")
        print("0. Go back")
        
        edit_choice = input("\nEnter your choice: ").strip()
        
        if edit_choice == "0":
            print("Edit cancelled.")
            return
        elif edit_choice == "1":
            print("\nEnter number to add or remove (e.g., +2 to add 2, -1 to remove 1)")
            num_edit = input("Enter number: ").strip()
            
            try:
                num_edit = int(num_edit)
                if book['available_copies'] + num_edit < 0:
                    print(f"❌ Cannot remove {abs(num_edit)} copies. Only {book['available_copies']} available.")
                else:
                    book['available_copies'] += num_edit
                    print(f"✅ Updated! {book['name']} now has {book['available_copies']} copies available.")
                    self.save_books()
                    self.operation_stack.push(f"Edit copies of '{book['name']}' to {book['available_copies']}")
            except ValueError:
                print("❌ Invalid input format. Please enter a number like +2 or -1")
        
        elif edit_choice == "2":
            confirm = input(f"Are you sure you want to set all copies of '{book['name']}' to 0? (y/n): ").strip().lower()
            if confirm == 'y':
                book['available_copies'] = 0
                print(f"✅ {book['name']} now has 0 copies available.")
                self.save_books()
                self.operation_stack.push(f"Set copies of '{book['name']}' to 0")
            else:
                print("Operation cancelled.")
        else:
            print("Invalid choice ❌")

    def adminAddorRemoveBook(self):
        print("\n=== Add or Remove Books ===")
        print("1. 📝 Add a new book")
        print("2. ❌ Remove a book")
        print("0. ↩️  Go back")
        
        AddOrRemove_Choice = input("\nEnter your choice: ").strip()
        
        if AddOrRemove_Choice == "0":
            print("Returning to admin menu...")
            return
        elif AddOrRemove_Choice == "2":
            if not self.books:
                print("❌ No books to remove")
                return
                
            print("\n📚 Available books to remove:")
            for idx, book in enumerate(self.books, 1):
                print(f"{idx}. {book['name']} by {book['author']}")
            
            try:
                RemoveBook_index = int(input(f"\nEnter index of book to remove (1 to {len(self.books)}), 0 to cancel: "))
                
                if RemoveBook_index == 0:
                    print("Operation cancelled.")
                    return
                
                if 1 <= RemoveBook_index <= len(self.books):
                    RemoveBook_book = self.books[RemoveBook_index-1]
                    confirm = input(f"Are you sure you want to remove '{RemoveBook_book['name']}'? (y/n): ").strip().lower()
                    
                    if confirm == 'y':
                        self.books.remove(RemoveBook_book)
                        self.book_linked_list = BookLinkedList()
                        for book in self.books:
                            self.book_linked_list.add_book(book)
                        self.save_books()
                        self.operation_stack.push(f"Remove book: '{RemoveBook_book['name']}'")
                        print(f"✅ Book '{RemoveBook_book['name']}' removed successfully")
                    else:
                        print("Operation cancelled.")
                else:
                    print("❌ Invalid index")
            except ValueError:
                print("❌ Invalid input")

        elif AddOrRemove_Choice == "1":
            print("\n📝 Adding a new book:")
            print("(Enter '0' at any time to cancel)")
            
            name = input("Enter book name: ").strip()
            if name == "0":
                print("Operation cancelled.")
                return
                
            author = input("Enter book author name: ").strip()
            if author == "0":
                print("Operation cancelled.")
                return
                
            year = input("Enter year of book: ").strip()
            if year == "0":
                print("Operation cancelled.")
                return
                
            total_copies = input("Enter total copies of book: ").strip()
            if total_copies == "0":
                print("Operation cancelled.")
                return
            
            try:
                new_book = {
                    "name": name,
                    "author": author,
                    "year": int(year),
                    "total_copies": int(total_copies),
                    "available_copies": int(total_copies),
                    "borrowed": False
                }
                self.books.append(new_book)
                self.book_linked_list.add_book(new_book)
                self.save_books()
                self.operation_stack.push(f"Add new book: '{new_book['name']}'")
                print(f"✅ Book '{new_book['name']}' added successfully")
            except ValueError:
                print("❌ Invalid input for year or copies")
        else:
            print("❌ Invalid choice")

    def AdminShowBorrowedBooks(self):
        if not os.path.exists("acount_info.csv"):
            print("❌ No user data found")
            return
            
        try:
            with open("acount_info.csv", "r", encoding="utf-8") as csv:
                has_data = False
                print(f"\n{'='*60}")
                print("📚 Currently Borrowed Books by Users")
                print(f"{'='*60}")
                
                for line in csv:
                    if line.strip() and "," in line:
                        parts = line.strip().split(",", 2)
                        if len(parts) == 3:
                            Username, Password, Borrowed_books = [x.strip() for x in parts]
                            if Borrowed_books and Borrowed_books != "":
                                print(f"\n👤 User: {Username}")
                                print("📖 Borrowed Books:")
                                books = Borrowed_books.split(",")
                                for idx, book in enumerate(books, 1):
                                    print(f"   {idx}. {book.strip()}")
                                print(f"{'-'*40}")
                                has_data = True
                
                if not has_data:
                    print("\n📭 No borrowed books found")
                print(f"{'='*60}")
        except Exception as e:
            print(f"❌ Error reading borrowed books: {e}")


# -------------------- admin --------------------
class Admin:
    def __init__(self):
        pass

    def adminLogin(self, library):
        print("\n=== Admin Login ===")
        print("(Enter '0' at any time to go back)")
        
        adminUsername = input("\nEnter admin username (or 0 to go back): ").strip()
        
        if adminUsername == "0":
            print("Returning to main menu...")
            return
        
        if adminUsername != "admin":
            print(f"❌ User '{adminUsername}' not found or not an admin")
            retry = input("\n1. Try again\n2. Return to main menu\nEnter choice: ").strip()
            
            if retry == "1":
                self.adminLogin(library)
            return
        
        attempts = 3
        while attempts > 0:
            adminPassword = input(f"Enter admin password (attempts left: {attempts}): ")
            
            if adminPassword == "0":
                print("Login cancelled.")
                return
            
            if adminPassword == "admin":
                print(f"\n✅ Welcome {adminUsername}!")
                self.adminMenu(library)
                return
            else:
                attempts -= 1
                if attempts > 0:
                    print(f"❌ Incorrect password! Attempts left: {attempts}")
                else:
                    print("❌ Too many failed attempts. Returning to main menu...")
                    return

    def adminMenu(self, library):
        while True:
            print(f"\n{'='*50}")
            print("👑 Admin Panel")
            print(f"{'='*50}")
            print("1. ✏️  Edit books")
            print("2. 🔍 Search books")
            print("3. 📚 Add or remove books")
            print("4. 👥 Show borrowed books")
            print("5. 📜 Show operation history (Stack)")
            print("6. 🔗 Show all books (Linked List)")
            print("7. 🚪 Exit admin panel")
            print(f"{'='*50}")
            
            admin_choice = input("\nEnter your choice: ").strip()
            
            if admin_choice == "1":
                library.load_books(True)
                if library.books:
                    try:
                        admin_index = int(input(f"\nEnter book index to edit (1 to {len(library.books)}), 0 to go back: "))
                        if admin_index == 0:
                            print("Returning to admin menu...")
                            continue
                        library.adminEdit(admin_index)
                    except ValueError:
                        print("❌ Invalid index")
                else:
                    print("❌ No books to edit")
            
            elif admin_choice == "2":
                library.adminSearch()
                
                if library.books:
                    print("\nOptions:")
                    print("1. Edit a book from search results")
                    print("2. Add or remove books")
                    print("0. Return to admin menu")
                    
                    after_search_choice = input("Enter your choice: ").strip()
                    
                    if after_search_choice == "1":
                        try:
                            admin_index = int(input("Enter book index to edit: "))
                            library.adminEdit(admin_index)
                        except ValueError:
                            print("❌ Invalid index")
                    elif after_search_choice == "2":
                        library.adminAddorRemoveBook()
                    elif after_search_choice == "0":
                        continue
                    else:
                        print("❌ Invalid choice")
            
            elif admin_choice == "3":
                library.load_books(True)
                library.adminAddorRemoveBook()
            
            elif admin_choice == "4":
                library.AdminShowBorrowedBooks()
                input("\nPress Enter to continue...")
            
            elif admin_choice == "5":
                print(f"\n{'='*50}")
                print("📜 Operation History (Last 20 operations)")
                print(f"{'='*50}")
                library.operation_stack.display()
                input("\nPress Enter to continue...")
            
            elif admin_choice == "6":
                print(f"\n{'='*50}")
                print("🔗 All Books (Linked List Structure)")
                print(f"{'='*50}")
                if library.book_linked_list.head:
                    library.book_linked_list.display_all_recursive(library.book_linked_list.head)
                    
                    total_books = library.book_linked_list.size
                    available_books = library.book_linked_list.count_available_recursive()
                    
                    print(f"\n{'='*50}")
                    print(f"📊 Library Statistics:")
                    print(f"   📚 Total books: {total_books}")
                    print(f"   ✅ Available books: {available_books}")
                    print(f"   📖 Borrowed books: {total_books - available_books}")
                    print(f"{'='*50}")
                else:
                    print("📭 No books in the library")
                input("\nPress Enter to continue...")
            
            elif admin_choice == "7":
                print("👋 Exiting admin panel...")
                break
            
            else:
                print("❌ Invalid choice")


# -------------------- main --------------------
def main():
    library = Library()
    users = UsersAcount()
    admin = Admin()

    print(f"\n{'='*60}")
    print("📚 WELCOME TO LIBRARY MANAGEMENT SYSTEM 📚")
    print(f"{'='*60}")
    
    while True:
        print(f"\n{'='*50}")
        print("🏠 Main Menu")
        print(f"{'='*50}")
        print("1. 👤 Create account")
        print("2. 🔑 Login")
        print("3. 👑 Admin panel")
        print("4. 🚪 Exit")
        print(f"{'='*50}")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            users.createAcount(library)
        elif choice == "2":
            users.login(library)
        elif choice == "3":
            admin.adminLogin(library)
        elif choice == "4":
            print(f"\n{'='*50}")
            print("👋 Thank you for using Library Management System!")
            print("📚 Goodbye!")
            print(f"{'='*50}")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
