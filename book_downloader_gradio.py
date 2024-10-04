import os
import subprocess
from libgen.scraper import Scraper
import gradio as gr

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
def download_book(book, output_dir, downloaded_titles):
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, f"{book['name']}.{book['format'].lower()}")
    
    if book['name'] in downloaded_titles:
        print(f"Skipping already downloaded book: {book['name']}")
        return f"Skipped: {book['name']}"

    print(f"Downloading: {book['name']}")

    try:
        download_successful = scraper.download(book['link'], output_path=output_file)
        if download_successful:
            print(f"Downloaded: {output_file}")
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

# Gradio Interface function to handle searches and downloads
def search_books(query):
    # Search for books
    books = scraper.get_data(query)
    # Filter and prioritize the books
    print("Books format")
    print(books)
    filtered_books = filter_books(books)
    print("Filtered books format")
    print(filtered_books)

    # Prepare book information for display as a list of lists
    book_info = [[book['name'], book['author'], book['year'], book['format']] for book in filtered_books]
    return filtered_books, book_info  # Return filtered_books for download and book_info for display

def download_selected_books(filtered_books, selected_indices, download_all):
    output_dir = "downloads"
    downloaded_titles = set()
    download_results = []

    if download_all:
        # If 'Select All' is chosen, download all books
        selected_books = filtered_books
    else:
        # Download only selected books based on indices
        selected_books = [filtered_books[i] for i in selected_indices]

    for book in selected_books:
        result = download_book(book, output_dir, downloaded_titles)
        download_results.append(result)

    return download_results

# Gradio Interface
with gr.Blocks() as app:
    gr.Markdown("## Book Downloader")
    query_input = gr.Textbox(label="Enter Book Query", placeholder="e.g., Hands-On ML")
    search_button = gr.Button("Search Books")
    
    # Placeholder for filtered books
    book_list = gr.DataFrame(headers=["Title", "Author", "Year", "Format"], label="Available Books", interactive=True)
    
    # Options to download selected books or all books
    download_all_checkbox = gr.Checkbox(label="Select All Books")
    selected_indices = gr.CheckboxGroup(label="Select Books to Download", choices=[])
    download_button = gr.Button("Download Selected Books")
    
    output_textbox = gr.Textbox(label="Download Results", interactive=False, lines=10)

    # Set up button callbacks
    search_button.click(search_books, inputs=query_input, outputs=[book_list, selected_indices])
    download_button.click(download_selected_books, inputs=[book_list, selected_indices, download_all_checkbox], outputs=output_textbox)

app.launch()
