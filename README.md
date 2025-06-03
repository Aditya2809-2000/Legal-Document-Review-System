# Legal Document Analyzer

An AI-powered legal document analysis system that helps legal professionals review and analyze documents with precision and efficiency.

## Features

- Document upload and analysis
- Risk assessment and compliance verification
- Entity extraction and summarization
- Beautiful, responsive UI with modern design
- Drag-and-drop file upload
- Comprehensive metrics and insights

## Tech Stack

- Flask (Backend web framework)
- spaCy (Natural Language Processing)
- PyPDF2 (PDF text extraction)
- Modern HTML/CSS with responsive design
- JavaScript for interactive features

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd legal-document-analyzer
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download spaCy language model:
```bash
python -m spacy download en_core_web_sm
```

5. Run the application:
```bash
python app.py
```

6. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

1. Upload a legal document (supported formats: PDF, DOC, DOCX, TXT)
2. Wait for the analysis to complete
3. Review the generated insights:
   - Document summary
   - Key entities
   - Risk assessment
   - Compliance score

## Project Structure

```
legal-document-analyzer/
├── app.py              # Flask application
├── requirements.txt    # Project dependencies
├── static/
│   └── style.css      # CSS styles
├── templates/
│   └── index.html     # HTML template
└── uploads/           # Temporary file storage
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 