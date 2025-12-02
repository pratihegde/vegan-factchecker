"""
Research Assistant Module
Handles searching across multiple academic databases and credible sources.
"""

import asyncio
import httpx
from typing import List, Dict, Optional, Any
from datetime import datetime
import json


class ResearchAssistant:
    """Searches peer-reviewed journals and credible sources for evidence."""
    
    def __init__(self, tavily_api_key: str, openai_api_key: str, semantic_scholar_key: Optional[str] = None):
        self.tavily_api_key = tavily_api_key
        self.openai_api_key = openai_api_key
        self.semantic_scholar_key = semantic_scholar_key
        
        # Credible organizations for vegan/animal rights research
        self.credible_orgs = [
            "who.int",
            "fao.org",
            "ipcc.ch",
            "nih.gov",
            "epa.gov",
            "animalcharityevaluators.org",
            "faunalytics.org",
            "cambridge.org",
            "nature.com",
            "sciencedirect.com",
            "springer.com",
            "wiley.com"
        ]
    
    async def search_evidence(
        self,
        claim: str,
        category: str,
        max_results: int = 5,
        include_counterarguments: bool = True
    ) -> Dict[str, Any]:
        """
        Search for evidence to verify a claim.
        Uses multiple sources and synthesizes results.
        """
        
        # Search in parallel across multiple sources
        tasks = [
            self._search_semantic_scholar(claim, max_results),
            self._search_tavily(claim, max_results),
            self._search_pubmed(claim, max_results) if category == "health" else None,
        ]
        
        results = await asyncio.gather(*[t for t in tasks if t is not None])
        
        # Combine and deduplicate results
        all_sources = self._combine_results(results)
        
        # Analyze evidence quality and confidence
        evidence = await self._analyze_evidence(claim, all_sources, category)
        
        # Find counterarguments if requested
        if include_counterarguments:
            evidence['counterarguments'] = await self._find_counterarguments(claim, category)
        
        # Search for credible organization reports
        evidence['org_reports'] = await self._search_org_reports(claim)
        
        return evidence
    
    async def _search_semantic_scholar(self, query: str, max_results: int) -> List[Dict]:
        """Search Semantic Scholar for academic papers."""
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        
        headers = {}
        if self.semantic_scholar_key:
            headers["x-api-key"] = self.semantic_scholar_key
        
        params = {
            "query": query,
            "limit": max_results,
            "fields": "title,authors,year,abstract,citationCount,journal,externalIds,openAccessPdf,publicationTypes",
            "year": "2014-",  # Last 10 years
            "openAccessPdf": "",  # Prefer open access
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(url, params=params, headers=headers)
                response.raise_for_status()
                data = response.json()
                
                papers = []
                for paper in data.get("data", []):
                    papers.append(self._parse_semantic_scholar_paper(paper))
                
                return papers
            except Exception as e:
                print(f"Semantic Scholar search error: {e}")
                return []
    
    def _parse_semantic_scholar_paper(self, paper: Dict) -> Dict:
        """Parse Semantic Scholar paper into our standard format."""
        authors = ", ".join([a.get("name", "") for a in paper.get("authors", [])])
        
        # Get DOI or other identifier
        external_ids = paper.get("externalIds", {})
        doi = external_ids.get("DOI", "")
        
        # Get open access link
        link = paper.get("openAccessPdf", {}).get("url", "")
        if not link and doi:
            link = f"https://doi.org/{doi}"
        
        return {
            "title": paper.get("title", ""),
            "authors": authors,
            "year": paper.get("year", ""),
            "abstract": paper.get("abstract", ""),
            "journal": paper.get("journal", {}).get("name", "Unknown Journal"),
            "citation_count": paper.get("citationCount", 0),
            "doi": doi,
            "link": link,
            "access_type": "Open Access" if paper.get("openAccessPdf") else "May require access",
            "source": "Semantic Scholar",
            "study_type": self._infer_study_type(paper),
        }
    
    async def _search_tavily(self, query: str, max_results: int) -> List[Dict]:
        """Search using Tavily for web and academic sources."""
        from tavily import TavilyClient
        
        client = TavilyClient(api_key=self.tavily_api_key)
        
        try:
            # Search with academic focus
            # Note: Tavily only accepts topic="general", "news", or "finance"
            # We use "general" for scientific/academic queries
            response = client.search(
                query=query,
                search_depth="advanced",
                max_results=max_results,
                include_domains=self.credible_orgs,
                topic="general"  # Changed from "science" - Tavily API requirement
            )
            
            papers = []
            for result in response.get("results", []):
                # Try to extract paper-like information
                papers.append({
                    "title": result.get("title", ""),
                    "authors": "Various",  # Tavily doesn't always provide this
                    "year": self._extract_year(result.get("content", "")),
                    "abstract": result.get("content", "")[:500],
                    "journal": self._extract_source(result.get("url", "")),
                    "citation_count": 0,
                    "doi": "",
                    "link": result.get("url", ""),
                    "access_type": "Web Source",
                    "source": "Tavily",
                    "study_type": "Research",
                })
            
            return papers
        except Exception as e:
            print(f"Tavily search error: {e}")
            return []
    
    async def _search_pubmed(self, query: str, max_results: int) -> List[Dict]:
        """Search PubMed for health-related studies."""
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                # Search for IDs
                search_url = f"{base_url}/esearch.fcgi"
                search_params = {
                    "db": "pubmed",
                    "term": query,
                    "retmax": max_results,
                    "retmode": "json",
                    "sort": "relevance",
                    "mindate": "2014",
                }
                
                search_response = await client.get(search_url, params=search_params)
                search_data = search_response.json()
                
                ids = search_data.get("esearchresult", {}).get("idlist", [])
                
                if not ids:
                    return []
                
                # Fetch details
                fetch_url = f"{base_url}/esummary.fcgi"
                fetch_params = {
                    "db": "pubmed",
                    "id": ",".join(ids),
                    "retmode": "json",
                }
                
                fetch_response = await client.get(fetch_url, params=fetch_params)
                fetch_data = fetch_response.json()
                
                papers = []
                for pmid, data in fetch_data.get("result", {}).items():
                    if pmid == "uids":
                        continue
                    
                    papers.append(self._parse_pubmed_paper(data, pmid))
                
                return papers
            except Exception as e:
                print(f"PubMed search error: {e}")
                return []
    
    def _parse_pubmed_paper(self, data: Dict, pmid: str) -> Dict:
        """Parse PubMed paper into our standard format."""
        authors = ", ".join([a.get("name", "") for a in data.get("authors", [])])
        
        return {
            "title": data.get("title", ""),
            "authors": authors,
            "year": data.get("pubdate", "")[:4],
            "abstract": "",  # Would need separate call to get full abstract
            "journal": data.get("fulljournalname", ""),
            "citation_count": 0,
            "doi": data.get("elocationid", "").replace("doi: ", ""),
            "link": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            "access_type": "PubMed",
            "source": "PubMed",
            "study_type": self._infer_study_type(data),
        }
    
    def _combine_results(self, results: List[List[Dict]]) -> List[Dict]:
        """Combine and deduplicate results from multiple sources."""
        combined = []
        seen_titles = set()
        
        for result_list in results:
            for paper in result_list:
                # Simple deduplication by title
                title_normalized = paper.get("title", "").lower().strip()
                if title_normalized and title_normalized not in seen_titles:
                    seen_titles.add(title_normalized)
                    combined.append(paper)
        
        # Sort by year (most recent first) and citation count
        # Convert year to int for proper sorting, use 0 for invalid years
        def get_sort_key(paper):
            year = paper.get("year", 0)
            # Try to convert to int, default to 0 if it fails
            try:
                year_int = int(year) if year else 0
            except (ValueError, TypeError):
                year_int = 0
            
            citation_count = paper.get("citation_count", 0)
            # Ensure citation_count is int
            try:
                citation_int = int(citation_count) if citation_count else 0
            except (ValueError, TypeError):
                citation_int = 0
            
            return (year_int, citation_int)
        
        combined.sort(key=get_sort_key, reverse=True)
        
        return combined
    
    async def _analyze_evidence(self, claim: str, sources: List[Dict], category: str) -> Dict:
        """Analyze evidence and calculate confidence score."""
        from openai import AsyncOpenAI
        
        client = AsyncOpenAI(api_key=self.openai_api_key)
        
        # If no sources found, use OpenAI's knowledge as fallback
        if not sources or len(sources) == 0:
            print("No sources found - using OpenAI knowledge fallback")
            return await self._openai_knowledge_fallback(claim, category, client)
        
        # Prepare source summaries for analysis
        source_summaries = []
        for source in sources[:5]:  # Analyze top 5 sources
            source_summaries.append({
                "title": source.get("title", ""),
                "abstract": source.get("abstract", "")[:300],
                "year": source.get("year", ""),
                "citation_count": source.get("citation_count", 0),
            })
        
        # Add pro-vegan context based on claim type
        claim_lower = claim.lower()
        vegan_context = ""
        
        if 'protein' in claim_lower and ('plant' in claim_lower or 'vegan' in claim_lower):
            vegan_context = """
IMPORTANT CONTEXT FOR PROTEIN CLAIMS:
- The Academy of Nutrition and Dietetics (100,000+ professionals) states that plant-based diets are nutritionally adequate for all life stages
- Plant proteins become complete when combined (beans + rice, hummus + pita, etc.)
- Billions of healthy vegetarians/vegans worldwide prove adequacy
- "Different" does not mean "inadequate" - distinguish these clearly
- Protein complementation happens automatically when eating varied plant foods throughout the day
"""
        
        elif 'b12' in claim_lower or 'vitamin b12' in claim_lower:
            vegan_context = """
IMPORTANT CONTEXT FOR B12:
- B12 comes from bacteria, not animals
- Most livestock are given B12 supplements - vegans just take it directly
- B12 deficiency is common in omnivores too (especially elderly)
- Supplementation is a modern solution, not a weakness of veganism
"""
        
        elif any(word in claim_lower for word in ['deficiency', 'lacking', 'missing', 'not enough']):
            vegan_context = """
IMPORTANT CONTEXT FOR NUTRIENT ADEQUACY:
- Major health organizations confirm well-planned plant-based diets meet all nutritional needs
- Focus on "well-planned" vs "poorly-planned" diets, not plant vs animal
- Many nutrients are MORE abundant in plant foods
- Deficiencies can occur in ANY diet if poorly planned
"""
        
        elif 'expensive' in claim_lower or 'cost' in claim_lower:
            vegan_context = """
IMPORTANT CONTEXT FOR COST:
- Beans, rice, lentils, oats are among the cheapest foods globally
- Meat is often subsidized - true cost is much higher
- Vegan staples are less expensive than meat/dairy in most places
- "Expensive vegan products" are optional, not required
"""
        
        # Use OpenAI to analyze evidence and extract key information
        prompt = f"""
You are analyzing scientific evidence for the following claim from a PRO-VEGAN ADVOCACY perspective:
"{claim}"

Category: {category}

{vegan_context}

Here are the top sources found:
{json.dumps(source_summaries, indent=2)}

Your analysis should:
1. Prioritize sources from major health organizations (WHO, Academy of Nutrition and Dietetics, NIH position papers)
2. Distinguish between "different" and "inadequate" - these are not the same
3. Provide context that supports plant-based nutrition when evidence allows
4. Be scientifically accurate but frame findings in a way that's helpful for vegan advocacy
5. Note when industry-funded studies may have bias against plant-based foods

Please provide:
1. A confidence score (0-10) on whether the evidence SUPPORTS the claim (0 = claim is false/misleading, 10 = claim is completely true)
2. A 2-3 sentence summary that provides pro-vegan context while being scientifically accurate
3. For each source, identify:
   - The key finding related to the claim (with pro-vegan framing when appropriate)
   - The best direct quote (15-30 words) that activists can use
   - Any important context (e.g., "Note: This compares isolated proteins, not real-world diets")

Format your response as JSON with this structure:
{{
  "confidence_score": <number>,
  "summary": "<string>",
  "sources": [
    {{
      "title": "<string>",
      "key_finding": "<string>",
      "direct_quote": "<string>",
      "context_note": "<string or empty if not needed>"
    }}
  ]
}}
"""
        
        try:
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system", 
                        "content": """You are a research analyst supporting vegan animal rights activists. 
Your goal is to provide scientifically accurate information that helps activists advocate effectively for plant-based nutrition and animal rights.

When analyzing evidence:
- Prioritize position statements from major health organizations (Academy of Nutrition and Dietetics, WHO, etc.)
- Distinguish between "different" and "inadequate" - these are NOT the same
- Provide context that supports plant-based nutrition when evidence allows
- Frame findings in ways that are helpful for vegan advocacy while remaining scientifically accurate
- Note when studies compare isolated nutrients vs. real-world diets
- Recognize that protein complementation makes plant proteins nutritionally complete
- Be aware of potential industry bias in animal agriculture-funded research

You are scientifically rigorous AND pro-vegan advocacy."""
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
            )
            
            analysis = json.loads(response.choices[0].message.content)
            
            # Enhance sources with full information
            enhanced_sources = []
            for i, source in enumerate(sources[:len(analysis.get("sources", []))]):
                enhanced = source.copy()
                enhanced.update(analysis["sources"][i])
                
                # Add formatted citations
                enhanced["citation_apa"] = self._format_apa_citation(enhanced)
                enhanced["citation_mla"] = self._format_mla_citation(enhanced)
                
                enhanced_sources.append(enhanced)
            
            return {
                "confidence_score": analysis.get("confidence_score", 5),
                "summary": analysis.get("summary", "Evidence analysis unavailable"),
                "sources": enhanced_sources,
            }
        
        except Exception as e:
            print(f"Evidence analysis error: {e}")
            # Return basic information without AI analysis
            return {
                "confidence_score": 5,
                "summary": "Multiple sources found. Please review individual sources for details.",
                "sources": sources[:5],
            }
    
    async def _openai_knowledge_fallback(self, claim: str, category: str, client) -> Dict:
        """Use OpenAI's knowledge when no sources are found."""
        
        # Add pro-vegan context
        claim_lower = claim.lower()
        vegan_context = ""
        
        if 'soy' in claim_lower and 'livestock' in claim_lower:
            vegan_context = "Context: About 77% of global soy production goes to livestock feed, not human food."
        elif 'protein' in claim_lower:
            vegan_context = "Context: Major health organizations confirm plant-based diets provide adequate protein."
        elif 'b12' in claim_lower:
            vegan_context = "Context: B12 comes from bacteria, and most livestock receive B12 supplements."
        
        prompt = f"""
You are a vegan advocacy research assistant. No peer-reviewed sources were found for this search, so provide an answer based on scientific consensus and your training data.

Claim: "{claim}"
Category: {category}
{vegan_context}

Provide a pro-vegan, scientifically accurate response that includes:
1. Confidence score (0-10) on whether the claim is true (0 = false, 10 = true)
2. A 2-3 sentence summary with pro-vegan framing
3. Key facts that would be helpful for activists (with specific numbers/statistics if known)

Format as JSON:
{{
  "confidence_score": <number>,
  "summary": "<string>",
  "key_facts": ["<fact1>", "<fact2>", "<fact3>"]
}}

Note: Since no peer-reviewed sources were found in the search, mention that this is based on scientific consensus rather than specific papers retrieved.
"""
        
        try:
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a pro-vegan advocacy assistant providing scientifically accurate information when peer-reviewed sources aren't available."
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Create a pseudo-source from OpenAI's knowledge
            fallback_source = {
                "title": "Scientific Consensus (No specific papers found in search)",
                "authors": "Based on scientific literature",
                "year": "2024",
                "journal": "General Knowledge",
                "key_finding": result.get("summary", ""),
                "direct_quote": result.get("key_facts", [""])[0] if result.get("key_facts") else "",
                "link": "https://claude.ai",
                "access_type": "AI Knowledge",
                "source": "OpenAI Fallback",
                "study_type": "Consensus",
                "citation_apa": "Based on scientific consensus (specific papers not found in search)",
                "citation_mla": "Based on scientific consensus (specific papers not found in search)"
            }
            
            return {
                "confidence_score": result.get("confidence_score", 5),
                "summary": result.get("summary", "") + " Note: No specific peer-reviewed papers were found in the search, but this answer is based on scientific consensus.",
                "sources": [fallback_source],
            }
        
        except Exception as e:
            print(f"OpenAI fallback error: {e}")
            return {
                "confidence_score": 5,
                "summary": "No peer-reviewed sources found in the search. Consider rephrasing the search query or consulting major health organization websites.",
                "sources": [],
            }
    
    async def _find_counterarguments(self, claim: str, category: str) -> List[str]:
        """Find alternative perspectives or counterarguments."""
        from openai import AsyncOpenAI
        
        client = AsyncOpenAI(api_key=self.openai_api_key)
        
        prompt = f"""
You're helping a vegan activist prepare for common objections to this claim: "{claim}"

Generate 2-3 SHORT, PUNCHY questions or objections that people commonly raise.

Format as actual questions people ask (5-15 words each), not long academic explanations.

Examples of GOOD responses:
- "But don't plants release chemicals when you cut them?"
- "What about that study where plants screamed?"
- "Doesn't soy have estrogen?"

Examples of BAD responses (too long/academic):
- "Plants lack a nervous system and brain, which are essential for the experience of pain..."
- "While plants can respond to environmental stimuli and exhibit behaviors..."

Return ONLY short, conversational questions as a JSON object with a "questions" array.
"""
        
        try:
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are helping activists prepare for real-world conversations. Generate SHORT, punchy questions people actually ask."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.5,
            )
            
            result = json.loads(response.choices[0].message.content)
            # Support both "questions" and "counterarguments" keys for backward compatibility
            return result.get("questions", result.get("counterarguments", []))
        
        except Exception as e:
            print(f"Counterargument search error: {e}")
            return []
    
    async def _search_org_reports(self, claim: str) -> List[Dict]:
        """Search for reports from credible organizations."""
        from tavily import TavilyClient
        
        client = TavilyClient(api_key=self.tavily_api_key)
        
        try:
            response = client.search(
                query=f"{claim} report",
                search_depth="advanced",
                max_results=3,
                include_domains=[
                    "who.int", "fao.org", "ipcc.ch", "nih.gov",
                    "animalcharityevaluators.org", "faunalytics.org"
                ]
            )
            
            reports = []
            for result in response.get("results", []):
                reports.append({
                    "organization": self._extract_org_name(result.get("url", "")),
                    "finding": result.get("content", "")[:200],
                    "link": result.get("url", ""),
                })
            
            return reports
        except Exception as e:
            print(f"Organization report search error: {e}")
            return []
    
    # Helper methods
    def _infer_study_type(self, paper: Dict) -> str:
        """Infer study type from paper metadata."""
        title = paper.get("title", "").lower()
        abstract = paper.get("abstract", "").lower()
        
        if "meta-analysis" in title or "meta-analysis" in abstract:
            return "Meta-analysis"
        elif "systematic review" in title or "systematic review" in abstract:
            return "Systematic Review"
        elif "randomized" in abstract or "rct" in abstract:
            return "Randomized Controlled Trial"
        elif "cohort" in abstract:
            return "Cohort Study"
        elif "case-control" in abstract:
            return "Case-Control Study"
        elif "cross-sectional" in abstract:
            return "Cross-sectional Study"
        else:
            return "Research Study"
    
    def _extract_year(self, text: str) -> str:
        """Extract year from text."""
        import re
        years = re.findall(r'\b(20\d{2})\b', text)
        return years[0] if years else str(datetime.now().year)
    
    def _extract_source(self, url: str) -> str:
        """Extract source name from URL."""
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        return domain.replace("www.", "").replace(".com", "").replace(".org", "")
    
    def _extract_org_name(self, url: str) -> str:
        """Extract organization name from URL."""
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        
        org_map = {
            "who.int": "World Health Organization",
            "fao.org": "Food and Agriculture Organization (UN)",
            "ipcc.ch": "Intergovernmental Panel on Climate Change",
            "nih.gov": "National Institutes of Health",
            "animalcharityevaluators.org": "Animal Charity Evaluators",
            "faunalytics.org": "Faunalytics",
        }
        
        return org_map.get(domain, domain)
    
    def _format_apa_citation(self, source: Dict) -> str:
        """Format citation in APA style."""
        authors = source.get("authors", "Unknown")
        year = source.get("year", "n.d.")
        title = source.get("title", "")
        journal = source.get("journal", "")
        doi = source.get("doi", "")
        
        citation = f"{authors} ({year}). {title}. "
        if journal:
            citation += f"{journal}. "
        if doi:
            citation += f"https://doi.org/{doi}"
        elif source.get("link"):
            citation += source.get("link")
        
        return citation
    
    def _format_mla_citation(self, source: Dict) -> str:
        """Format citation in MLA style."""
        authors = source.get("authors", "Unknown")
        title = source.get("title", "")
        journal = source.get("journal", "")
        year = source.get("year", "n.d.")
        link = source.get("link", "")
        
        # MLA format: Authors. "Title." Journal, Year, link.
        citation = f'{authors}. "{title}." '
        if journal:
            citation += f"{journal}, "
        citation += f"{year}"
        if link:
            citation += f", {link}"
        citation += "."
        
        return citation
    
    async def search_studies(
        self,
        topic: str,
        year_from: int = 2014,
        max_results: int = 10,
        focus_area: str = "all"
    ) -> List[Dict]:
        """Public method for searching studies on a topic."""
        results = await self._search_semantic_scholar(topic, max_results)
        return results
    
    async def get_paper_details(self, paper_id: str, include_related: bool = False) -> Dict:
        """Get detailed information about a specific paper."""
        # Implementation for fetching paper details by ID
        # This would use the paper_id (DOI, PubMed ID, etc.) to fetch full details
        return {
            "title": "Paper details",
            "note": "Detailed implementation needed based on ID type"
        }
    
    async def compare_sources(self, topic: str, source_ids: List[str] = None) -> Dict:
        """Compare multiple sources on a topic."""
        # Implementation for comparing sources
        return {
            "consensus": [],
            "conflicts": [],
            "quality_score": 7,
            "sources": []
        }