# GitHub Models API Integration Setup

## 🚀 Features Implemented

### 1. **"Find with AI" Button**
- Located next to the regular "Find Tools" button
- Uses GitHub Models API for real-time AI tool discovery
- Powered by GPT models (gpt-4o-mini, gpt-4o, gpt-3.5-turbo)

### 2. **Smart AI Search**
- Returns exactly 5 relevant AI tools per search
- Validates all URLs to ensure they're working links
- Falls back to database search if AI fails
- Optimized prompts to reduce token usage

### 3. **Robust Error Handling**
- Tries multiple models if one fails
- JSON validation and cleaning
- Fallback to local database search
- User-friendly error messages

## 🔧 Setup Instructions

### 1. **GitHub Token Setup**
1. Go to [GitHub Settings → Developer Settings → Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select these scopes:
   - `read:user` (basic access to GitHub Models)
4. Copy the token and add it to your `.env` file:

```env
GITHUB_TOKEN=github_pat_your_new_token_here
```

### 2. **Test the Application**
1. Start the server: `python app.py`
2. Visit: http://localhost:5000
3. Try searching with both buttons:
   - 🔍 **Find Tools**: Searches local database
   - 🤖 **Find with AI**: Uses GitHub Models API

## 🎯 How It Works

### AI Search Process:
1. **User Query** → Optimized prompt with specific requirements
2. **GitHub Models API** → Tries gpt-4o-mini first (cost-effective)
3. **Validation** → Checks for valid URLs and proper JSON format
4. **Response** → Returns 5 curated AI tools with descriptions
5. **Fallback** → Uses local database if AI fails

### Prompt Optimization:
- Requests exactly 5 tools to save tokens
- Asks for real, working URLs only
- Requires specific JSON format
- Temperature set to 0.3 for consistent results

## 📊 API Models Used

1. **gpt-4o-mini** (Primary) - Cost effective, good for simple queries
2. **gpt-4o** (Fallback) - More powerful for complex queries  
3. **gpt-3.5-turbo** (Last resort) - Backup option

## 🔍 Example Queries

Try these with the "Find with AI" button:
- "tools for video editing"
- "AI image generators"
- "convert CSV to PDF"
- "code assistant tools"
- "music generation AI"

## 🛡️ Security Features

- GitHub token stored securely in `.env`
- Input validation and sanitization
- URL validation for all tool links
- Rate limiting through GitHub's API limits

## 🚨 Troubleshooting

### Common Issues:
1. **"AI search failed"** → Check your GitHub token
2. **No results** → Falls back to database search automatically
3. **Invalid JSON** → Tries alternative models automatically

### Token Limits:
- GitHub Models has generous free tier
- Optimized prompts minimize token usage
- Multiple model fallbacks ensure reliability
