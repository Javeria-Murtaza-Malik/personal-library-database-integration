from pymongo import MongoClient
from dotenv import load_dotenv
import os

# ✅ Load environment variables from .env file
load_dotenv()

# ✅ Get MongoDB Atlas URL from .env
connection_string = os.getenv("MONGO_URI")

# ✅ Connect to MongoDB Atlas
if not connection_string:
    raise ValueError("⚠️ MongoDB connection string is missing in .env file!")

client = MongoClient(connection_string)
db = client["PersonalLibrary"]  # Database name
collection = db["Books"]  # Collection name

# ✅ Check if connection is successful
try:
    client.admin.command("ping")
    print("✅ Successfully connected to MongoDB Atlas!")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")

# ✅ Function to insert sample data
def insert_sample_books():
    sample_books = [
        {"title": "Atomic Habits", "author": "James Clear", "year": 2018},
        {"title": "Deep Work", "author": "Cal Newport", "year": 2016},
        {"title": "The 5 AM Club", "author": "Robin Sharma", "year": 2018}
    ]
    collection.insert_many(sample_books)
    print("✅ Sample books inserted successfully!")

# ✅ Function to fetch and display all books
def fetch_all_books():
    books = collection.find()  # Fetch all documents
    print("\n📚 List of Books in Database:")
    for book in books:
        print(book)

# ✅ Run functions
insert_sample_books()  # Insert sample data
fetch_all_books()  # Fetch and display data
