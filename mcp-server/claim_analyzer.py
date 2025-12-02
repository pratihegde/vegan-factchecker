"""
Claim Analyzer Module
Analyzes claims to categorize them and determine what type of evidence is needed.
"""

import json
from typing import Dict, List
from openai import AsyncOpenAI


class ClaimAnalyzer:
    """Analyzes claims about veganism and animal rights."""
    
    def __init__(self, openai_api_key: str):
        self.client = AsyncOpenAI(api_key=openai_api_key)
        
        # Common vegan claim categories
        self.categories = {
            "health": "Health and nutrition claims",
            "environment": "Environmental impact claims",
            "ethics": "Animal welfare and ethical claims",
            "economics": "Economic and industry claims",
            "misconception": "Common misconceptions about veganism"
        }
    
    async def analyze(self, claim: str) -> Dict:
        """
        Analyze a claim to understand its nature and what evidence is needed.
        
        Returns:
            Dict with category, key_concepts, evidence_type, search_terms, etc.
        """
        
        prompt = f"""
Analyze the following claim about veganism or animal rights:

"{claim}"

Provide a comprehensive analysis:

1. **Category**: Which category does this claim fall into?
   - health: Claims about nutrition, health outcomes, deficiencies
   - environment: Claims about climate change, sustainability, pollution
   - ethics: Claims about animal sentience, suffering, rights
   - economics: Claims about industry, costs, farming practices
   - misconception: Common myths or misunderstandings about veganism

2. **Key Concepts**: What are the main concepts or terms in this claim?

3. **Evidence Type**: What kind of evidence is most appropriate?
   - Clinical trials
   - Meta-analyses
   - Observational studies
   - Environmental data
   - Philosophical arguments
   - Economic reports

4. **Search Terms**: What are the best academic search terms (5-7 terms)?

5. **Relevant Fields**: What academic fields should we search?
   - Nutrition science
   - Environmental science
   - Animal cognition
   - Philosophy/Ethics
   - Agricultural economics
   - etc.

6. **Complexity**: Rate the complexity of finding evidence (1-10)
   - Simple: Well-studied, clear consensus (e.g., "Do vegans need B12 supplements?")
   - Complex: Emerging research, mixed evidence (e.g., "Can plants feel pain?")

7. **Common Counterarguments**: What are typical counterarguments to this claim?

Return your analysis as JSON in this exact format:
{{
  "category": "<one of: health, environment, ethics, economics, misconception>",
  "key_concepts": ["concept1", "concept2", "concept3"],
  "evidence_type": "<type>",
  "search_terms": ["term1", "term2", "term3", "term4", "term5"],
  "relevant_fields": ["field1", "field2", "field3"],
  "complexity": <number 1-10>,
  "typical_counterarguments": ["counter1", "counter2"],
  "context": "<brief context about why this claim matters in vegan advocacy>"
}}
"""
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert in vegan advocacy, nutrition science, environmental science, and animal ethics. 
You help activists understand claims deeply so they can find the best evidence.
You are objective and scientific in your analysis."""
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
            )
            
            analysis = json.loads(response.choices[0].message.content)
            
            # Validate and enhance the analysis
            analysis = self._validate_analysis(analysis, claim)
            
            return analysis
        
        except Exception as e:
            print(f"Claim analysis error: {e}")
            # Return a basic fallback analysis
            return self._fallback_analysis(claim)
    
    def _validate_analysis(self, analysis: Dict, claim: str) -> Dict:
        """Validate and ensure all required fields are present."""
        required_fields = [
            "category",
            "key_concepts",
            "evidence_type",
            "search_terms",
            "relevant_fields",
            "complexity",
            "typical_counterarguments",
            "context"
        ]
        
        for field in required_fields:
            if field not in analysis:
                analysis[field] = self._get_default_value(field, claim)
        
        # Ensure category is valid
        if analysis["category"] not in self.categories:
            analysis["category"] = self._guess_category(claim)
        
        # Ensure complexity is in range
        if not isinstance(analysis["complexity"], int) or analysis["complexity"] < 1:
            analysis["complexity"] = 5
        analysis["complexity"] = min(10, max(1, analysis["complexity"]))
        
        return analysis
    
    def _get_default_value(self, field: str, claim: str):
        """Get default value for missing fields."""
        defaults = {
            "category": "misconception",
            "key_concepts": [claim[:50]],
            "evidence_type": "Peer-reviewed studies",
            "search_terms": [claim],
            "relevant_fields": ["Nutrition", "Animal Science"],
            "complexity": 5,
            "typical_counterarguments": [],
            "context": "Common question in vegan advocacy"
        }
        return defaults.get(field, "")
    
    def _guess_category(self, claim: str) -> str:
        """Simple heuristic to guess claim category."""
        claim_lower = claim.lower()
        
        health_keywords = ["protein", "b12", "nutrition", "deficiency", "health", "vitamin", "omega"]
        environment_keywords = ["climate", "greenhouse", "emissions", "environment", "sustainability", "water"]
        ethics_keywords = ["pain", "suffer", "sentience", "feel", "consciousness", "rights"]
        economics_keywords = ["industry", "farming", "cost", "expensive", "economic", "production"]
        
        if any(kw in claim_lower for kw in health_keywords):
            return "health"
        elif any(kw in claim_lower for kw in environment_keywords):
            return "environment"
        elif any(kw in claim_lower for kw in ethics_keywords):
            return "ethics"
        elif any(kw in claim_lower for kw in economics_keywords):
            return "economics"
        else:
            return "misconception"
    
    def _fallback_analysis(self, claim: str) -> Dict:
        """Provide a basic analysis if the AI analysis fails."""
        category = self._guess_category(claim)
        
        return {
            "category": category,
            "key_concepts": [claim[:50]],
            "evidence_type": "Peer-reviewed studies",
            "search_terms": [claim, f"vegan {category}"],
            "relevant_fields": ["Nutrition Science", "Animal Science"],
            "complexity": 5,
            "typical_counterarguments": ["Analysis unavailable"],
            "context": "Claim requires further analysis"
        }
    
    async def batch_analyze(self, claims: List[str]) -> List[Dict]:
        """Analyze multiple claims in parallel."""
        import asyncio
        
        tasks = [self.analyze(claim) for claim in claims]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle any exceptions
        analyses = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                analyses.append(self._fallback_analysis(claims[i]))
            else:
                analyses.append(result)
        
        return analyses
    
    def get_category_description(self, category: str) -> str:
        """Get a description of what a category means."""
        return self.categories.get(category, "Unknown category")
    
    def suggest_follow_up_questions(self, claim: str, analysis: Dict) -> List[str]:
        """Suggest follow-up questions based on the claim analysis."""
        category = analysis.get("category", "")
        
        follow_ups = {
            "health": [
                "What are the latest studies on this topic?",
                "Are there any long-term health outcomes to consider?",
                "What do major health organizations say?",
            ],
            "environment": [
                "What are the most recent environmental impact studies?",
                "How does this compare to animal agriculture?",
                "What do climate scientists say?",
            ],
            "ethics": [
                "What does the scientific evidence say about animal sentience?",
                "What are the philosophical frameworks for animal rights?",
                "What do ethicists and researchers conclude?",
            ],
            "economics": [
                "What are the economic analyses of this claim?",
                "How has this changed over time?",
                "What do agricultural economists say?",
            ],
            "misconception": [
                "What does the scientific consensus say?",
                "Where did this misconception originate?",
                "What evidence contradicts this claim?",
            ]
        }
        
        return follow_ups.get(category, [
            "What does the scientific literature say?",
            "Are there any recent studies on this?",
            "What is the consensus view?",
        ])