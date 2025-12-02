"""
FastAPI wrapper for the Vegan Fact Checker MCP Server
Exposes REST endpoints for the frontend with proper JSON responses
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
import sys

# IMPORTANT: Load environment variables FIRST before importing other modules
from dotenv import load_dotenv
load_dotenv()

# Add parent directory to path to import from server.py
sys.path.insert(0, os.path.dirname(__file__))

# NOW import the components (after env vars are loaded)
from research_tools import ResearchAssistant
from claim_analyzer import ClaimAnalyzer
from citation_formatter import CitationFormatter
from nutrition_calculator import NutritionCalculator

app = FastAPI(
    title="Vegan Fact Checker API",
    description="Research assistant for vegan animal rights activists",
    version="1.0.0"
)

# Initialize components (env vars are already loaded)
research_assistant = ResearchAssistant(
    tavily_api_key=os.getenv("TAVILY_API_KEY"),
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    semantic_scholar_key=os.getenv("SEMANTIC_SCHOLAR_API_KEY")
)

claim_analyzer = ClaimAnalyzer(openai_api_key=os.getenv("OPENAI_API_KEY"))
citation_formatter = CitationFormatter()
nutrition_calc = NutritionCalculator()

# CORS configuration - allows frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class VerifyClaimRequest(BaseModel):
    claim: str
    max_sources: int = 5
    include_counterarguments: bool = True

class SearchRequest(BaseModel):
    topic: str
    year_from: int = 2014
    max_results: int = 10
    focus_area: str = "all"

class AnalyzeRequest(BaseModel):
    claim: str

class NutritionRequest(BaseModel):
    age: int
    gender: str
    weight: float
    nutrient: str

# Health check endpoint
@app.get("/")
@app.get("/health")
async def health_check():
    return {
        "status": "online",
        "service": "Vegan Fact Checker API",
        "version": "1.0.0",
        "mode": "production"
    }

# Main verification endpoint
@app.post("/verify")
async def verify_claim(request: VerifyClaimRequest):
    """
    Verify a claim about veganism with peer-reviewed sources.
    Returns structured JSON with analysis and evidence.
    """
    try:
        print(f"\n🔍 Verifying claim: {request.claim}")
        
        # Step 1: Analyze the claim
        print("📊 Analyzing claim...")
        analysis = await claim_analyzer.analyze(request.claim)
        
        # Step 2: Search for evidence
        print("🔬 Searching for evidence...")
        evidence = await research_assistant.search_evidence(
            claim=request.claim,
            category=analysis["category"],
            max_results=request.max_sources,
            include_counterarguments=request.include_counterarguments
        )
        
        # Step 3: Format citations for sources
        print("📚 Formatting citations...")
        for source in evidence.get("sources", []):
            if "citation_apa" not in source or not source["citation_apa"]:
                citations = citation_formatter.parse_paper_for_citation(source)
                source["citation_apa"] = citations.get("apa", "")
                source["citation_mla"] = citations.get("mla", "")
        
        print(f"✅ Found {len(evidence.get('sources', []))} sources")
        
        # Return properly structured response
        return {
            "claim": request.claim,
            "analysis": analysis,
            "evidence": evidence
        }
        
    except Exception as e:
        print(f"❌ Error in verify_claim: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Search studies endpoint
@app.post("/search")
async def search_studies(request: SearchRequest):
    """
    Search for peer-reviewed studies on a topic.
    """
    try:
        print(f"🔍 Searching studies: {request.topic}")
        
        results = await research_assistant.search_studies(
            topic=request.topic,
            year_from=request.year_from,
            max_results=request.max_results,
            focus_area=request.focus_area
        )
        
        print(f"✅ Found {len(results)} studies")
        return {"success": True, "data": results}
        
    except Exception as e:
        print(f"❌ Error in search_studies: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Analyze claim endpoint
@app.post("/analyze")
async def analyze_claim(request: AnalyzeRequest):
    """
    Analyze a claim to understand its category and evidence needs.
    """
    try:
        print(f"📊 Analyzing: {request.claim}")
        
        result = await claim_analyzer.analyze(request.claim)
        
        print(f"✅ Category: {result.get('category')}")
        return {"success": True, "data": result}
        
    except Exception as e:
        print(f"❌ Error in analyze_claim: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Nutrition calculator endpoint
@app.post("/nutrition-calculate")
async def calculate_nutrition(request: NutritionRequest):
    """
    Calculate personalized nutrition needs.
    
    Example:
    POST /nutrition-calculate
    {
        "age": 27,
        "gender": "female",
        "weight": 50,
        "nutrient": "omega-3"
    }
    """
    try:
        print(f"🥗 Calculating nutrition for {request.gender}, {request.age}yo, {request.weight}kg")
        print(f"   Nutrient: {request.nutrient}")
        
        result = nutrition_calc.generate_recommendation(
            age=request.age,
            gender=request.gender,
            weight=request.weight,
            nutrient=request.nutrient
        )
        
        print(f"✅ Calculated: {result.get('daily_need')} {result.get('unit')}")
        return result
        
    except Exception as e:
        print(f"❌ Error in nutrition calculation: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    
    # Check that API keys are loaded
    openai_key = os.getenv("OPENAI_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")
    
    print(f"""
    ╔═══════════════════════════════════════════════╗
    ║  🌱 Vegan Fact Checker API Server            ║
    ║                                               ║
    ║  Running on: http://localhost:{port}           ║
    ║  Docs: http://localhost:{port}/docs            ║
    ║                                               ║
    ║  API Keys loaded:                             ║
    ║  - OpenAI: {'✅ ' + openai_key[:8] + '...' if openai_key else '❌ NOT FOUND'}
    ║  - Tavily: {'✅ ' + tavily_key[:8] + '...' if tavily_key else '❌ NOT FOUND'}
    ║                                               ║
    ║  Ready to verify claims! 🔍                   ║
    ╚═══════════════════════════════════════════════╝
    """)
    
    if not openai_key or not tavily_key:
        print("⚠️  WARNING: Missing API keys!")
        print("   Please check your .env file in the mcp-server directory")
        print("   Required keys: OPENAI_API_KEY, TAVILY_API_KEY")
        print("")
    
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")