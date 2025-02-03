# WebCrawlAI: AI-Powered Web Scraper

This project implements a web scraping API that leverages the Gemini AI model to extract specific information from websites.  It provides a user-friendly interface for defining extraction criteria and handles dynamic content and CAPTCHAs using a scraping browser.  The API is deployed on Render and is designed for easy integration into various projects.

## Features

*   Scrapes data from websites, handling dynamic content and CAPTCHAs.
*   Uses Gemini AI to precisely extract the requested information.
*   Provides a clean JSON output of the extracted data.
*   Includes a user-friendly web interface for easy interaction.
*   Error handling and retry mechanisms for robust operation.
*   Event tracking using GetAnalyzr for monitoring API usage.

## Usage

1.  **Access the Web Interface:** Visit [https://webcrawlai.onrender.com/](https://webcrawlai.onrender.com/)
2.  **Enter the URL:** Input the website URL you want to scrape.
3.  **Specify Extraction Prompt:** Provide a clear description of the data you need (e.g., "Extract all product names and prices").
4.  **Click "Extract Information":** The API will process your request, and the results will be displayed.

## Installation

This project is deployed as a web application. No local installation is required for usage.  However, if you wish to run the code locally, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/WebCrawlAI.git
    cd WebCrawlAI
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set Environment Variables:** Create a `.env` file (refer to `.env.example`) and populate it with your `SBR_WEBDRIVER` (Bright Data Scraping Browser URL) and `GEMINI_API_KEY` (Google Gemini API Key).
4.  **Run the Application:**
    ```bash
    python main.py
    ```

## Technologies Used

*   **Flask (3.0.0):** Web framework for building the API.
*   **BeautifulSoup (4.12.2):** HTML/XML parser for extracting data from web pages.
*   **Selenium (4.16.0):** For automating browser interactions, handling dynamic content and CAPTCHAs.
*   **lxml:** Fast and efficient XML and HTML processing library.
*   **html5lib:**  For parsing HTML documents.
*   **python-dotenv (1.0.0):** For managing environment variables.
*   **google-generativeai (0.3.1):**  Integrates the Gemini AI model for data parsing and extraction.
*   **axios:** JavaScript library for making HTTP requests (client-side).
*   **marked:** JavaScript library for rendering Markdown (client-side).
*   **Tailwind CSS:** Utility-first CSS framework for styling (client-side).
*   **GetAnalyzr:** For event tracking and API usage monitoring.
*   **Bright Data Scraping Browser:** Provides fully-managed, headless browsers for reliable web scraping.


## API Documentation

**Endpoint:** `/scrape-and-parse`

**Method:** `POST`

**Request Body (JSON):**

```json
{
  "url": "https://www.example.com",
  "parse_description": "Extract all product names and prices"
}
```

**Response (JSON):**

**Success:**

```json
{
  "success": true,
  "result": {
    "products": [
      {"name": "Product A", "price": "$10"},
      {"name": "Product B", "price": "$20"}
    ]
  }
}
```

**Error:**

```json
{
  "error": "An error occurred during scraping or parsing"
}
```


## Dependencies

The project dependencies are listed in `requirements.txt`.  Use `pip install -r requirements.txt` to install them.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Testing

No formal testing framework is currently implemented.  Testing should be added as part of future development.


*README.md was made with [Etchr](https://etchr.dev)*