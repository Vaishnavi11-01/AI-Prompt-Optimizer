# AI Prompt Optimizer

A web application that uses Google Gemini AI to optimize and improve your prompts for better AI responses.

## Features

- ✅ **Prompt Optimization**: Uses Google Gemini AI to enhance your prompts for clarity, specificity, and effectiveness
- ✅ **Quality Scoring**: Calculates a quality score (0-100) for prompts based on various criteria (Length, Clarity, Specificity, Context, Format)
- ✅ **Category Detection**: Automatically categorizes prompts (Creative Writing, Code, Business, Education, etc.)
- ✅ **Detailed Dashboard**: Visual display of score breakdown with progress bars and suggestions
- ✅ **History Tracking**: View and manage your previous prompt optimizations with search and filters
- ✅ **Statistics Dashboard**: Track your optimization metrics, category distribution, and monthly usage with interactive charts
- ✅ **PDF Report Generation**: Download professional PDF reports with optimization details
- ✅ **Dark Mode**: Toggle between light and dark themes with preference saved in Local Storage
- ✅ **JSON Export**: Export your entire prompt history as JSON
- ✅ **Responsive Design**: Works seamlessly on desktop and mobile devices

## Project Structure

```
AI-Prompt-Optimizer/
├── app.py                 # Flask application with API routes
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── templates/
│   ├── index.html        # Main optimizer page
│   ├── history.html      # Prompt history page
│   └── stats.html        # Statistics dashboard
├── static/
│   ├── style.css         # Styling with dark mode support
│   ├── script.js         # Frontend JavaScript for optimizer
│   ├── history.js        # Frontend JavaScript for history
│   └── stats.js          # Frontend JavaScript for statistics
├── database/
│   ├── init_db.py        # Database initialization script
│   └── prompts.db        # SQLite database (created on init)
├── utils/
│   ├── score.py          # Prompt scoring algorithm
│   ├── category.py       # Prompt categorization logic
│   ├── gemini.py         # Google Gemini AI integration
│   └── pdf_generator.py  # PDF report generation
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
   - Click "Optimize" to enhance your prompt using Gemini AI
   - View the optimization results with detailed score breakdown
   - Copy the optimized prompt to clipboard
   - Download a PDF report of the optimization
   - Browse your optimization history with search and filters
   - View statistics about your prompts with interactive charts
   - Toggle dark mode for comfortable viewing
   - Export your history as JSON

## API Endpoints

- `POST /optimize` - Optimize a prompt using Gemini AI
- `GET /history` - Get all prompt optimizations
- `GET /history/<id>` - Get specific prompt details
- `DELETE /history/<id>` - Delete a prompt
- `GET /stats` - Get optimization statistics
- `GET /export/json` - Export all prompts as JSON
- `POST /generate-pdf` - Generate PDF report for optimization

## Dependencies

- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- google-generativeai 0.3.2
- PyPDF2 3.0.1
- python-dotenv 1.0.0
- Werkzeug 3.0.1
- reportlab 4.0.7

## License

This project is open source and available for educational purposes.
