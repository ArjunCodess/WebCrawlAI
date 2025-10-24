<h1 align="center">WebCrawlAI - AI-Powered Web Scraping Platform</h1>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/ArjunCodess/WebCrawlAI.svg)](https://github.com/ArjunCodess/WebCrawlAI/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/ArjunCodess/WebCrawlAI.svg)](https://github.com/ArjunCodess/WebCrawlAI/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)]()

</div>

---

<p align="center">
  AI-powered web scraping platform that leverages Gemini AI to extract specific information from websites — handles dynamic content, CAPTCHAs, and provides clean JSON output for easy integration.
</p>

---

## 🏆 Sponsors

<div align="center">

| <a href="https://thordata.com" target="_blank"><img src="assets/thordata-logo.png" alt="Thordata Logo" width="100" height="100"/></a> | **Sponsored by [Thordata](https://thordata.com)** — powering reliable proxy infrastructure for developers and data engineers.<br/><br/>**Use code "THOR66" at checkout for 30% off!** |
| :-----------------------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |

</div>

---

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [API Documentation](#api_documentation)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

WebCrawlAI is an intelligent web scraping platform designed to help developers, researchers, and businesses extract specific information from websites with ease. The platform combines advanced web scraping capabilities with AI-powered data extraction to handle complex websites, dynamic content, and CAPTCHAs.

The platform features an AI-powered extraction engine that uses Google's Gemini AI model to precisely parse and extract requested information based on natural language prompts. Users can simply provide a URL and describe what data they need (e.g., "Extract all product names and prices") and receive clean, structured JSON output.

Built with modern web technologies, WebCrawlAI emphasizes reliability through robust error handling, retry mechanisms, and comprehensive monitoring. The platform is designed for both technical and non-technical users, providing a user-friendly web interface alongside a powerful API for integration into existing workflows.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

- **Python** (v3.8 or higher)
- **pip** package manager
- **Bright Data Scraping Browser** account (for SBR_WEBDRIVER)
- **Google Gemini API Key** (for AI-powered extraction)

### Installing

1. **Clone the repository**

   ```bash
   git clone https://github.com/ArjunCodess/WebCrawlAI.git
   cd WebCrawlAI
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file and configure the required variables:

   ```env
   SBR_WEBDRIVER="your_bright_data_scraping_browser_url"
   GEMINI_API_KEY="your_google_gemini_api_key"
   ```

4. **Run the application**

   ```bash
   python main.py
   ```

The application will be available at `http://localhost:5000` (default Flask port).

## 🔧 Running the tests <a name = "tests"></a>

Currently, the project uses manual testing and user acceptance testing. Automated testing setup is planned for future releases.

### Manual Testing

1. **Development Testing**

   - Run the development server with `python main.py`
   - Test core features: web scraping, AI extraction, JSON output
   - Verify error handling and retry mechanisms

2. **Integration Testing**

   - Test with various website types (static, dynamic, with CAPTCHAs)
   - Verify AI extraction accuracy with different prompts
   - Test API endpoints and response formats

3. **User Journey Testing**
   - Complete web interface workflow
   - Test API integration
   - Verify output format and accuracy

## 🎈 Usage <a name="usage"></a>

### Core Features

1. **Web Scraping**

   - Handle static and dynamic websites
   - Bypass CAPTCHAs and anti-bot measures
   - Support for JavaScript-heavy sites

2. **AI-Powered Extraction**

   - Natural language prompts for data extraction
   - Precise parsing using Gemini AI
   - Structured JSON output

3. **Web Interface**

   - User-friendly interface for non-technical users
   - Real-time extraction results
   - Error handling and status updates

4. **API Integration**

   - RESTful API for programmatic access
   - Clean JSON responses
   - Easy integration into existing workflows

5. **Monitoring and Analytics**
   - Event tracking with GetAnalyzr
   - Performance monitoring
   - Usage analytics

### Getting Started Workflow

1. Access the web interface at the deployed URL
2. Enter the target website URL
3. Provide a clear extraction prompt (e.g., "Extract all product names and prices")
4. Click "Extract Information"
5. Review the structured JSON output

## 🚀 Deployment <a name = "deployment"></a>

The project is configured for deployment on Render with the following setup:

### Production Deployment

1. **Render Deployment**

   - Connect your repository to Render
   - Configure environment variables in Render dashboard
   - Deploy automatically on pushes to main branch

2. **Required Environment Variables**

   ```env
   SBR_WEBDRIVER="your_bright_data_scraping_browser_url"
   GEMINI_API_KEY="your_google_gemini_api_key"
   FLASK_ENV="production"
   ```

3. **Service Configuration**

   - Configure as a Web Service on Render
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `python main.py`

4. **Monitoring and Error Tracking**

   - GetAnalyzr integration for event tracking
   - Built-in error handling and logging
   - Performance monitoring capabilities

### Additional Services

- **Bright Data Scraping Browser**: For reliable web scraping with CAPTCHA handling
- **Google Gemini AI**: For intelligent data extraction and parsing
- **GetAnalyzr**: For usage analytics and monitoring

## 📚 API Documentation <a name="api_documentation"></a>

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
      { "name": "Product A", "price": "$10" },
      { "name": "Product B", "price": "$20" }
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

## ⛏️ Built Using <a name = "built_using"></a>

### Core Framework

- [Flask](https://flask.palletsprojects.com/) - Web Framework (v3.0.0)
- [Python](https://www.python.org/) - Programming Language
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML/XML Parser (v4.12.2)

### Web Scraping & Automation

- [Selenium](https://selenium-python.readthedocs.io/) - Browser Automation (v4.16.0)
- [lxml](https://lxml.de/) - Fast XML and HTML Processing
- [html5lib](https://html5lib.readthedocs.io/) - HTML Document Parser
- [Bright Data Scraping Browser](https://brightdata.com/products/scraping-browser) - Managed Browser Service

### AI & Machine Learning

- [Google Generative AI](https://ai.google.dev/) - Gemini AI Integration (v0.3.1)
- [Vercel AI SDK](https://sdk.vercel.ai/) - AI Integration Tools

### Frontend & UI

- [Tailwind CSS](https://tailwindcss.com/) - Utility-First CSS Framework
- [Axios](https://axios-http.com/) - HTTP Client Library
- [Marked](https://marked.js.org/) - Markdown Parser

### Development & Deployment

- [Render](https://render.com/) - Deployment Platform
- [python-dotenv](https://python-dotenv.readthedocs.io/) - Environment Variables (v1.0.0)
- [GetAnalyzr](https://getanalyzr.com/) - Analytics and Event Tracking

### Additional Libraries

- [Waitress](https://docs.pylonsproject.org/projects/waitress/) - WSGI Server

## ✍️ Authors <a name = "authors"></a>

- **ArjunCodess** (Arjun Vijay Prakash) - Project development and maintenance

_Note: This project embraces open-source values and transparency. We love open source because it keeps us accountable, fosters collaboration, and drives innovation. For collaboration opportunities or questions, please reach out through the appropriate channels._

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- **Google** for providing the Gemini AI model that powers our intelligent extraction capabilities
- **Bright Data** for reliable scraping browser infrastructure
- **Render** for the excellent deployment platform
- **Flask Team** for the robust web framework
- **Selenium** for powerful browser automation capabilities
- **Open Source Community** for the countless libraries and tools that make modern web development possible

---

<div align="center">

**WebCrawlAI** - Transforming web data into structured insights

_Built with ❤️ for developers and data enthusiasts_

</div>
