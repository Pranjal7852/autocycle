from crewai_tools import SerperDevTool
from crewai.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchRun
from typing import Union, Dict, List
import json
import logging
import re
import random
# Initialize logging
logging.basicConfig(level=logging.DEBUG)

# Initialize base tools
search_tool = SerperDevTool()
ddg_search_tool = DuckDuckGoSearchRun()

# Define custom tools as BaseTool subclasses
class BrandResearchTool(BaseTool):
    name: str = "BrandResearchTool"
    description: str = "Search for information about brand value, perception, and sustainability metrics."

    def _run(self, query: str) -> str:
        return ddg_search_tool.run(f"brand analysis market perception {query}")

class IndustryCompatibilityTool(BaseTool):
    name: str = "IndustryCompatibilityTool"
    description: str = "Research compatibility between different industries for plastic reuse."

    def _run(self, query: str) -> str:
        return ddg_search_tool.run(f"plastic reuse compatibility {query}")

class MarketRatesTool(BaseTool):
    name: str = "MarketRatesTool"
    description: str = "Find current market rates for different types of recycled plastics."

    def _run(self, query: str) -> str:
        return ddg_search_tool.run(f"plastic recycling market rates {query}")

class IndustryMatchTool(BaseTool):
    name: str = "IndustryMatchTool"
    description: str = "Identifies diverse brands across industries that could use the specified plastic type for upcycling, aligned with the seller's brand values."

    def _run(self, input_data: Union[str, Dict]) -> str:
        try:
            # Parse input data
            data = self._parse_input(input_data)
            
            plastic_type = data.get("plastic_type", "PCABS")
            brand = data.get("brand", "NIKE")
            brand_analysis = data.get("brand_analysis", {})
            
            logging.debug(f"IndustryMatchTool input: {data}")
            
            # Get core brand elements for matching
            brand_category = brand_analysis.get("brand_category", "other")
            brand_values = brand_analysis.get("brand_characteristics", {}).get("values", [])
            brand_focus = brand_analysis.get("brand_characteristics", {}).get("focus_areas", [])
            target_audience = brand_analysis.get("brand_characteristics", {}).get("target_audience", [])
            
            # Generate targeted search queries - fewer but more diverse queries
            search_queries = self._generate_diverse_queries(
                brand, plastic_type, brand_category, brand_values, brand_focus, target_audience
            )
            
            # Shuffle queries to ensure different sequences on each run
            random.shuffle(search_queries)
            
            # Find matches across industries with built-in diversity
            matches = self._find_diverse_matches(
                search_queries, brand, plastic_type, brand_analysis
            )
            
            if not matches:
                raise Exception("No valid brand matches found after search attempts")
                
            # Ensure variety in final results by enforcing industry diversity
            diverse_matches = self._ensure_industry_diversity(matches)
            
            return json.dumps(diverse_matches[:5], indent=2)
            
        except Exception as e:
            logging.error(f"Error in IndustryMatchTool: {str(e)}")
            return json.dumps({"error": f"Failed to identify brands: {str(e)}"}, indent=2)

    def _parse_input(self, input_data: Union[str, Dict]) -> Dict:
        """Parse and normalize input data."""
        if isinstance(input_data, dict):
            return input_data
            
        try:
            data = json.loads(input_data)
            if isinstance(data, str):
                data = json.loads(data)
            return data
        except json.JSONDecodeError:
            return {}

    def _generate_diverse_queries(self, brand: str, plastic_type: str, brand_category: str,
                                brand_values: List[str], brand_focus: List[str],
                                target_audience: List[str]) -> List[str]:
        """Generate fewer but more diverse search queries."""
        queries = []
        
        # Primary queries - always include these
        queries.extend([
            f"innovative companies using {plastic_type} sustainable manufacturing",
            f"brands circular economy {plastic_type} recycling",
            f"{plastic_type} recycling industry leaders"
        ])
        
        # Brand-specific queries - add context from the original brand
        if brand:
            queries.append(f"brands similar to {brand} sustainable innovation")
            
        # Add value-based queries with randomization
        if brand_values:
            # Pick 1-2 random values
            selected_values = random.sample(brand_values, min(2, len(brand_values)))
            for value in selected_values:
                queries.append(f"{value} focused brands sustainable materials")
        
        # Add focus-based query
        if brand_focus:
            focus = random.choice(brand_focus)
            queries.append(f"{focus} companies recycling innovation")
        
        # Add industry-diverse queries to ensure varied results
        industries = ["fashion", "furniture", "automotive", "electronics", "toys", 
                     "outdoor", "medical", "packaging", "construction"]
                     
        # Select 3 random industries for this search
        selected_industries = random.sample(industries, 3)
        for industry in selected_industries:
            queries.append(f"{industry} brands using recycled {plastic_type}")
        
        return list(set(queries))  # Remove any duplicates

    def _find_diverse_matches(self, search_queries: List[str], target_brand: str, 
                           plastic_type: str, brand_analysis: Dict) -> List[Dict]:
        """Find diverse brand matches by tracking industries and ensuring variety."""
        matches = []
        seen_brands = set()
        industry_count = {}
        
        # Use only a subset of queries to improve performance
        for query in search_queries[:8]:  # Limit to 8 queries max
            try:
                logging.debug(f"Search query: {query}")
                search_results = search_tool.run(search_query=query)
                
                if not isinstance(search_results, dict) or "organic" not in search_results:
                    continue
                    
                for result in search_results["organic"]:
                    if len(matches) >= 8:  # Get more matches than needed for diversity filtering
                        break
                        
                    title = result.get("title", "")
                    snippet = result.get("snippet", "")
                    
                    # Extract brand and industry
                    brand_name = self._extract_brand_name(title, snippet)
                    if not brand_name or brand_name.lower() in [b.lower() for b in seen_brands]:
                        continue
                        
                    industry = self._identify_industry(title, snippet)
                    if not industry:
                        continue
                        
                    # Track industry count
                    industry_count[industry] = industry_count.get(industry, 0) + 1
                    
                    # Limit matches per industry to ensure diversity
                    if industry_count[industry] > 2:
                        continue
                    
                    # Create match with reason and alignment
                    match = {
                        "brand": brand_name,
                        "industry": industry,
                        "reason": self._generate_reason(brand_name, industry, plastic_type, target_brand, snippet),
                        "brand_value_alignment": self._generate_alignment(brand_name, target_brand, brand_analysis),
                        "market_synergy": self._generate_synergy(brand_name, target_brand, industry, brand_analysis)
                    }
                    
                    matches.append(match)
                    seen_brands.add(brand_name)
                    
            except Exception as e:
                logging.warning(f"Search query failed: {query} - {str(e)}")
                continue
                
        return matches

    def _ensure_industry_diversity(self, matches: List[Dict]) -> List[Dict]:
        """Ensure industry diversity in final results."""
        if len(matches) <= 5:
            return matches
            
        # Group by industry
        industry_groups = {}
        for match in matches:
            industry = match["industry"]
            if industry not in industry_groups:
                industry_groups[industry] = []
            industry_groups[industry].append(match)
            
        # Select diverse matches
        diverse_matches = []
        industries = list(industry_groups.keys())
        
        # Take one from each industry first
        for industry in industries:
            if len(diverse_matches) < 5 and industry_groups[industry]:
                diverse_matches.append(industry_groups[industry].pop(0))
                
        # Fill remaining slots with leftover matches
        remaining_matches = [m for group in industry_groups.values() for m in group]
        random.shuffle(remaining_matches)  # Randomize order
        
        while len(diverse_matches) < 5 and remaining_matches:
            diverse_matches.append(remaining_matches.pop(0))
            
        return diverse_matches

    def _extract_brand_name(self, title: str, snippet: str) -> str:
        """Extract brand name using improved patterns and filtering."""
        # Combine text for processing
        text = title + " " + snippet
        
        # Extract potential brand names
        candidates = []
        
        # Pattern 1: Look for capitalized words followed by company indicators
        pattern1 = r'([A-Z][a-zA-Z0-9]*(?:\s+[A-Z][a-zA-Z0-9]*){0,2})(?:\s+(?:Inc|LLC|Ltd|Company|Corp|GmbH|Co\.|Group|Brands|Technology|Industries))'
        matches = re.findall(pattern1, text)
        candidates.extend(matches)
        
        # Pattern 2: Look for capitalized names in quotes
        pattern2 = r'"([A-Z][a-zA-Z0-9]*(?:\s+[A-Z][a-zA-Z0-9]*){0,2})"'
        matches = re.findall(pattern2, text)
        candidates.extend(matches)
        
        # Pattern 3: Look for capitalized words followed by verbs
        pattern3 = r'([A-Z][a-zA-Z0-9]*(?:\s+[A-Z][a-zA-Z0-9]*){0,2})(?:\s+(?:is|has|announced|launched|developed|created|produces|manufactures))'
        matches = re.findall(pattern3, text)
        candidates.extend(matches)
        
        # Filter candidates
        filtered_candidates = []
        common_words = {'the', 'this', 'that', 'these', 'those', 'their', 'our', 'your', 
                       'from', 'with', 'about', 'what', 'when', 'where', 'why', 'how'}
        
        for candidate in candidates:
            # Skip single letter brands and common words
            if len(candidate) <= 1 or candidate.lower() in common_words:
                continue
                
            # Skip common phrases
            if any(term in candidate.lower() for term in ['sustainable', 'recycled', 'company', 'brand']):
                continue
                
            filtered_candidates.append(candidate.strip())
            
        # Return the first valid candidate or None
        return filtered_candidates[0] if filtered_candidates else None

    def _identify_industry(self, title: str, snippet: str) -> str:
        """Identify industry with improved pattern matching."""
        text = (title + " " + snippet).lower()
        
        # Industry mapping with weighted keywords
        industries = {
            "Fashion": ["apparel", "clothing", "fashion", "textile", "garment", "wear", "sportswear"],
            "Furniture": ["furniture", "home décor", "interior design", "housewares"],
            "Automotive": ["automotive", "car", "vehicle", "transportation", "mobility"],
            "Electronics": ["electronics", "technology", "devices", "gadgets", "tech", "digital"],
            "Toys": ["toys", "games", "play", "children", "kids", "educational"],
            "Outdoor": ["outdoor", "recreation", "sports equipment", "fitness", "adventure"],
            "Medical": ["medical", "healthcare", "health", "pharmaceutical", "wellness"],
            "Packaging": ["packaging", "container", "shipping", "storage"],
            "Construction": ["construction", "building", "architecture", "infrastructure"],
            "Consumer Goods": ["consumer", "household", "home", "lifestyle"],
            "Industrial": ["industrial", "manufacturing", "factory", "production"]
        }
        
        # Score each industry by counting keyword matches
        scores = {industry: 0 for industry in industries}
        
        for industry, keywords in industries.items():
            for keyword in keywords:
                if keyword in text:
                    scores[industry] += 1
                    
        # Return highest scoring industry or None if no clear match
        max_score = max(scores.values()) if scores else 0
        if max_score > 0:
            # Get industries with the maximum score
            top_industries = [ind for ind, score in scores.items() if score == max_score]
            return random.choice(top_industries)  # Random choice if multiple match
            
        return None

    def _generate_reason(self, brand_name: str, industry: str, plastic_type: str, 
                        target_brand: str, snippet: str) -> str:
        """Generate concise, varied reasoning."""
        # Extract themes from snippet
        themes = []
        theme_keywords = {
            "sustainability": ["sustainable", "eco", "green", "environment"],
            "innovation": ["innovative", "technology", "advanced", "cutting-edge"],
            "quality": ["premium", "quality", "high-end", "luxury"],
            "design": ["design", "aesthetic", "style", "creative"],
            "circular economy": ["circular", "recycling", "upcycling", "reuse"]
        }
        
        for theme, keywords in theme_keywords.items():
            if any(keyword in snippet.lower() for keyword in keywords):
                themes.append(theme)
                
        # Add 1-2 random themes if none found
        if not themes:
            themes = random.sample(list(theme_keywords.keys()), min(2, len(theme_keywords)))
            
        # Create reason templates for variety
        templates = [
            f"{brand_name} could integrate {plastic_type} into their {industry} products, focusing on {themes[0] if themes else 'sustainability'}.",
            f"As a leader in {industry}, {brand_name} could benefit from utilizing {plastic_type} in their production process.",
            f"{brand_name}'s {industry} expertise combined with {plastic_type} could create innovative sustainable products.",
            f"Incorporating {plastic_type} aligns with {brand_name}'s {themes[0] if themes else 'sustainability'} initiatives in the {industry} sector."
        ]
        
        return random.choice(templates)

    def _generate_alignment(self, brand_name: str, target_brand: str, brand_analysis: Dict) -> str:
        """Generate varied brand value alignment statements."""
        # Get brand values with fallbacks
        values = brand_analysis.get("brand_characteristics", {}).get("values", 
                 ["sustainability", "innovation", "quality"])
                 
        # Create alignment templates for variety
        templates = [
            f"{brand_name} and {target_brand} share values in {random.choice(values)}, creating natural partnership potential.",
            f"Both brands emphasize {random.choice(values)}, making this collaboration culturally aligned.",
            f"The partnership could strengthen both brands' commitment to {random.choice(values)}.",
            f"Values alignment in {random.choice(values)} would make this collaboration authentic and meaningful."
        ]
        
        return random.choice(templates)

    def _generate_synergy(self, brand_name: str, target_brand: str, industry: str, 
                         brand_analysis: Dict) -> str:
        """Generate varied market synergy statements."""
        # Get audience with fallbacks
        audience = brand_analysis.get("brand_characteristics", {}).get("target_audience", 
                  ["eco-conscious consumers", "quality-focused customers"])
                  
        # Create synergy templates for variety
        templates = [
            f"Collaboration between {brand_name} and {target_brand} would appeal to {random.choice(audience)} seeking sustainable {industry} solutions.",
            f"The partnership could create new market opportunities in the {industry} sector for both brands.",
            f"Combined expertise would drive innovation in sustainable {industry} products for {random.choice(audience)}.",
            f"This collaboration could establish both brands as leaders in sustainable {industry} solutions."
        ]
        
        return random.choice(templates)

    def _arun(self, input_data: Union[str, Dict]) -> str:
        # Async version
        return self._run(input_data)

# Instantiate tools
brand_research_tool = BrandResearchTool()
industry_compatibility_tool = IndustryCompatibilityTool()
market_rates_tool = MarketRatesTool()
industry_match_tool = IndustryMatchTool()