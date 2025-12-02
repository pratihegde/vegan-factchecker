"""
Nutrition Calculator
Calculates personalized daily nutrition needs based on age, gender, and weight
"""

from nutrition_database import (
    RDA_DATABASE,
    VEGAN_FOODS,
    NUTRIENT_TIPS,
    NUTRIENT_ALIASES
)


class NutritionCalculator:
    """Calculate personalized nutrition recommendations."""
    
    def __init__(self):
        self.rda_db = RDA_DATABASE
        self.foods_db = VEGAN_FOODS
        self.tips_db = NUTRIENT_TIPS
        self.aliases = NUTRIENT_ALIASES
    
    def normalize_nutrient_name(self, nutrient: str) -> str:
        """
        Normalize nutrient name to handle variations.
        Examples: 'omega3' -> 'omega-3', 'b12' -> 'vitamin-b12'
        """
        nutrient_lower = nutrient.lower().strip()
        
        # Check if it's an alias
        if nutrient_lower in self.aliases:
            return self.aliases[nutrient_lower]
        
        # Return as-is if not found (will be checked later)
        return nutrient_lower
    
    def calculate_daily_need(
        self,
        nutrient: str,
        age: int,
        gender: str,
        weight: float
    ) -> dict:
        """
        Calculate the daily need for a nutrient based on demographics.
        
        Returns:
            dict with daily_need, unit, notes
        """
        # Normalize nutrient name
        nutrient = self.normalize_nutrient_name(nutrient)
        
        # Check if nutrient exists
        if nutrient not in self.rda_db:
            available = list(self.rda_db.keys())
            return {
                "error": f"Nutrient '{nutrient}' not found in database.",
                "available_nutrients": sorted(available)
            }
        
        rda_info = self.rda_db[nutrient]
        
        # Special case: protein (weight-based calculation)
        if nutrient == "protein" or rda_info.get("calculation") == "weight_based":
            daily_need = rda_info["base_amount"] * weight
            return {
                "nutrient": nutrient,
                "daily_need": round(daily_need, 1),
                "unit": rda_info["unit"],
                "notes": rda_info.get("note", ""),
                "official_sources": ["NIH", "USDA", "WHO"]
            }
        
        # Find appropriate age range
        age_range = self._find_age_range(age, rda_info)
        
        if not age_range:
            return {
                "error": f"No RDA data for age {age}",
                "available_nutrients": list(self.rda_db.keys())
            }
        
        # Get RDA for gender
        rda_data = rda_info[age_range]
        gender_normalized = gender.lower()
        
        if gender_normalized not in rda_data:
            return {
                "error": f"No data for gender '{gender}'",
                "available_nutrients": list(self.rda_db.keys())
            }
        
        daily_need = rda_data[gender_normalized]
        
        return {
            "nutrient": nutrient,
            "daily_need": daily_need,
            "unit": rda_info["unit"],
            "notes": rda_info.get("note", ""),
            "official_sources": ["NIH", "USDA", "WHO"]
        }
    
    def _find_age_range(self, age: int, rda_info: dict) -> str:
        """Find the appropriate age range for the given age."""
        # Get all age ranges (exclude 'unit' and 'note' keys)
        age_ranges = [k for k in rda_info.keys() if k not in ['unit', 'note', 'calculation', 'base_amount']]
        
        for age_range in age_ranges:
            if self._age_in_range(age, age_range):
                return age_range
        
        return None
    
    def _age_in_range(self, age: int, age_range: str) -> bool:
        """Check if age falls within the specified range."""
        if '+' in age_range:
            # Format: "51+"
            min_age = int(age_range.replace('+', ''))
            return age >= min_age
        elif '-' in age_range:
            # Format: "19-50" or "51-70"
            parts = age_range.split('-')
            min_age = int(parts[0])
            max_age = int(parts[1])
            return min_age <= age <= max_age
        else:
            # Single age or error
            return False
    
    def find_food_sources(self, nutrient: str, max_results: int = 5) -> list:
        """
        Find the best food sources for a nutrient.
        Returns top foods sorted by amount per serving.
        """
        # Normalize nutrient name
        nutrient = self.normalize_nutrient_name(nutrient)
        
        if nutrient not in self.foods_db:
            return []
        
        foods = self.foods_db[nutrient]
        
        # Sort by amount (highest first)
        sorted_foods = sorted(foods, key=lambda x: x['amount'], reverse=True)
        
        return sorted_foods[:max_results]
    
    def generate_recommendation(
        self,
        age: int,
        gender: str,
        weight: float,
        nutrient: str
    ) -> dict:
        """
        Generate complete nutrition recommendation.
        
        Returns:
            Complete recommendation with daily need, food sources, tips, etc.
        """
        # Calculate daily need
        need_info = self.calculate_daily_need(nutrient, age, gender, weight)
        
        # Check for errors
        if "error" in need_info:
            return need_info
        
        # Find food sources
        food_sources = self.find_food_sources(nutrient)
        
        if not food_sources:
            return {
                "error": f"No food sources found for {nutrient}",
                "daily_need": need_info["daily_need"],
                "unit": need_info["unit"],
                "available_nutrients": list(self.rda_db.keys())
            }
        
        # Get tips if available
        tips = self.tips_db.get(nutrient, {})
        
        # Generate copy-paste response
        copy_response = self._generate_copy_response(
            nutrient=nutrient,
            daily_need=need_info["daily_need"],
            unit=need_info["unit"],
            top_food=food_sources[0]
        )
        
        return {
            "nutrient": nutrient.replace('-', ' ').title(),
            "profile": {
                "age": age,
                "gender": gender,
                "weight": weight
            },
            "daily_need": need_info["daily_need"],
            "unit": need_info["unit"],
            "notes": need_info.get("notes", ""),
            "food_options": food_sources,
            "tips": tips,
            "copy_response": copy_response,
            "official_sources": need_info["official_sources"]
        }
    
    def _generate_copy_response(
        self,
        nutrient: str,
        daily_need: float,
        unit: str,
        top_food: dict
    ) -> str:
        """
        Generate a copy-paste response for debates.
        
        Example: "I get my omega-3 from ground flaxseeds (1 tbsp) - 
                  that's 214% of my daily need."
        """
        food_name = top_food['name'].lower()
        serving = top_food['serving']
        amount = top_food['amount']
        
        # Calculate percentage
        percentage = round((amount / daily_need) * 100)
        
        # Format nutrient name nicely
        nutrient_display = nutrient.replace('-', ' ')
        
        # Generate response
        if percentage >= 100:
            response = (
                f"I get my {nutrient_display} from {food_name} ({serving}) - "
                f"that's {percentage}% of my daily need in just one serving!"
            )
        else:
            # Calculate servings needed
            servings_needed = round(daily_need / amount, 1)
            if servings_needed <= 3:
                response = (
                    f"I get my {nutrient_display} from {food_name} - "
                    f"about {servings_needed} servings throughout the day covers my needs."
                )
            else:
                response = (
                    f"I get my {nutrient_display} from {food_name} ({serving}) - "
                    f"each serving provides {amount}{unit}."
                )
        
        return response
    
    def list_available_nutrients(self) -> list:
        """Return list of all available nutrients."""
        return sorted(list(self.rda_db.keys()))