import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import pandas as pd

# ✅ Load environment variables
load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["PersonalLibrary"]
collection = db["Books"]

class LibraryManager:
    def __init__(self):
        """Initialize MongoDB collection"""
        self.collection = collection

    def add_book(self, title, author, year, genre, read_status):
        """Add a book to MongoDB"""
        book_data = {"title": title, "author": author, "year": year, "genre": genre, "read": read_status}
        self.collection.insert_one(book_data)

    def remove_book(self, title):
        """Remove a book from MongoDB"""
        self.collection.delete_one({"title": title})

    def search_book(self, query):
        """Search for a book in MongoDB"""
        return list(self.collection.find({
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"author": {"$regex": query, "$options": "i"}}
            ]
        }))

    def get_all_books(self):
        """Retrieve all books from MongoDB"""
        return list(self.collection.find())

    def display_statistics(self):
        """Get total books and percentage read"""
        total_books = self.collection.count_documents({})
        read_books = self.collection.count_documents({"read": True})
        percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
        return total_books, percentage_read

library_manager = LibraryManager()

# Streamlit UI
st.title("📚 Personal Library Manager (MongoDB Atlas)")

menu = st.sidebar.selectbox("Menu", ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Statistics"])

if menu == "Add a Book":
    st.header("Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=0, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Mark as Read")
    if st.button("Add Book"):
        library_manager.add_book(title, author, year, genre, read_status)
        st.success("📖 Book added to MongoDB Atlas!")

elif menu == "Remove a Book":
    st.header("Remove a Book")
    books = [book["title"] for book in library_manager.get_all_books()]
    book_to_remove = st.selectbox("Select a book to remove", books) if books else None
    if st.button("Remove Book") and book_to_remove:
        library_manager.remove_book(book_to_remove)
        st.success("❌ Book removed from MongoDB Atlas!")

elif menu == "Search for a Book":
    st.header("Search for a Book")
    query = st.text_input("Enter title or author")
    if st.button("Search") and query:
        results = library_manager.search_book(query)
        if results:
            df = pd.DataFrame(results, columns=["title", "author", "year", "genre", "read"])
            df["read"] = df["read"].apply(lambda x: "✅ Read" if x else "❌ Unread")
            st.dataframe(df)
        else:
            st.warning("No matching books found.")

elif menu == "Display All Books":
    st.header("Your Library")
    books = library_manager.get_all_books()
    if not books:
        st.warning("Your library is empty.")
    else:
        df = pd.DataFrame(books, columns=["title", "author", "year", "genre", "read"])
        df["read"] = df["read"].apply(lambda x: "✅ Read" if x else "❌ Unread")
        st.dataframe(df)

elif menu == "Statistics":
    st.header("Library Statistics")
    total_books, percentage_read = library_manager.display_statistics()
    st.write(f"📚 Total books: {total_books}")
    st.write(f"📖 Percentage read: {percentage_read:.2f}%")
