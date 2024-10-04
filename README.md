# libgenbot


```markdown
# Book Downloader

A Python-based application for downloading eBooks from Library Genesis, with support for multiple formats and conversion to PDF. The application leverages multithreading to speed up downloads and provides options for users to select which books to download.

## Features

- **Search and Filter**: Search for books using keywords and filter results based on the latest versions or preferred formats.
- **Multithreaded Downloads**: Concurrently download multiple books to improve download speeds.
- **File Conversion**: Convert downloaded books in various formats (MOBI, EPUB, DJVU, DOCX) to PDF using Calibre.
- **User-Friendly Interface**: Simple console-based interface for selecting books to download.

## Requirements

- Python 3.6 or later
- `libgen` package: `pip install libgen`
- Calibre (for file conversion) installed on your system.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/book_downloader.git
   cd book_downloader
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure Calibre is installed and accessible on your system.

## Usage

1. Run the application:
   ```bash
   python book_downloader.py
   ```

2. Enter a book title or keyword to search.
3. Select the books you want to download by entering their corresponding numbers.
4. The application will start downloading the selected books concurrently.

## How It Works

- **Searching for Books**: The application uses the `libgen` scraper to search for books based on user input.
- **Filtering**: It filters the results to show only unique titles, preferring the latest version or PDF format.
- **Downloading**: Books are downloaded using multithreading for efficiency, ensuring that multiple books can be downloaded simultaneously.
- **Conversion**: Any non-PDF formats are converted to PDF after downloading, utilizing Calibre’s command-line tools.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. 

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Library Genesis](http://libgen.rs/) for providing access to a vast collection of books.
- [Calibre](https://calibre-ebook.com/) for its powerful ebook management and conversion capabilities.

## Contact

For any questions or suggestions, feel free to reach out at [your.email@example.com](mailto:your.email@example.com).
```

### Explanation of Sections:

1. **Project Title**: Clearly states what the project is about.
2. **Features**: Highlights key functionalities of the application.
3. **Requirements**: Lists necessary software and libraries.
4. **Installation**: Step-by-step instructions on how to set up the project.
5. **Usage**: Simple instructions on how to run the application and what to expect.
6. **How It Works**: Briefly describes the internal workings of the application.
7. **Contributing**: Invites contributions from the community.
8. **License**: Indicates the project's license.
9. **Acknowledgements**: Gives credit to external resources or tools used in the project.
10. **Contact**: Provides a way for users to reach out for support.

Feel free to modify any part of this template to fit your specific project details!