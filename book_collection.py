import requests
import csv
import time
from bs4 import BeautifulSoup

# Function to handle pagination and collect book metadata
def get_books(query, max_books=100):
    all_books = []
    page = 1

    while len(all_books) < max_books:
        print(f"Fetching page {page}...")

        try:
            # Adjust the query URL with pagination and 100 results per page
            base_url = "http://libgen.is/search.php"
            params = {
                "req": query,         # The search query
                "res": "100",         # Limit to 100 results per page
                "view": "simple",     # View in simple format (optional)
                "page": page          # Specify the page number
            }
            
            response = requests.get(base_url, params=params, timeout=10)  # Adding timeout for safety
            response.raise_for_status()  # Check if the request was successful
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the table containing search results
            table = soup.find_all('table')[2]  # The third table contains search results
            rows = table.find_all('tr')[1:]  # Skip the header row

            if not rows:
                print(f"No more results on page {page}.")
                break  # Stop if no more results are found

            for row in rows:
                if len(all_books) >= max_books:
                    break  # Stop once we have enough books

                columns = row.find_all('td')
                if len(columns) >= 9:
                    # Extracting relevant metadata from each column
                    book_info = {
                        "id": columns[0].get_text(strip=True),
                        "author": columns[1].get_text(strip=True),
                        "name": columns[2].get_text(strip=True),
                        "publisher": columns[3].get_text(strip=True),
                        "year": columns[4].get_text(strip=True),
                        "language": columns[6].get_text(strip=True),
                        "size": columns[7].get_text(strip=True),
                        "format": columns[8].get_text(strip=True),
                        "link": columns[9].find_all('a')[0]['href']
                    }
                    all_books.append(book_info)

            page += 1  # Move to the next page for the next batch of results
        
        except requests.exceptions.RequestException as e:
            print(f"Request failed on page {page}: {e}. Skipping this page...")
            page += 1  # Skip this page and continue to the next
        
        except IndexError:
            print(f"Unexpected page structure encountered on page {page}. Skipping...")
            page += 1  # Skip this page and continue to the next

    return all_books

# Function to save metadata into a CSV file
def save_books_to_csv(books, filename='libgen_books_metadata.csv'):
    if not books:
        print("No books to save.")
        return

    keys = books[0].keys()  # Extract the headers from the first book entry
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(books)
    print(f"Metadata saved to {filename} successfully.")

# Main script to fetch and store the book metadata
def main():
    query = input("Enter the book title or query: ").replace(" ", "+")
    max_books = int(input("Enter the number of books to fetch (e.g., 100): "))

    # Start timing the execution
    start_time = time.time()

    if books := get_books(query, max_books):
        save_books_to_csv(books)
    else:
        print("No books found for the given query.")

    # Calculate the elapsed time
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
