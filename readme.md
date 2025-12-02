# Vegan Fact Checker MCP Server

A research assistant MCP server for vegan animal rights activists to verify claims with peer-reviewed sources and credible evidence.

## Features

🔬 **Evidence-Based Fact Checking**
- Searches peer-reviewed journals (Semantic Scholar, PubMed)
- Prioritizes recent studies (last 10 years)
- Includes reports from credible organizations (WHO, FAO, etc.)

📊 **Comprehensive Reports**
- Direct quotes from papers
- Summary of findings
- Confidence scoring (0-10)
- Citations in APA & MLA formats
- Links to full text when available

🎯 **Smart Claim Analysis**
- Automatically categorizes claims (health, environment, ethics, economics)
- Identifies key concepts and evidence needs
- Provides counterarguments for balanced understanding

## Installation

### 1. Prerequisites
- Python 3.10 or higher
- API keys for:
  - OpenAI (required)
  - Tavily (required)
  - Semantic Scholar (optional, recommended)

### 2. Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
```

### 3. Get API Keys

**OpenAI:** https://platform.openai.com/api-keys
**Tavily:** https://tavily.com
**Semantic Scholar:** https://www.semanticscholar.org/product/api (optional)

### 4. Configure MCP in Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "vegan-fact-checker": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {
        "OPENAI_API_KEY": "your-key",
        "TAVILY_API_KEY": "your-key",
        "SEMANTIC_SCHOLAR_API_KEY": "your-key"
      }
    }
  }
}
```

## Available Tools

1. **verify_claim** - Main fact-checking tool
2. **search_studies** - Search academic papers
3. **get_paper_details** - Get detailed paper info
4. **analyze_claim_category** - Analyze claim type
5. **compare_sources** - Compare multiple sources

## Usage Examples

```
"Can you verify: Plants feel pain"
"Search for studies on omega-3 in vegan diets"
"Compare sources on environmental impact of animal agriculture"
```

## Project Structure

```
vegan-fact-checker-server/
├── server.py              # Main MCP server
├── research_tools.py      # Research and search functionality
├── claim_analyzer.py      # Claim categorization
├── citation_formatter.py  # Citation formatting
├── requirements.txt       # Dependencies
├── .env.example          # Environment template
└── README.md             # This file
```

## Common Claims to Test

- "Vegans don't get enough protein"
- "Plants feel pain"
- "Animal agriculture causes climate change"
- "B12 deficiency is common in vegans"
- "Vegan diets are expensive"

## License

MIT License - Use this tool to support evidence-based vegan advocacy!