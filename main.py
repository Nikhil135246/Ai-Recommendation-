import os
import json
import requests
import re
from dotenv import load_dotenv
from typing import List, Dict, Optional
import time

# Load environment variables
load_dotenv()

class AIToolRecommendationSystem:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        
        # GitHub Models API endpoint
        self.github_api_base = "https://models.inference.ai.azure.com"
        
        # AI tools database with categories and descriptions
        self.ai_tools_database = {
            "pdf_converter": [
                {"name": "SmallPDF", "link": "https://smallpdf.com", "description": "Online PDF converter and editor"},
                {"name": "ILovePDF", "link": "https://www.ilovepdf.com", "description": "Free online PDF tools"},
                {"name": "PDF24", "link": "https://tools.pdf24.org", "description": "Free PDF tools and converter"},
                {"name": "Sejda PDF", "link": "https://www.sejda.com", "description": "Online PDF editor and converter"}
            ],
            "csv_tools": [
                {"name": "CSV to PDF Converter", "link": "https://www.convertcsv.com/csv-to-pdf.htm", "description": "Convert CSV files to PDF format"},
                {"name": "Online CSV Tools", "link": "https://onlinecsvtools.com", "description": "Collection of CSV manipulation tools"},
                {"name": "CSV Kit", "link": "https://csvkit.readthedocs.io", "description": "Command-line tools for CSV files"}
            ],
            "image_generator": [
                {"name": "DALL-E 2", "link": "https://openai.com/dall-e-2", "description": "AI image generator by OpenAI"},
                {"name": "Midjourney", "link": "https://midjourney.com", "description": "AI art generator"},
                {"name": "Stable Diffusion", "link": "https://stability.ai", "description": "Open-source AI image generator"},
                {"name": "Leonardo AI", "link": "https://leonardo.ai", "description": "AI-powered creative platform"}
            ],
            "text_generator": [
                {"name": "ChatGPT", "link": "https://chat.openai.com", "description": "Conversational AI by OpenAI"},
                {"name": "Claude", "link": "https://claude.ai", "description": "AI assistant by Anthropic"},
                {"name": "Gemini", "link": "https://gemini.google.com", "description": "Google's AI chatbot"},
                {"name": "Copy.ai", "link": "https://copy.ai", "description": "AI copywriting tool"}
            ],
            "code_assistant": [
                {"name": "GitHub Copilot", "link": "https://github.com/features/copilot", "description": "AI pair programmer"},
                {"name": "Tabnine", "link": "https://www.tabnine.com", "description": "AI code completion"},
                {"name": "CodeWhisperer", "link": "https://aws.amazon.com/codewhisperer", "description": "Amazon's AI coding companion"},
                {"name": "Cursor", "link": "https://cursor.sh", "description": "AI-first code editor"}
            ],
            "video_editor": [
                {"name": "Runway ML", "link": "https://runwayml.com", "description": "AI video editing and generation"},
                {"name": "Synthesia", "link": "https://www.synthesia.io", "description": "AI video generator with avatars"},
                {"name": "Lumen5", "link": "https://lumen5.com", "description": "AI-powered video creation"},
                {"name": "InVideo", "link": "https://invideo.io", "description": "AI video maker"}
            ],
            "design_tools": [
                {"name": "Canva", "link": "https://www.canva.com", "description": "AI-enhanced design platform"},
                {"name": "Adobe Firefly", "link": "https://www.adobe.com/products/firefly.html", "description": "Adobe's generative AI"},
                {"name": "Figma", "link": "https://www.figma.com", "description": "Collaborative design tool with AI features"},
                {"name": "Uizard", "link": "https://uizard.io", "description": "AI-powered design tool"}
            ],
            "music_generator": [
                {"name": "AIVA", "link": "https://www.aiva.ai", "description": "AI music composer"},
                {"name": "Mubert", "link": "https://mubert.com", "description": "AI music generator"},
                {"name": "Soundful", "link": "https://soundful.com", "description": "AI music creation platform"},
                {"name": "Boomy", "link": "https://boomy.com", "description": "Create songs with AI"}
            ]
        }

    def query_github_models(self, query: str, model: str = "gpt-4o-mini") -> Optional[str]:
        """Query GitHub Models API with optimal prompt for AI tool recommendations"""
        if not self.github_token:
            return None
            
        headers = {
            "Authorization": f"Bearer {self.github_token}",
            "Content-Type": "application/json"
        }
        
        # Robust and optimal prompt for consistent results
        prompt = f"""You are an AI tool discovery expert. Find exactly 5 AI tools/services for this query: "{query}"

IMPORTANT REQUIREMENTS:
1. Return ONLY a valid JSON array - no other text
2. Each tool must have real, working links (no placeholders)
3. Verify tools exist and are currently available
4. Focus on popular, established AI tools
5. Include diverse options from different categories

FORMAT (strict JSON only):
[
    {{"name": "Tool Name", "link": "https://actual-working-url.com", "description": "Brief 1-2 sentence description of what it does"}},
    {{"name": "Tool Name 2", "link": "https://another-real-url.com", "description": "Brief 1-2 sentence description"}}
]

Query: {query}

Remember: Return only the JSON array, no explanations or additional text."""
        
        data = {
            "model": model,
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a precise AI tool discovery assistant. Always respond with valid JSON arrays only. Never include explanations or markdown formatting."
                },
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1500,
            "temperature": 0.3
        }
        
        try:
            response = requests.post(
                f"{self.github_api_base}/chat/completions", 
                headers=headers, 
                json=data, 
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                print(f"GitHub Models API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"GitHub Models API error: {e}")
            return None

    def find_with_ai(self, query: str) -> Dict:
        """Find AI tools using GitHub Models API"""
        if not query.strip():
            return {'error': 'Please provide a query', 'tools': [], 'total_found': 0}
        
        print(f"🤖 AI Search initiated for: '{query}'")
        
        if not self.github_token:
            print("❌ No GitHub token found - falling back to database search")
            return self.recommend_tools(query)
        
        # Try different models for best results
        models_to_try = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
        
        for model in models_to_try:
            try:
                print(f"🤖 Querying {model} for: {query}")
                response = self.query_github_models(query, model)
                
                if response:
                    # Clean the response - remove any markdown formatting
                    cleaned_response = response.strip()
                    if cleaned_response.startswith('```json'):
                        cleaned_response = cleaned_response[7:]
                    if cleaned_response.endswith('```'):
                        cleaned_response = cleaned_response[:-3]
                    cleaned_response = cleaned_response.strip()
                    
                    print(f"✅ Raw AI response from {model}: {cleaned_response[:200]}...")
                    
                    # Parse JSON response
                    tools = json.loads(cleaned_response)
                    
                    if isinstance(tools, list) and len(tools) > 0:
                        # Validate and clean tools
                        validated_tools = []
                        for tool in tools[:5]:  # Limit to 5 tools
                            if (isinstance(tool, dict) and 
                                'name' in tool and 
                                'link' in tool and 
                                'description' in tool and
                                tool['link'].startswith(('http://', 'https://'))):
                                validated_tools.append({
                                    'name': tool['name'][:100],  # Limit length
                                    'link': tool['link'],
                                    'description': tool['description'][:200]  # Limit length
                                })
                        
                        if validated_tools:
                            print(f"✅ Successfully found {len(validated_tools)} AI tools using {model}")
                            return {
                                'query': query,
                                'tools': validated_tools,
                                'total_found': len(validated_tools),
                                'source': f'AI-powered by {model}'
                            }
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing error with {model}: {e}")
                continue
            except Exception as e:
                print(f"❌ Error with {model}: {e}")
                continue
        
        # Fallback to database search if AI fails
        print("🔄 AI search failed, falling back to database search")
        return self.recommend_tools(query)

    def get_best_llm_response(self, query: str) -> str:
        """Try different LLM APIs and return the best response"""
        responses = []
        
        # Try OpenAI GPT
        if self.openai_api_key:
            try:
                gpt_response = self.query_openai(query)
                if gpt_response:
                    responses.append(("OpenAI GPT", gpt_response))
            except Exception as e:
                print(f"OpenAI error: {e}")
        
        # Try Anthropic Claude
        if self.anthropic_api_key:
            try:
                claude_response = self.query_anthropic(query)
                if claude_response:
                    responses.append(("Claude", claude_response))
            except Exception as e:
                print(f"Anthropic error: {e}")
        
        # Try DeepSeek (if available)
        if self.deepseek_api_key:
            try:
                deepseek_response = self.query_deepseek(query)
                if deepseek_response:
                    responses.append(("DeepSeek", deepseek_response))
            except Exception as e:
                print(f"DeepSeek error: {e}")
        
        # Return the first successful response
        if responses:
            return responses[0][1]
        else:
            return self.fallback_response(query)

    def query_openai(self, query: str) -> Optional[str]:
        """Query OpenAI GPT API"""
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""Find AI tools for this query: "{query}"
        
        Respond with a JSON list of tools in this exact format:
        [
            {{"name": "Tool Name", "link": "https://example.com", "description": "Brief description"}},
            {{"name": "Tool Name 2", "link": "https://example2.com", "description": "Brief description"}}
        ]
        
        Focus on actual AI tools and services that exist and are relevant to the query."""
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000,
            "temperature": 0.3
        }
        
        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", 
                                   headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return None

    def query_anthropic(self, query: str) -> Optional[str]:
        """Query Anthropic Claude API"""
        headers = {
            "x-api-key": self.anthropic_api_key,
            "content-type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        prompt = f"""Find AI tools for this query: "{query}"
        
        Respond with a JSON list of tools in this exact format:
        [
            {{"name": "Tool Name", "link": "https://example.com", "description": "Brief description"}},
            {{"name": "Tool Name 2", "link": "https://example2.com", "description": "Brief description"}}
        ]
        
        Focus on actual AI tools and services that exist and are relevant to the query."""
        
        data = {
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        try:
            response = requests.post("https://api.anthropic.com/v1/messages", 
                                   headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                return response.json()["content"][0]["text"]
        except Exception as e:
            print(f"Anthropic API error: {e}")
            return None

    def query_deepseek(self, query: str) -> Optional[str]:
        """Query DeepSeek API (placeholder - adjust URL based on actual API)"""
        # Note: This is a placeholder. Adjust the URL and headers based on actual DeepSeek API
        headers = {
            "Authorization": f"Bearer {self.deepseek_api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""Find AI tools for this query: "{query}"
        
        Respond with a JSON list of tools in this exact format:
        [
            {{"name": "Tool Name", "link": "https://example.com", "description": "Brief description"}},
            {{"name": "Tool Name 2", "link": "https://example2.com", "description": "Brief description"}}
        ]
        
        Focus on actual AI tools and services that exist and are relevant to the query."""
        
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }
        
        try:
            response = requests.post("https://api.deepseek.com/v1/chat/completions", 
                                   headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"DeepSeek API error: {e}")
            return None

    def fallback_response(self, query: str) -> str:
        """Fallback response using local database when APIs fail"""
        query_lower = query.lower()
        relevant_tools = []
        
        # Search through local database
        for category, tools in self.ai_tools_database.items():
            if any(keyword in query_lower for keyword in category.split('_')):
                relevant_tools.extend(tools)
        
        # Generic search for common keywords
        if not relevant_tools:
            if any(word in query_lower for word in ['convert', 'csv', 'pdf', 'file']):
                relevant_tools.extend(self.ai_tools_database.get('pdf_converter', []))
                relevant_tools.extend(self.ai_tools_database.get('csv_tools', []))
            elif any(word in query_lower for word in ['image', 'picture', 'photo', 'generate']):
                relevant_tools.extend(self.ai_tools_database.get('image_generator', []))
            elif any(word in query_lower for word in ['text', 'write', 'content']):
                relevant_tools.extend(self.ai_tools_database.get('text_generator', []))
            elif any(word in query_lower for word in ['code', 'programming', 'developer']):
                relevant_tools.extend(self.ai_tools_database.get('code_assistant', []))
            elif any(word in query_lower for word in ['video', 'edit', 'movie']):
                relevant_tools.extend(self.ai_tools_database.get('video_editor', []))
            elif any(word in query_lower for word in ['design', 'ui', 'graphic']):
                relevant_tools.extend(self.ai_tools_database.get('design_tools', []))
            elif any(word in query_lower for word in ['music', 'audio', 'sound']):
                relevant_tools.extend(self.ai_tools_database.get('music_generator', []))
        
        # If still no results, return general AI tools
        if not relevant_tools:
            relevant_tools = self.ai_tools_database.get('text_generator', [])
        
        return json.dumps(relevant_tools[:5])  # Limit to top 5 results

    def parse_llm_response(self, response: str) -> List[Dict]:
        """Parse LLM response to extract tools"""
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                tools = json.loads(json_str)
                return tools
            else:
                # If no JSON found, try to parse manually
                return self.manual_parse_response(response)
        except Exception as e:
            print(f"Parsing error: {e}")
            return []

    def manual_parse_response(self, response: str) -> List[Dict]:
        """Manually parse response if JSON parsing fails"""
        tools = []
        lines = response.split('\n')
        
        current_tool = {}
        for line in lines:
            if 'name:' in line.lower() or 'tool:' in line.lower():
                if current_tool:
                    tools.append(current_tool)
                    current_tool = {}
                current_tool['name'] = line.split(':', 1)[1].strip()
            elif 'link:' in line.lower() or 'url:' in line.lower():
                current_tool['link'] = line.split(':', 1)[1].strip()
            elif 'description:' in line.lower():
                current_tool['description'] = line.split(':', 1)[1].strip()
        
        if current_tool:
            tools.append(current_tool)
        
        return tools

    def recommend_tools(self, query: str) -> Dict:
        """Main function to get AI tool recommendations"""
        print(f"🔍 Searching for AI tools related to: '{query}'")
        print("⏳ Please wait while I query the best AI models...")
        
        # Get response from the best available LLM
        llm_response = self.get_best_llm_response(query)
        
        # Parse the response
        tools = self.parse_llm_response(llm_response)
        
        # Validate and clean the results
        validated_tools = []
        for tool in tools:
            if isinstance(tool, dict) and all(key in tool for key in ['name', 'link', 'description']):
                validated_tools.append({
                    'name': tool['name'],
                    'link': tool['link'],
                    'description': tool['description'][:100] + '...' if len(tool['description']) > 100 else tool['description']
                })
        
        return {
            'query': query,
            'tools': validated_tools,
            'total_found': len(validated_tools)
        }

def main():
    """Main function to run the AI recommendation system"""
    print("🤖 AI Tool Recommendation System")
    print("=" * 50)
    
    system = AIToolRecommendationSystem()
    
    while True:
        print("\n" + "=" * 50)
        query = input("Enter your query (or 'quit' to exit): ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not query:
            print("❌ Please enter a valid query.")
            continue
        
        try:
            # Get recommendations
            result = system.recommend_tools(query)
            
            print(f"\n✅ Found {result['total_found']} AI tools for: '{result['query']}'")
            print("-" * 50)
            
            if result['tools']:
                for i, tool in enumerate(result['tools'], 1):
                    print(f"{i}. 🔧 {tool['name']}")
                    print(f"   🔗 Link: {tool['link']}")
                    print(f"   📝 Description: {tool['description']}")
                    print()
            else:
                print("❌ No relevant tools found. Please try a different query.")
        
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please try again with a different query.")

if __name__ == "__main__":
    main()