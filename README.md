# AI Prompt Optimizer

A web application that uses Google Gemini AI to optimize and improve your prompts for better AI responses.

## Current Status

- ✅ Frontend completed
- ✅ Flask backend setup
- ✅ Database initialized
- ✅ Project structure established
- 🚧 Gemini API integration in progress
- 🚧 Prompt optimization under development
- 🚧 Prompt quality scoring in progress
- 🚧 Category detection in progress

## Planned Features

- **Prompt Optimization**: Uses Google Gemini AI to enhance your prompts for clarity, specificity, and effectiveness
- **Quality Scoring**: Calculates a quality score (0-100) for prompts based on various criteria
- **Category Detection**: Automatically categorizes prompts (Creative Writing, Code, Business, Education, etc.)
- **PDF Text Extraction**: Upload PDF files to extract text for prompt optimization
- **History Tracking**: View and manage your previous prompt optimizations
- **Statistics Dashboard**: Track your optimization metrics and category distribution

## Project Structure

```
AI-Prompt-Optimizer/
├── app.py                 # Flask application with API routes
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── style.css         # Styling
│   └── script.js         # Frontend JavaScript
├── database/
│   ├── init_db.py        # Database initialization script
│   └── prompts.db        # SQLite database (created on init)
├── utils/
│   ├── score.py          # Prompt scoring algorithm
│   ├── category.py       # Prompt categorization logic
│   ├── gemini.py         # Google Gemini AI integration
│   └── pdf.py            # PDF text extraction
└── reports/              # Directory for generated reports
```

## Installation

1. **Clone or download the project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Add your Google Gemini API key:
     ```
     GEMINI_API_KEY=your_actual_api_key_here
     ```

4. **Initialize the database**:
   ```bash
   python database/init_db.py
   ```

## Usage

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to `http://localhost:5000`

3. **Use the application**:
   - Enter your prompt in the text area
   - Optionally upload a PDF to extract text
   - Click "Optimize Prompt" to enhance your prompt
   - View the optimization results with score comparison
   - Copy the optimized prompt to clipboard
   - Browse your optimization history
   - View statistics about your prompts

## API Endpoints

- `POST /api/optimize` - Optimize a prompt
- `POST /api/upload-pdf` - Upload and extract text from PDF
- `GET /api/history` - Get recent prompt optimizations
- `GET /api/prompt/<id>` - Get specific prompt details
- `DELETE /api/prompt/<id>` - Delete a prompt
- `GET /api/stats` - Get optimization statistics

## Dependencies

- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- google-generativeai 0.3.2
- PyPDF2 3.0.1
- python-dotenv 1.0.0
- Werkzeug 3.0.1

## License

This project is open source and available for educational purposes.
