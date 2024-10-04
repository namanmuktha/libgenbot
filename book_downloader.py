import os
import subprocess
from libgen.scraper import Scraper
import streamlit as st

# Function to convert files to PDF using Calibre
def convert_to_pdf(input_file, output_pdf):
    print(f"Converting {input_file} to {output_pdf}...")
    extension = input_file.split('.')[-1].lower()
    
    if extension in ['mobi', 'epub', 'djvu', 'docx']:
        command = f"/Applications/calibre.app/Contents/MacOS/ebook-convert '{input_file}' '{output_pdf}'"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Converted {input_file} to PDF as {output_pdf}")
        else:
            print(f"Error in conversion: {result.stderr.strip()}")
    else:
        print(f"No conversion required for {input_file}, already in PDF format.")
    return output_pdf

# Function to download a book and convert it if necessary
def download_book(book, output_dir, downloaded_titles, progress):
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{book['name']}.{book['format'].lower()}")

    if book['name'] in downloaded_titles:
        return f"Skipped: {book['name']}"

    print(f"Downloading: {book['name']}")

    try:
        download_successful = scraper.download(book['link'], output_path=output_file)
        if download_successful:
            progress.progress(1)  # Update progress to 100%
            if book['format'].lower() != "pdf":
                output_pdf = os.path.join(output_dir, f"{book['name']}.pdf")
                convert_to_pdf(output_file, output_pdf)
            downloaded_titles.add(book['name'])
            return f"Downloaded: {book['name']}"
        else:
            return f"Download failed for: {book['name']}. Check the link."
    except Exception as e:
        return f"An error occurred while downloading {book['name']}: {str(e)}"

# Function to filter and prioritize books
def filter_books(books):
    unique_books = {}
    
    for book in books:
        title = book['name']
        if title not in unique_books:
            unique_books[title] = book
        else:
            existing_book = unique_books[title]
            if (book['year'] > existing_book['year'] and book['format'].lower() == 'pdf') or \
               (book['format'].lower() == 'pdf' and existing_book['format'].lower() != 'pdf'):
                unique_books[title] = book

    return list(unique_books.values())

# Initialize the scraper
scraper = Scraper()

# Streamlit Interface
st.title("Book Downloader")
query_input = st.text_input("Enter Book Query", placeholder="e.g., Hands-On ML")

if st.button("Search Books"):
    # Search for books
    books = scraper.get_data(query_input)
    # Filter and prioritize the books
    st.session_state.filtered_books = filter_books(books)

if 'filtered_books' in st.session_state and st.session_state.filtered_books:
    st.write("Available Books:")
    book_names = [book['name'] for book in st.session_state.filtered_books]
    
    # Maintain selection across interactions
    if 'selected_books' not in st.session_state:
        st.session_state.selected_books = []

    selected_books = st.multiselect("Select Books to Download", options=book_names, 
                                     default=st.session_state.selected_books)

    download_all = st.checkbox("Select All Books")

    if st.button("Download Selected Books"):
        st.session_state.selected_books = selected_books  # Update session state
        output_dir = "downloads"
        downloaded_titles = set()
        download_results = []

        progress = st.progress(0)  # Initialize progress bar
        total_books = len(selected_books)
        
        for index, book in enumerate(st.session_state.filtered_books):
            if book['name'] in selected_books:
                result = download_book(book, output_dir, downloaded_titles, progress)
                download_results.append(result)
                progress.progress((index + 1) / total_books)  # Update progress

        st.text_area("Download Results", "\n".join(download_results), height=200)
else:
    st.write("No books found matching your query.")
