"""
Citation Formatter Module
Formats citations in APA and MLA styles for academic papers.
"""

from typing import Dict, Optional, List
from datetime import datetime


class CitationFormatter:
    """Formats academic citations in various styles."""
    
    def format_apa(
        self,
        authors: str,
        year: str,
        title: str,
        journal: Optional[str] = None,
        volume: Optional[str] = None,
        issue: Optional[str] = None,
        pages: Optional[str] = None,
        doi: Optional[str] = None,
        url: Optional[str] = None,
    ) -> str:
        """
        Format citation in APA 7th edition style.
        
        Example:
        Smith, J., & Johnson, M. (2020). Plant-based diets and health outcomes.
        Journal of Nutrition, 150(3), 234-245. https://doi.org/10.1234/jn.2020.001
        """
        citation = f"{authors} ({year}). {title}. "
        
        if journal:
            citation += f"{journal}"
            if volume:
                citation += f", {volume}"
            if issue:
                citation += f"({issue})"
            if pages:
                citation += f", {pages}"
            citation += ". "
        
        if doi:
            citation += f"https://doi.org/{doi}"
        elif url:
            citation += url
        
        return citation.strip()
    
    def format_mla(
        self,
        authors: str,
        title: str,
        journal: Optional[str] = None,
        volume: Optional[str] = None,
        issue: Optional[str] = None,
        year: Optional[str] = None,
        pages: Optional[str] = None,
        doi: Optional[str] = None,
        url: Optional[str] = None,
    ) -> str:
        """
        Format citation in MLA 9th edition style.
        
        Example:
        Smith, John, and Mary Johnson. "Plant-based Diets and Health Outcomes."
        Journal of Nutrition, vol. 150, no. 3, 2020, pp. 234-245.
        https://doi.org/10.1234/jn.2020.001
        """
        # Format authors for MLA (last name, first name)
        citation = f'{self._format_mla_authors(authors)}. "{title}." '
        
        if journal:
            citation += f"{journal}"
            if volume:
                citation += f", vol. {volume}"
            if issue:
                citation += f", no. {issue}"
            if year:
                citation += f", {year}"
            if pages:
                citation += f", pp. {pages}"
            citation += ". "
        
        if doi:
            citation += f"https://doi.org/{doi}"
        elif url:
            citation += url
        
        citation += "."
        return citation
    
    def format_chicago(
        self,
        authors: str,
        year: str,
        title: str,
        journal: Optional[str] = None,
        volume: Optional[str] = None,
        issue: Optional[str] = None,
        pages: Optional[str] = None,
        doi: Optional[str] = None,
    ) -> str:
        """
        Format citation in Chicago style (Notes and Bibliography).
        
        Example:
        Smith, John, and Mary Johnson. "Plant-based Diets and Health Outcomes."
        Journal of Nutrition 150, no. 3 (2020): 234-45. https://doi.org/10.1234/jn.2020.001
        """
        citation = f'{self._format_chicago_authors(authors)}. "{title}." '
        
        if journal:
            citation += f"{journal} "
            if volume:
                citation += f"{volume}"
            if issue:
                citation += f", no. {issue}"
            if year:
                citation += f" ({year})"
            if pages:
                citation += f": {pages}"
            citation += ". "
        
        if doi:
            citation += f"https://doi.org/{doi}"
        
        return citation
    
    def format_vancouver(
        self,
        authors: str,
        title: str,
        journal: Optional[str] = None,
        year: Optional[str] = None,
        volume: Optional[str] = None,
        issue: Optional[str] = None,
        pages: Optional[str] = None,
    ) -> str:
        """
        Format citation in Vancouver style (common in medical journals).
        
        Example:
        Smith J, Johnson M. Plant-based diets and health outcomes.
        J Nutr. 2020;150(3):234-45.
        """
        # Vancouver uses initials only
        authors_vancouver = self._format_vancouver_authors(authors)
        
        citation = f"{authors_vancouver}. {title}. "
        
        if journal:
            # Abbreviate journal name (simplified version)
            journal_abbrev = self._abbreviate_journal(journal)
            citation += f"{journal_abbrev}. "
            
            if year:
                citation += f"{year}"
            if volume:
                citation += f";{volume}"
            if issue:
                citation += f"({issue})"
            if pages:
                citation += f":{pages}"
            citation += "."
        
        return citation
    
    def _format_mla_authors(self, authors: str) -> str:
        """Format authors for MLA style."""
        # Simple implementation - split by comma or 'and'
        if not authors:
            return "Unknown"
        
        # If already formatted or simple, return as is
        if "," in authors or len(authors.split()) <= 2:
            return authors
        
        # Try to format first author correctly
        parts = authors.split()
        if len(parts) >= 2:
            return f"{parts[-1]}, {' '.join(parts[:-1])}"
        
        return authors
    
    def _format_chicago_authors(self, authors: str) -> str:
        """Format authors for Chicago style."""
        return self._format_mla_authors(authors)
    
    def _format_vancouver_authors(self, authors: str) -> str:
        """Format authors for Vancouver style (Last name + initials)."""
        if not authors:
            return "Unknown"
        
        # Simplified - just return as is for now
        # Full implementation would parse and convert to initials
        return authors
    
    def _abbreviate_journal(self, journal: str) -> str:
        """Abbreviate journal name for Vancouver style."""
        # Common abbreviations for vegan/nutrition journals
        abbreviations = {
            "Journal of Nutrition": "J Nutr",
            "American Journal of Clinical Nutrition": "Am J Clin Nutr",
            "British Journal of Nutrition": "Br J Nutr",
            "Nutrients": "Nutrients",
            "Nature": "Nature",
            "Science": "Science",
            "The Lancet": "Lancet",
            "BMJ": "BMJ",
            "JAMA": "JAMA",
            "Environmental Science & Technology": "Environ Sci Technol",
        }
        
        return abbreviations.get(journal, journal)
    
    def format_bibtex(
        self,
        authors: str,
        year: str,
        title: str,
        journal: Optional[str] = None,
        volume: Optional[str] = None,
        issue: Optional[str] = None,
        pages: Optional[str] = None,
        doi: Optional[str] = None,
        citation_key: Optional[str] = None,
    ) -> str:
        """
        Format citation in BibTeX format.
        
        Example:
        @article{smith2020plant,
          author = {Smith, John and Johnson, Mary},
          title = {Plant-based Diets and Health Outcomes},
          journal = {Journal of Nutrition},
          year = {2020},
          volume = {150},
          number = {3},
          pages = {234--245},
          doi = {10.1234/jn.2020.001}
        }
        """
        if not citation_key:
            # Generate a simple key
            first_author = authors.split(",")[0].split()[-1].lower()
            citation_key = f"{first_author}{year}"
        
        bibtex = f"@article{{{citation_key},\n"
        bibtex += f"  author = {{{authors}}},\n"
        bibtex += f"  title = {{{title}}},\n"
        
        if journal:
            bibtex += f"  journal = {{{journal}}},\n"
        if year:
            bibtex += f"  year = {{{year}}},\n"
        if volume:
            bibtex += f"  volume = {{{volume}}},\n"
        if issue:
            bibtex += f"  number = {{{issue}}},\n"
        if pages:
            # BibTeX uses -- for page ranges
            pages_formatted = pages.replace("-", "--")
            bibtex += f"  pages = {{{pages_formatted}}},\n"
        if doi:
            bibtex += f"  doi = {{{doi}}},\n"
        
        bibtex += "}"
        
        return bibtex
    
    def parse_paper_for_citation(self, paper: Dict) -> Dict[str, str]:
        """
        Parse a paper dictionary and format it in all citation styles.
        
        Args:
            paper: Dictionary with paper information
            
        Returns:
            Dictionary with formatted citations in multiple styles
        """
        citations = {
            "apa": self.format_apa(
                authors=paper.get("authors", "Unknown"),
                year=str(paper.get("year", "n.d.")),
                title=paper.get("title", ""),
                journal=paper.get("journal"),
                volume=paper.get("volume"),
                issue=paper.get("issue"),
                pages=paper.get("pages"),
                doi=paper.get("doi"),
                url=paper.get("link")
            ),
            "mla": self.format_mla(
                authors=paper.get("authors", "Unknown"),
                title=paper.get("title", ""),
                journal=paper.get("journal"),
                volume=paper.get("volume"),
                issue=paper.get("issue"),
                year=str(paper.get("year", "")),
                pages=paper.get("pages"),
                doi=paper.get("doi"),
                url=paper.get("link")
            ),
            "chicago": self.format_chicago(
                authors=paper.get("authors", "Unknown"),
                year=str(paper.get("year", "n.d.")),
                title=paper.get("title", ""),
                journal=paper.get("journal"),
                volume=paper.get("volume"),
                issue=paper.get("issue"),
                pages=paper.get("pages"),
                doi=paper.get("doi")
            ),
            "vancouver": self.format_vancouver(
                authors=paper.get("authors", "Unknown"),
                title=paper.get("title", ""),
                journal=paper.get("journal"),
                year=str(paper.get("year", "")),
                volume=paper.get("volume"),
                issue=paper.get("issue"),
                pages=paper.get("pages")
            ),
            "bibtex": self.format_bibtex(
                authors=paper.get("authors", "Unknown"),
                year=str(paper.get("year", "")),
                title=paper.get("title", ""),
                journal=paper.get("journal"),
                volume=paper.get("volume"),
                issue=paper.get("issue"),
                pages=paper.get("pages"),
                doi=paper.get("doi")
            )
        }
        
        return citations
    
    def format_inline_citation(self, authors: str, year: str, style: str = "apa") -> str:
        """
        Format an inline citation for use in text.
        
        Args:
            authors: Author names
            year: Publication year
            style: Citation style ('apa', 'mla', 'chicago')
            
        Returns:
            Formatted inline citation
            
        Examples:
            APA: (Smith & Johnson, 2020)
            MLA: (Smith and Johnson 234)
            Chicago: (Smith and Johnson 2020, 234)
        """
        if style == "apa":
            # Get first author's last name
            first_author = authors.split(",")[0].split()[-1]
            if "," in authors or " and " in authors.lower():
                return f"({first_author} et al., {year})"
            return f"({first_author}, {year})"
        
        elif style == "mla":
            first_author = authors.split(",")[0].split()[-1]
            if "," in authors or " and " in authors.lower():
                return f"({first_author} et al.)"
            return f"({first_author})"
        
        elif style == "chicago":
            first_author = authors.split(",")[0].split()[-1]
            return f"({first_author} {year})"
        
        return f"({authors}, {year})"