MY-LogiC** is a simple, modern web application that allows users to upload legal contracts (PDFs), automatically extract clauses, classify them, and assign basic risk scores + explanations.

Built as an MVP to demonstrate AI-assisted contract review.

## Current Features

- Beautiful, responsive single-page frontend (glassmorphism + dark/light mode)
- Upload PDF contracts directly from browser
- Text extraction using PyMuPDF
- Rule-based clause type detection (liability, indemnification, termination, etc.)
- Basic risk scoring & reasoning
- Clean results display with confidence scores & highlighted text

## Project Structure
contract-risk-analyzer/
├── backend/                    # FastAPI backend
│   ├── app.py                  # Main application (PDF upload + analysis)
│   └── requirements.txt        # Python dependencies
├── frontend/                   # Single-file static frontend
│   └── index.html              # Complete UI (HTML + CSS + JS)
├── data/
│   └── sample_contracts/       # (optional) put test PDFs here
├── README.md                   # This file
└── .gitignore
text## Tech Stack

**Frontend**
- HTML5 + CSS3 (custom glassmorphism)
- Vanilla JavaScript (no frameworks/build tools)
- Google Fonts (Outfit + Plus Jakarta Sans)
- Font Awesome icons

**Backend**
- FastAPI (modern Python API framework)
- PyMuPDF / fitz (fast PDF text extraction)
- Uvicorn (ASGI server)

## Prerequisites

- Python 3.9+
- pip
- Git

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/contract-risk-analyzer.git
cd contract-risk-analyzer
2. Backend Setup
Bashcd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
3. Run the Backend
Bashuvicorn app:app --reload --port 8001
→ Open http://localhost:8001/docs to see interactive Swagger UI (for testing)
4. Frontend Setup
No build tools required (single HTML file)
Bashcd ../frontend
python -m http.server 5500
→ Open http://localhost:5500 in your browser
How to Use

Go to http://localhost:5500
Click to upload a PDF contract (or drag & drop)
Recommended: use clean, text-selectable PDFs (not scanned/images)

Click Run Risk Analysis
View detected clauses, confidence scores, and risk flags

Development Notes

Clause detection is currently keyword-based (simple MVP version)
Next steps:
Replace with fine-tuned Legal-BERT for better classification
Add LLM-powered natural language risk explanations
Improve paragraph/clause segmentation
Support scanned PDFs (OCR)
Add user authentication (JWT) if needed later


Contributing
Feel free to fork and submit pull requests!

Fork the repo
Create your feature branch (git checkout -b feature/amazing-feature)
Commit changes (git commit -m 'Add amazing feature')
Push to branch (git push origin feature/amazing-feature)
Open a Pull Request

License
MIT License – see LICENSE for details.
Acknowledgments

UI inspired by modern glassmorphism trends
Built with love in Coimbatore, Tamil Nadu

Made with ❤️ by Yugeswaran.D
text### Quick Tips for GitHub

1. Create a file named `LICENSE` in the root with MIT content (or choose another license)
2. Add a few nice screenshots/GIFs to README (upload to repo → drag into markdown)
   Example:
