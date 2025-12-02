"""
Test OpenAI Fallback when no sources found
"""
import sys
import os
import asyncio

sys.path.insert(0, 'C:/AIAgents/vegan_factchecker/mcp-server')

from dotenv import load_dotenv
load_dotenv()

from research_tools import ResearchAssistant
from claim_analyzer import ClaimAnalyzer
from server import format_verification_response

async def test_fallback():
    print("="*70)
    print("🧪 TESTING OPENAI FALLBACK (0 Sources Found)")
    print("="*70)
    
    research_assistant = ResearchAssistant(
        tavily_api_key=os.getenv("TAVILY_API_KEY"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        semantic_scholar_key=None
    )
    
    claim_analyzer = ClaimAnalyzer(openai_api_key=os.getenv("OPENAI_API_KEY"))
    
    # Use the soy query that returned 0 results
    claim = "77% of soy production goes to livestock feed"
    
    print(f"\n🔍 Testing: {claim}")
    print("⏳ Searching...\n")
    
    analysis = await claim_analyzer.analyze(claim)
    print(f"✓ Category: {analysis['category']}")
    
    evidence = await research_assistant.search_evidence(
        claim=claim,
        category=analysis['category'],
        max_results=5,
        include_counterarguments=True
    )
    
    print(f"✓ Found {len(evidence['sources'])} sources")
    
    if len(evidence['sources']) == 0:
        print("⚠️  No sources found - should trigger OpenAI fallback")
    
    print("\n" + "="*70)
    print("📱 OUTPUT WITH OPENAI FALLBACK:")
    print("="*70 + "\n")
    
    output = format_verification_response(claim, analysis, evidence)
    print(output)
    
    print("\n" + "="*70)
    print("✅ Fallback test complete!")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(test_fallback())