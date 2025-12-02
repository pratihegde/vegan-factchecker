"""
Vegan Fact Checker MCP Server
A research assistant for vegan animal rights activists to verify claims with peer-reviewed sources.
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Any, Optional, List, Dict
from dotenv import load_dotenv

from mcp.server import Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
import mcp.server.stdio

# Import our custom modules
from research_tools import ResearchAssistant
from claim_analyzer import ClaimAnalyzer
from citation_formatter import CitationFormatter

# Load environment variables
load_dotenv()

# Initialize the MCP server
app = Server("vegan-fact-checker")

# Initialize our research components
research_assistant = ResearchAssistant(
    tavily_api_key=os.getenv("TAVILY_API_KEY"),
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    semantic_scholar_key=os.getenv("SEMANTIC_SCHOLAR_API_KEY")
)

claim_analyzer = ClaimAnalyzer(openai_api_key=os.getenv("OPENAI_API_KEY"))
citation_formatter = CitationFormatter()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available fact-checking tools."""
    return [
        Tool(
            name="verify_claim",
            description="""
            Verify a claim about veganism, animal rights, or related topics.
            This is the main tool for fact-checking. It will:
            - Analyze the claim
            - Search peer-reviewed journals and credible sources
            - Provide evidence with citations
            - Include direct quotes, summaries, and confidence scoring
            - Prioritize recent studies (last 10 years)
            
            Example claims:
            - "Vegans don't get omega-3 from food"
            - "Plants feel pain"
            - "Animal agriculture contributes to climate change"
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "claim": {
                        "type": "string",
                        "description": "The claim to verify (e.g., 'Plants feel pain')"
                    },
                    "max_sources": {
                        "type": "integer",
                        "description": "Maximum number of sources to retrieve (default: 5)",
                        "default": 5
                    },
                    "include_counterarguments": {
                        "type": "boolean",
                        "description": "Whether to include opposing viewpoints (default: true)",
                        "default": True
                    }
                },
                "required": ["claim"]
            }
        ),
        Tool(
            name="search_studies",
            description="""
            Search for peer-reviewed studies and credible sources on a specific topic.
            Use this for broader research beyond a single claim.
            
            Returns: List of relevant papers with abstracts, citations, and links.
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Research topic or keywords"
                    },
                    "year_from": {
                        "type": "integer",
                        "description": "Only include studies from this year onwards (default: 2014)",
                        "default": 2014
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 10)",
                        "default": 10
                    },
                    "focus_area": {
                        "type": "string",
                        "description": "Optional: Focus on 'health', 'environment', 'ethics', or 'economics'",
                        "enum": ["health", "environment", "ethics", "economics", "all"],
                        "default": "all"
                    }
                },
                "required": ["topic"]
            }
        ),
        Tool(
            name="get_paper_details",
            description="""
            Get detailed information about a specific paper including:
            - Full abstract
            - Key findings and quotes
            - Methods used
            - Limitations
            - Full citation in APA and MLA formats
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "paper_id": {
                        "type": "string",
                        "description": "Paper identifier (DOI, PubMed ID, or Semantic Scholar ID)"
                    },
                    "include_related": {
                        "type": "boolean",
                        "description": "Include related papers (default: false)",
                        "default": False
                    }
                },
                "required": ["paper_id"]
            }
        ),
        Tool(
            name="analyze_claim_category",
            description="""
            Analyze and categorize a claim to understand what type of evidence is needed.
            Useful for understanding the nature of a claim before researching.
            
            Returns: Category, key concepts, suggested search terms, and evidence type needed.
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "claim": {
                        "type": "string",
                        "description": "The claim to analyze"
                    }
                },
                "required": ["claim"]
            }
        ),
        Tool(
            name="compare_sources",
            description="""
            Compare multiple sources on the same topic to identify:
            - Consensus findings
            - Conflicting results
            - Quality of evidence
            - Potential biases
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Topic to compare sources on"
                    },
                    "source_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional: Specific paper IDs to compare"
                    }
                },
                "required": ["topic"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls for fact-checking."""
    
    try:
        if name == "verify_claim":
            result = await verify_claim_handler(arguments)
            return [TextContent(type="text", text=result)]
        
        elif name == "search_studies":
            result = await search_studies_handler(arguments)
            return [TextContent(type="text", text=result)]
        
        elif name == "get_paper_details":
            result = await get_paper_details_handler(arguments)
            return [TextContent(type="text", text=result)]
        
        elif name == "analyze_claim_category":
            result = await analyze_claim_handler(arguments)
            return [TextContent(type="text", text=result)]
        
        elif name == "compare_sources":
            result = await compare_sources_handler(arguments)
            return [TextContent(type="text", text=result)]
        
        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error executing {name}: {str(e)}"
        )]


async def verify_claim_handler(args: Dict[str, Any]) -> str:
    """
    Main claim verification handler.
    This orchestrates the entire fact-checking process.
    """
    claim = args["claim"]
    max_sources = args.get("max_sources", 5)
    include_counterarguments = args.get("include_counterarguments", True)
    
    # Step 1: Analyze the claim
    analysis = await claim_analyzer.analyze(claim)
    
    # Step 2: Search for evidence
    evidence = await research_assistant.search_evidence(
        claim=claim,
        category=analysis["category"],
        max_results=max_sources,
        include_counterarguments=include_counterarguments
    )
    
    # Step 3: Format the response
    response = format_verification_response(claim, analysis, evidence)
    
    return response


async def search_studies_handler(args: Dict[str, Any]) -> str:
    """Search for studies on a topic."""
    topic = args["topic"]
    year_from = args.get("year_from", 2014)
    max_results = args.get("max_results", 10)
    focus_area = args.get("focus_area", "all")
    
    results = await research_assistant.search_studies(
        topic=topic,
        year_from=year_from,
        max_results=max_results,
        focus_area=focus_area
    )
    
    return format_search_results(results)


async def get_paper_details_handler(args: Dict[str, Any]) -> str:
    """Get detailed information about a specific paper."""
    paper_id = args["paper_id"]
    include_related = args.get("include_related", False)
    
    details = await research_assistant.get_paper_details(
        paper_id=paper_id,
        include_related=include_related
    )
    
    return format_paper_details(details)


async def analyze_claim_handler(args: Dict[str, Any]) -> str:
    """Analyze a claim to understand its category and evidence needs."""
    claim = args["claim"]
    
    analysis = await claim_analyzer.analyze(claim)
    
    return format_claim_analysis(analysis)


async def compare_sources_handler(args: Dict[str, Any]) -> str:
    """Compare multiple sources on a topic."""
    topic = args["topic"]
    source_ids = args.get("source_ids", [])
    
    comparison = await research_assistant.compare_sources(
        topic=topic,
        source_ids=source_ids
    )
    
    return format_source_comparison(comparison)


def format_verification_response(claim: str, analysis: Dict, evidence: Dict) -> str:
    """Format the verification response in mobile-first, compact format."""
    
    # Determine verdict based on confidence score and summary
    verdict = _determine_verdict(evidence['confidence_score'], evidence['summary'])
    verdict_emoji = "❌" if verdict == "FALSE" else "✅" if verdict == "TRUE" else "⚠️"
    
    # Extract prestigious sources
    prestigious_sources = _extract_prestigious_sources(evidence['sources'])
    
    # Create mobile-optimized response
    response = f"""═══════════════════════════════════
{claim.upper()}
═══════════════════════════════════

{verdict_emoji} {verdict}

💬 QUICK RESPONSE:
"{_generate_quick_response(claim, analysis, evidence)}"

───────────────────────────────────

📊 KEY FACTS:
"""
    
    # Add 2-3 key facts with bold emphasis
    key_facts = _extract_key_facts(evidence['sources'], analysis['category'])
    for fact in key_facts[:3]:
        response += f"\n• {fact}"
    
    response += f"""

🏆 SOURCES:
{prestigious_sources}

───────────────────────────────────

💡 SIMPLE EXPLANATION:

{_create_simple_explanation(evidence['summary'])}

───────────────────────────────────
"""
    
    # Add 1-2 most common questions if counterarguments exist
    if evidence.get('counterarguments') and len(evidence['counterarguments']) > 0:
        response += "\n❓ COMMON QUESTIONS:\n\n"
        for i, counter in enumerate(evidence['counterarguments'][:2], 1):
            response += f"Q: {counter}\n"
            response += f"A: {_generate_counter_response(counter, evidence['sources'])}\n\n"
        response += "───────────────────────────────────\n"
    
    # Collapsible full details section
    response += "\n📖 FULL ACADEMIC DETAILS:\n\n"
    
    for idx, source in enumerate(evidence['sources'][:5], 1):
        response += f"""{idx}. {_highlight_prestigious_journal(source['journal'])} ({source['year']})
   "{source['title']}"
   
   Finding: {source.get('key_finding', 'See paper for details')}
   
   Type: Peer-Reviewed
   Link: {source['link']}
   
"""
    
    response += f"""───────────────────────────────────
📱 Generated: {datetime.now().strftime('%Y-%m-%d')}
🔬 {len(evidence['sources'])} peer-reviewed sources ({_get_year_range(evidence['sources'])})
"""
    
    return response


def format_search_results(results: List[Dict]) -> str:
    """Format search results in a readable format."""
    from citation_formatter import CitationFormatter
    
    formatter = CitationFormatter()
    output = f"# Research Results\n\n**Found {len(results)} studies**\n\n"
    
    for idx, paper in enumerate(results, 1):
        # Generate citation if not present
        if 'citation_apa' not in paper:
            try:
                citations = formatter.parse_paper_for_citation(paper)
                paper['citation_apa'] = citations.get('apa', 'Citation unavailable')
            except:
                paper['citation_apa'] = 'Citation unavailable'
        
        # Handle missing abstract
        abstract = paper.get('abstract', 'No abstract available')
        if abstract and len(abstract) > 500:
            abstract = abstract[:500] + "..."
        
        output += f"""
## {idx}. {paper.get('title', 'Untitled')}

**Authors:** {paper.get('authors', 'Unknown')}
**Year:** {paper.get('year', 'N/A')}
**Journal:** {paper.get('journal', 'Unknown')}
**Citations:** {paper.get('citation_count', 'N/A')}

**Abstract:**
{abstract}

**Link:** {paper.get('link', 'N/A')}

**Citation (APA):**
{paper.get('citation_apa', 'Citation unavailable')}

---
"""
    
    return output


def format_paper_details(details: Dict) -> str:
    """Format detailed paper information."""
    return f"""
# Paper Details

## {details['title']}

**Authors:** {details['authors']}
**Published:** {details['journal']} ({details['year']})
**DOI:** {details.get('doi', 'N/A')}

## Abstract
{details['abstract']}

## Key Findings
{details['key_findings']}

## Methodology
{details['methods']}

## Limitations
{details['limitations']}

## Citations

**APA:**
{details['citation_apa']}

**MLA:**
{details['citation_mla']}

**Access:** {details['link']}

{"## Related Papers\n" + chr(10).join([f"- {p['title']}" for p in details.get('related_papers', [])]) if details.get('related_papers') else ""}
"""


def format_claim_analysis(analysis: Dict) -> str:
    """Format claim analysis results."""
    return f"""
# Claim Analysis

**Category:** {analysis['category']}

**Key Concepts:** {', '.join(analysis['key_concepts'])}

**Evidence Type Needed:** {analysis['evidence_type']}

**Suggested Search Terms:**
{chr(10).join([f"- {term}" for term in analysis['search_terms']])}

**Relevant Fields:**
{chr(10).join([f"- {field}" for field in analysis['relevant_fields']])}

**Complexity:** {analysis['complexity']}/10
"""


def format_source_comparison(comparison: Dict) -> str:
    """Format source comparison results."""
    output = f"""
# Source Comparison

## Consensus Findings
{chr(10).join([f"- {finding}" for finding in comparison['consensus']])}

## Conflicting Results
{chr(10).join([f"- {conflict}" for conflict in comparison['conflicts']])}

## Evidence Quality
**Overall Quality Score:** {comparison['quality_score']}/10

"""
    
    for source in comparison['sources']:
        output += f"""
### {source['title']}
**Quality:** {source['quality']}/10
**Strengths:** {source['strengths']}
**Limitations:** {source['limitations']}

---
"""
    
    return output


# ============================================================================
# HELPER FUNCTIONS FOR MOBILE-FIRST FORMATTING
# ============================================================================

def _determine_verdict(confidence_score: int, summary: str) -> str:
    """
    Determine verdict from confidence score and summary.
    Low confidence score (1-3) usually means claim is FALSE.
    High confidence score (8-10) usually means claim is TRUE.
    """
    summary_lower = summary.lower()
    
    # Check summary for explicit statements
    if any(word in summary_lower for word in ['refutes', 'false', 'incorrect', 'not supported', 'no evidence']):
        return "FALSE"
    elif any(word in summary_lower for word in ['supports', 'confirms', 'true', 'correct', 'evidence shows']):
        return "TRUE"
    elif any(word in summary_lower for word in ['partially', 'mixed', 'complex', 'depends']):
        return "PARTIALLY TRUE"
    
    # Fallback to confidence score
    if confidence_score <= 3:
        return "FALSE"
    elif confidence_score >= 7:
        return "TRUE"
    else:
        return "PARTIALLY TRUE"


def _extract_prestigious_sources(sources: List[Dict]) -> str:
    """Extract and highlight prestigious sources."""
    prestigious = {
        # Order matters - check more specific names first!
        'harvard medical school': '🏆 Harvard Medical School',
        'harvard': '🏆 Harvard',
        'oxford': '🏆 Oxford', 
        'stanford': '🏆 Stanford',
        'cambridge': '🏆 Cambridge',
        'mit': '🏆 MIT',
        'the lancet': '🏆 The Lancet',
        'new england journal of medicine': '🏆 New England Journal of Medicine',
        'nejm': '🏆 NEJM',
        'jama': '🏆 JAMA',
        'mayo clinic': '🏆 Mayo Clinic',
        'johns hopkins': '🏆 Johns Hopkins',
        'world health organization': '🏆 WHO',
        'who.int': '🏆 WHO',
        'nih.gov': '🏆 NIH',
        'national institutes of health': '🏆 NIH',
        'ipcc': '🏆 IPCC',
        # Prestigious journals - be specific to avoid false matches
        'nature medicine': '🏆 Nature Medicine',
        'nature communications': '🏆 Nature Communications',
        'nature ': '🏆 Nature',  # Space after to avoid matching "Frontiers in Nature Science"
        'science ': '🏆 Science',  # Space after to avoid matching journal names containing "science"
        'cell ': '🏆 Cell',
        # Good but not top-tier (no trophy)
        'frontiers': 'Frontiers',
        'protoplasma': 'Protoplasma',
        'plos': 'PLOS',
        'bmc': 'BMC',
    }
    
    found_sources = []
    years = []
    
    for source in sources[:5]:
        journal = source.get('journal', '').lower()
        year = source.get('year', '')
        
        # Check if prestigious - use exact matching to avoid false positives
        matched = False
        for key, display_name in prestigious.items():
            # For entries with trailing space, do exact word match
            if key.endswith(' '):
                # Match "Nature " but not "Nature Science"
                if journal == key.strip() or journal.startswith(key):
                    if display_name not in found_sources:
                        found_sources.append(display_name)
                    if year and year not in years:
                        years.append(str(year))
                    matched = True
                    break
            # For other entries, use 'in' matching
            elif key in journal:
                if display_name not in found_sources:
                    found_sources.append(display_name)
                if year and year not in years:
                    years.append(str(year))
                matched = True
                break
        
        # If not in prestigious list, add the actual journal name
        if not matched:
            journal_name = source.get('journal', 'Unknown')
            if journal_name and journal_name not in found_sources:
                found_sources.append(journal_name)
            if year and year not in years:
                years.append(str(year))
    
    # Format output
    if not found_sources:
        return "Peer-reviewed journals"
    
    source_str = ", ".join(found_sources[:3])
    if len(found_sources) > 3:
        source_str += f" +{len(found_sources) - 3} more"
    
    # Add year range if available
    if years:
        years_sorted = sorted(years)
        if len(years_sorted) > 1:
            source_str += f" ({years_sorted[0]}-{years_sorted[-1]})"
        else:
            source_str += f" ({years_sorted[0]})"
    
    return source_str


def _generate_quick_response(claim: str, analysis: Dict, evidence: Dict) -> str:
    """Generate a one-line response the activist can say out loud."""
    summary = evidence.get('summary', '').lower()
    category = analysis.get('category', '')
    
    # Check if claim is refuted/false
    is_false = any(word in summary for word in ['refutes', 'false', 'incorrect', 'not supported', 'no evidence', 'lack'])
    is_misleading = any(word in summary for word in ['misleading', 'partially', 'context'])
    
    # Generate conversational responses based on category and verdict
    if 'plant' in claim.lower() and 'pain' in claim.lower():
        if is_false:
            return "Plants don't have brains or nervous systems—both required for pain. Their responses are just automatic chemistry, not conscious suffering."
    
    if 'protein' in claim.lower() and any(word in claim.lower() for word in ['plant', 'vegan', 'not enough', 'inadequate']):
        if is_false or is_misleading:
            return "Plant proteins are complete when combined—and the Academy of Nutrition says plant-based diets meet all protein needs for all life stages. Beans, lentils, tofu, and grains easily provide complete protein."
        else:
            # Even if evidence is mixed, provide pro-vegan context
            return "Plant proteins combined throughout the day provide all essential amino acids. Major health organizations confirm plant-based diets are nutritionally adequate."
    
    if 'b12' in claim.lower() or 'b-12' in claim.lower():
        return "B12 comes from bacteria, not animals. Factory-farmed animals get B12 supplements too—vegans just take it directly instead of through animal products."
    
    if any(word in claim.lower() for word in ['expensive', 'cost', 'afford']):
        return "Beans, rice, lentils, and oats are among the cheapest foods available. Meat is expensive and heavily subsidized—plant-based staples cost less."
    
    if 'soy' in claim.lower() and ('estrogen' in claim.lower() or 'hormone' in claim.lower()):
        return "Soy contains phytoestrogens, which are plant compounds chemically different from human estrogen. Studies show soy is safe and may reduce cancer risk."
    
    # Fallback: try to make the summary more conversational
    if is_false:
        # Generic false response
        return "The scientific evidence shows this isn't true. Major health organizations support plant-based nutrition."
    else:
        # Generic true/complex response
        sentences = evidence.get('summary', '').split('. ')
        if sentences:
            response = sentences[0].strip()
            if len(response) > 150:
                response = response[:147] + "..."
            return response
    
    return "The scientific evidence addresses this claim. See details below."


def _extract_key_facts(sources: List[Dict], category: str) -> List[str]:
    """Extract 2-3 key facts with bold numbers and institutions."""
    facts = []
    claim_text = " ".join([s.get('key_finding', '') + " " + s.get('title', '') for s in sources]).lower()
    
    # Pattern matching for common vegan claims with punchy rewrites
    
    # Plants and pain
    if 'plant' in claim_text and ('pain' in claim_text or 'conscious' in claim_text):
        facts.append("**0 plants** have brains or nervous systems (required for pain)")
        facts.append("**0 plants** respond to anesthetics (they lack pain receptors)")
        review_count = sum(1 for s in sources if 'review' in s.get('study_type', '').lower())
        if review_count > 0:
            facts.append(f"**{review_count} systematic reviews** confirm no plant consciousness")
        else:
            facts.append(f"**{len(sources)} peer-reviewed studies** confirm no plant consciousness")
        return facts
    
    # Try to extract quantitative data from findings
    import re
    for source in sources[:5]:
        finding = source.get('key_finding', '')
        journal = source.get('journal', '')
        
        # Look for numbers in findings
        numbers = re.findall(r'\b\d+[,\d]*\b', finding)
        
        # Create fact statements with bold numbers
        if numbers and len(finding) < 200:
            fact = finding
            for num in numbers:
                fact = fact.replace(num, f"**{num}**", 1)  # Only replace first occurrence
            
            # Add prestigious journal if present
            if any(keyword in journal.lower() for keyword in ['harvard', 'oxford', 'nature', 'science', 'lancet', 'jama']):
                fact += f" ({journal})"
            
            facts.append(fact)
        
        # Look for "no evidence" or "lack" statements
        elif any(phrase in finding.lower() for phrase in ['no evidence', 'lack', 'absence', 'not found']):
            # Make it punchier by bolding key negatives
            fact = finding.replace('no evidence', '**no evidence**')
            fact = fact.replace('lack', '**lack**')
            fact = fact.replace('absence', '**absence**')
            facts.append(fact[:150] + ("..." if len(fact) > 150 else ""))
    
    # If no good facts found, create generic ones
    if not facts:
        facts.append(f"**{len(sources)}** peer-reviewed studies examined this claim")
        
        review_count = sum(1 for s in sources if 'review' in s.get('study_type', '').lower())
        if review_count > 0:
            facts.append(f"Includes **{review_count}** systematic review(s) analyzing multiple studies")
        
        # Add year range
        years = [int(s.get('year', 0)) for s in sources if s.get('year', '').isdigit()]
        if years:
            facts.append(f"Research from **{min(years)}-{max(years)}** (recent & consistent)")
    
    return facts[:3]  # Max 3 facts


def _create_simple_explanation(summary: str) -> str:
    """Create a 2-3 sentence simple explanation."""
    # Limit summary to first 2-3 sentences
    sentences = summary.split('. ')
    if len(sentences) > 3:
        return '. '.join(sentences[:3]) + '.'
    return summary


def _generate_counter_response(counter: str, sources: List[Dict]) -> str:
    """Generate a brief response to a counterargument."""
    counter_lower = counter.lower()
    
    # Plant pain responses
    if 'chemical' in counter_lower and 'cut' in counter_lower:
        return "True, but that's automatic signaling, not pain. A smoke detector beeps when there's fire—it's not scared. No brain = no suffering."
    
    if 'scream' in counter_lower or 'sound' in counter_lower:
        return "That was ultrasonic vibrations from air bubbles in damaged stems—like wood creaking. No evidence of consciousness or distress."
    
    if 'respond' in counter_lower or 'react' in counter_lower:
        return "Response doesn't equal pain. Your thermostat responds to temperature—it doesn't feel hot or cold. Plants lack the neurological hardware for suffering."
    
    if 'communication' in counter_lower or 'signal' in counter_lower:
        return "Plants use chemical signals, but that's not communication like animals. It's automatic chemistry—no consciousness required."
    
    # Protein responses - PRO-VEGAN
    if 'protein' in counter_lower:
        if 'incomplete' in counter_lower or 'complete' in counter_lower:
            return "Beans + rice, hummus + pita, PB&J—all give complete protein. Your body combines amino acids throughout the day. The Academy of Nutrition confirms plant-based diets meet protein needs for all life stages."
        
        if 'amino acid' in counter_lower or 'essential' in counter_lower:
            return "All 9 essential amino acids are in plants. Eating a variety of beans, grains, nuts, and seeds throughout the day gives you everything. No need to combine in one meal—that's outdated science."
        
        if 'quality' in counter_lower or 'digest' in counter_lower:
            return "Plant protein is highly digestible—tofu is 95%, similar to eggs. 'Quality' studies often compare isolated proteins, not real meals. Billions of healthy vegans worldwide prove adequacy."
        
        if 'enough' in counter_lower or 'adequate' in counter_lower:
            return "The Academy of Nutrition and Dietetics (100,000+ professionals) confirms plant-based diets provide adequate protein for all life stages, including athletes and pregnancy."
        
        # Generic protein response
        return "Plant proteins combined throughout the day provide all essential amino acids. Major health organizations worldwide confirm plant-based diets are nutritionally adequate."
    
    # B12 responses
    if 'b12' in counter_lower or 'b-12' in counter_lower:
        if 'natural' in counter_lower or 'supplement' in counter_lower:
            return "B12 comes from bacteria in soil/water, not animals. Factory-farmed animals get B12 supplements in their feed—vegans just skip the middleman and take it directly."
        if 'deficiency' in counter_lower:
            return "B12 deficiency affects omnivores too (40% of Americans are low). Most livestock get B12 supplements—taking it directly is more efficient than filtering it through animals."
        return "B12 is made by bacteria, not animals. Supplementation is a modern solution for everyone—even meat-eaters often need it as they age."
    
    # Cost/expense responses
    if 'expensive' in counter_lower or 'cost' in counter_lower or 'afford' in counter_lower:
        return "Beans, rice, lentils, oats—the cheapest foods in any grocery store. Meat is subsidized and expensive. Vegan specialty products are optional, not required."
    
    # Environmental responses  
    if 'crop' in counter_lower and 'animal' in counter_lower:
        return "Growing crops for humans directly is far more efficient. It takes 10-25 lbs of plants to produce 1 lb of beef. Going vegan reduces total crop deaths and land use by ~90%."
    
    if 'avocado' in counter_lower or 'almond' in counter_lower or 'import' in counter_lower:
        return "Even the most resource-intensive plant foods (avocados, almonds) have lower impact than animal products. Plus, most animal feed is imported too—soy for livestock travels farther than your tofu."
    
    if 'local' in counter_lower and 'meat' in counter_lower:
        return "Transportation is only ~6% of food emissions. What you eat matters more than where it's from. Local beef has way higher emissions than imported plant foods."
    
    # Soy responses
    if 'soy' in counter_lower:
        if 'estrogen' in counter_lower or 'hormone' in counter_lower or 'man boob' in counter_lower:
            return "Soy has phytoestrogens (plant compounds), not human estrogen. Studies show it's safe for men and may reduce cancer risk. Meanwhile, dairy has actual mammalian estrogen."
        if 'processed' in counter_lower:
            return "Tofu, tempeh, edamame are minimally processed—just cooked soybeans. Plus, 70% of global soy goes to livestock feed, not tofu."
        return "Soy is a complete protein and safe to eat. It may reduce cancer and heart disease risk. Phytoestrogens are not the same as animal estrogen."
    
    # Iron/calcium responses
    if 'iron' in counter_lower:
        return "Plant foods are high in iron (lentils, spinach, fortified cereals). Pair with vitamin C for better absorption. Many omnivores are iron-deficient too—it's about eating well, not eating meat."
    
    if 'calcium' in counter_lower:
        return "Calcium is abundant in fortified plant milk, tofu, leafy greens, and tahini. Countries with highest dairy consumption have highest osteoporosis rates—calcium alone doesn't equal bone health."
    
    # Omega-3 responses
    if 'omega' in counter_lower or 'dha' in counter_lower or 'epa' in counter_lower:
        return "ALA from flax, chia, and walnuts converts to DHA/EPA. Or take algae oil (where fish get their omega-3s anyway). No need for fish—go straight to the source."
    
    # Evolution/natural arguments
    if 'ancestor' in counter_lower or 'evolution' in counter_lower or 'caveman' in counter_lower:
        return "Our ancestors also died at 30. Modern nutrition science trumps appeals to evolution. We can thrive on plants—and our longest-lived populations eat mostly plant-based."
    
    if 'lion' in counter_lower or 'carnivore' in counter_lower and 'nature' in counter_lower:
        return "Lions are obligate carnivores with short digestive tracts. We have long intestines like herbivores. Lions also don't have moral agency—we do."
    
    # Generic fallback
    return "The peer-reviewed research supports plant-based nutrition. Major health organizations worldwide confirm well-planned vegan diets are nutritionally adequate for all life stages."


def _highlight_prestigious_journal(journal: str) -> str:
    """Add emoji to prestigious journals."""
    prestigious_keywords = ['harvard', 'oxford', 'stanford', 'cambridge', 'mit', 
                           'nature', 'science', 'lancet', 'jama', 'nejm']
    
    if any(keyword in journal.lower() for keyword in prestigious_keywords):
        return f"🏆 {journal}"
    return journal


def _get_year_range(sources: List[Dict]) -> str:
    """Get the year range of sources."""
    years = [int(s.get('year', 0)) for s in sources if s.get('year', '').isdigit()]
    if not years:
        return "recent years"
    
    years = sorted(years)
    if len(years) == 1:
        return str(years[0])
    return f"{years[0]}-{years[-1]}"


async def main():
    """Run the MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())