import streamlit as st
import json
import os

LIBRARY_FILE = "library.txt"

# Load library from file if it exists
if os.path.exists(LIBRARY_FILE):
    with open(LIBRARY_FILE, "r") as f:
        try:
            library = json.load(f)
        except json.JSONDecodeError:
            library = []
else:
    library = []

def save_library():
    with open(LIBRARY_FILE, "w") as f:
        json.dump(library, f, indent=4)

def add_book(title, author, year, genre, read):
    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read
    }
    library.append(book)
    save_library()

def remove_book(title):
    global library
    library = [book for book in library if book["title"].lower() != title.lower()]
    save_library()

def search_books(query, by="title"):
    return [book for book in library if query.lower() in book[by].lower()]

def display_statistics():
    total = len(library)
    read_count = sum(1 for book in library if book["read"])
    percentage = (read_count / total) * 100 if total else 0
    return total, percentage

st.set_page_config(page_title="📚 Personal Library Manager", page_icon="📖")
st.title("📚 Personal Library Manager")

menu = ["Add a Book", "Remove a Book", "Search Books", "Display All Books", "Statistics"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add a Book":
    st.header("➕ Add a New Book")
    with st.form("add_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=0, max_value=2100, step=1)
        genre = st.text_input("Genre")
        read = st.checkbox("Have you read this book?")
        submitted = st.form_submit_button("Add Book")
        if submitted:
            add_book(title, author, int(year), genre, read)
            st.success("Book added successfully!")

elif choice == "Remove a Book":
    st.header("🗑️ Remove a Book")
    titles = [book["title"] for book in library]
    if titles:
        selected = st.selectbox("Select a book to remove", titles)
        if st.button("Remove Book"):
            remove_book(selected)
            st.success("Book removed successfully!")
    else:
        st.info("No books available to remove.")

elif choice == "Search Books":
    st.header("🔍 Search Books")
    search_by = st.radio("Search by", ["title", "author"])
    query = st.text_input("Enter your search term")
    if query:
        results = search_books(query, search_by)
        if results:
            for book in results:
                status = "✅ Read" if book["read"] else "❌ Unread"
                st.markdown(f"**{book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {status}")
        else:
            st.warning("No matching books found.")

elif choice == "Display All Books":
    st.header("📖 All Books in Library")
    if library:
        for i, book in enumerate(library, 1):
            status = "✅ Read" if book["read"] else "❌ Unread"
            st.markdown(f"**{i}. {book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {status}")
    else:
        st.info("Library is empty.")

elif choice == "Statistics":
    st.header("📊 Library Statistics")
    total, percentage = display_statistics()
    st.metric("Total Books", total)
    st.metric("Percentage Read", f"{percentage:.1f}%")