import os
import subprocess
from libgen.scraper import Scraper

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

# Function to download and convert the book if necessary
def download_book(book, output_dir, downloaded_titles):
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, f"{book['name']}.{book['format'].lower()}")
    
    if book['name'] in downloaded_titles:
        print(f"Skipping already downloaded book: {book['name']}")
        return

    print(f"Downloading: {book['name']}")

    download_successful = scraper.download(book['link'], output_path=output_file)
    
    if download_successful:
        print(f"Downloaded: {output_file}")
        if book['format'].lower() != "pdf":
            output_pdf = os.path.join(output_dir, f"{book['name']}.pdf")
            convert_to_pdf(output_file, output_pdf)
        downloaded_titles.add(book['name'])
    else:
        print(f"Download failed for: {book['name']}")

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

# Search for books based on user input
query = input("Enter the book title or query: ")
books = scraper.get_data(query)

# Filter the books
filtered_books = filter_books(books)

# Display the filtered books with an index for user selection
for index, book in enumerate(filtered_books):
    print(f"{index + 1}. {book['name']} ({book['year']}) - {book['format']}")

# Ask user to select the books they want to download
selection = input("Enter the numbers of the books to download (comma-separated, e.g., 1,3,5): ")
selected_indices = [int(x.strip()) - 1 for x in selection.split(',')]

# Validate the selected indices
selected_books = [filtered_books[i] for i in selected_indices if 0 <= i < len(filtered_books)]

# Download the selected books
downloaded_titles = set()
for book in selected_books:
    download_book(book, output_dir="downloads", downloaded_titles=downloaded_titles)

print("All selected books have been processed.")
