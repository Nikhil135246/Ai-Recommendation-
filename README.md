# 🤖 AI Tool Recommendation System

An intelligent system that uses multiple LLM APIs (GPT-5, Claude Sonnet, DeepSeek) to find the best AI tools for any user query. The system provides relevant AI tool recommendations with direct links and descriptions.

## ✨ Features

- **Multi-LLM Integration**: Uses OpenAI GPT, Anthropic Claude, and DeepSeek APIs
- **Smart Fallback**: Local database backup when APIs are unavailable
- **Web Interface**: Beautiful, responsive web UI
- **Command Line Interface**: Terminal-based interaction
- **Real-time Recommendations**: Instant AI tool suggestions
- **Link Extraction**: Direct links to recommended tools
- **Category-based Search**: Organized tool database

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
Edit the `.env` file and add your API keys:
```env
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

### 3. Run the Application

**Web Interface** (Recommended):
```bash
python app.py
```
Then visit: http://localhost:5000

**Command Line Interface**:
```bash
python main.py
```

## 🎯 Example Queries

- "convert CSV to PDF"
- "generate AI images"
- "write code with AI assistant"
- "edit videos with AI"
- "create music with AI"
- "design logos with AI"
- "translate text to different languages"
- "analyze data with AI"

## 📁 Project Structure

```
python/
├── main.py              # Core recommendation system
├── app.py              # Flask web application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (API keys)
├── README.md          # This file
└── templates/
    └── index.html     # Web interface template
```

## 🔧 API Configuration

The system tries multiple LLM APIs in order:
1. **OpenAI GPT** - Primary choice for comprehensive results
2. **Anthropic Claude** - Backup for detailed analysis
3. **DeepSeek** - Alternative AI model
4. **Local Database** - Fallback when all APIs fail

## 💡 How It Works

1. **User Query**: User enters what they want to accomplish
2. **LLM Processing**: System queries the best available AI model
3. **Tool Extraction**: Parses AI response to extract tool recommendations
4. **Validation**: Validates and formats the results
5. **Display**: Shows tools with links and descriptions

## 🛠️ Available Tool Categories

- **PDF/Document Converters**: CSV to PDF, file format conversion
- **Image Generators**: DALL-E, Midjourney, Stable Diffusion
- **Text Generators**: ChatGPT, Claude, content creation tools
- **Code Assistants**: GitHub Copilot, Tabnine, coding tools
- **Video Editors**: AI-powered video creation and editing
- **Design Tools**: Canva, Adobe Firefly, UI/UX design
- **Music Generators**: AI music composition and creation

## 🔒 Environment Variables

Required API keys in `.env` file:
- `OPENAI_API_KEY`: OpenAI API key for GPT models
- `ANTHROPIC_API_KEY`: Anthropic API key for Claude
- `DEEPSEEK_API_KEY`: DeepSeek API key (optional)
- `GITHUB_TOKEN`: Your GitHub token (already included)

## 🎨 Web Interface Features

- **Responsive Design**: Works on desktop and mobile
- **Example Queries**: Click-to-search common requests
- **Real-time Search**: Instant results with loading indicators
- **Direct Links**: Click to visit recommended tools
- **Error Handling**: User-friendly error messages

## 🚀 Usage Examples

### Web Interface
1. Open http://localhost:5000
2. Enter your query: "convert CSV to PDF"
3. Click "Find Tools"
4. Browse recommended AI tools with links

### Command Line
```bash
python main.py
# Enter query: convert CSV to PDF
# View results with links and descriptions
```

## 🔍 Sample Output

For query: "convert CSV to PDF"
```
✅ Found 4 AI tools for: 'convert CSV to PDF'
--------------------------------------------------
1. 🔧 SmallPDF
   🔗 Link: https://smallpdf.com
   📝 Description: Online PDF converter and editor

2. 🔧 CSV to PDF Converter
   🔗 Link: https://www.convertcsv.com/csv-to-pdf.htm
   📝 Description: Convert CSV files to PDF format
```

## 🤝 Contributing

1. Fork the repository
2. Add new AI tools to the database
3. Improve LLM prompt engineering
4. Enhance the web interface
5. Submit a pull request

## 📝 License

This project is open source. Feel free to use and modify as needed.

## 🔧 Troubleshooting

**API Issues**: 
- Check your API keys in `.env`
- Verify API rate limits
- System falls back to local database

**Installation Issues**:
- Use Python 3.8 or higher
- Install dependencies: `pip install -r requirements.txt`

**Web Interface Issues**:
- Ensure Flask is installed
- Check port 5000 availability
- Run `python app.py` from project directory
