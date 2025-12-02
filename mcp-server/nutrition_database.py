"""
Comprehensive Nutrition Database for Vegan Foods
Includes vitamins, minerals, protein, omega-3, and more
All data from USDA FoodData Central, NIH, and WHO
"""

# RDA (Recommended Daily Allowances) for various nutrients
# Format: {nutrient: {age_range: {gender: amount}}}

RDA_DATABASE = {
    # PROTEIN (g per kg body weight)
    "protein": {
        "calculation": "weight_based",  # 0.8g per kg
        "base_amount": 0.8,
        "unit": "g"
    },
    
    # OMEGA-3 FATTY ACIDS
    "omega-3": {
        "19-50": {"male": 1.6, "female": 1.1},
        "51+": {"male": 1.6, "female": 1.1},
        "unit": "g",
        "note": "ALA (alpha-linolenic acid) - converts to DHA/EPA"
    },
    
    # MINERALS
    "iron": {
        "19-50": {"male": 8, "female": 18},
        "51+": {"male": 8, "female": 8},
        "unit": "mg",
        "note": "Plant-based iron - pair with vitamin C for better absorption"
    },
    
    "calcium": {
        "19-50": {"male": 1000, "female": 1000},
        "51-70": {"male": 1000, "female": 1200},
        "71+": {"male": 1200, "female": 1200},
        "unit": "mg"
    },
    
    "zinc": {
        "19+": {"male": 11, "female": 8},
        "unit": "mg",
        "note": "Important for immune function. Plant sources abundant."
    },
    
    "magnesium": {
        "19-30": {"male": 400, "female": 310},
        "31+": {"male": 420, "female": 320},
        "unit": "mg"
    },
    
    "selenium": {
        "19+": {"male": 55, "female": 55},
        "unit": "mcg",
        "note": "Just 1-2 Brazil nuts covers daily need!"
    },
    
    "iodine": {
        "19+": {"male": 150, "female": 150},
        "unit": "mcg"
    },
    
    "potassium": {
        "19+": {"male": 3400, "female": 2600},
        "unit": "mg"
    },
    
    "phosphorus": {
        "19+": {"male": 700, "female": 700},
        "unit": "mg"
    },
    
    "manganese": {
        "19+": {"male": 2.3, "female": 1.8},
        "unit": "mg"
    },
    
    "copper": {
        "19+": {"male": 900, "female": 900},
        "unit": "mcg"
    },
    
    # B VITAMINS
    "vitamin-b12": {
        "19+": {"male": 2.4, "female": 2.4},
        "unit": "mcg",
        "note": "Take a B12 supplement - most livestock get B12 supplements too!"
    },
    
    "vitamin-b1": {  # Thiamin
        "19+": {"male": 1.2, "female": 1.1},
        "unit": "mg"
    },
    
    "thiamin": {  # Alias for B1
        "19+": {"male": 1.2, "female": 1.1},
        "unit": "mg"
    },
    
    "vitamin-b2": {  # Riboflavin
        "19+": {"male": 1.3, "female": 1.1},
        "unit": "mg"
    },
    
    "riboflavin": {  # Alias for B2
        "19+": {"male": 1.3, "female": 1.1},
        "unit": "mg"
    },
    
    "vitamin-b3": {  # Niacin
        "19+": {"male": 16, "female": 14},
        "unit": "mg"
    },
    
    "niacin": {  # Alias for B3
        "19+": {"male": 16, "female": 14},
        "unit": "mg"
    },
    
    "vitamin-b5": {  # Pantothenic acid
        "19+": {"male": 5, "female": 5},
        "unit": "mg"
    },
    
    "pantothenic-acid": {  # Alias for B5
        "19+": {"male": 5, "female": 5},
        "unit": "mg"
    },
    
    "vitamin-b6": {  # Pyridoxine
        "19-50": {"male": 1.3, "female": 1.3},
        "51+": {"male": 1.7, "female": 1.5},
        "unit": "mg"
    },
    
    "pyridoxine": {  # Alias for B6
        "19-50": {"male": 1.3, "female": 1.3},
        "51+": {"male": 1.7, "female": 1.5},
        "unit": "mg"
    },
    
    "vitamin-b9": {  # Folate/Folic acid
        "19+": {"male": 400, "female": 400},
        "unit": "mcg"
    },
    
    "folate": {  # Alias for B9
        "19+": {"male": 400, "female": 400},
        "unit": "mcg"
    },
    
    "folic-acid": {  # Alias for B9
        "19+": {"male": 400, "female": 400},
        "unit": "mcg"
    },
    
    # FAT-SOLUBLE VITAMINS
    "vitamin-d": {
        "19-70": {"male": 600, "female": 600},
        "71+": {"male": 800, "female": 800},
        "unit": "IU",
        "note": "Get sunlight or take a supplement (D2 or vegan D3 from lichen)"
    },
    
    "vitamin-a": {
        "19+": {"male": 900, "female": 700},
        "unit": "mcg RAE",
        "note": "Plant foods provide beta-carotene which converts to vitamin A"
    },
    
    "vitamin-e": {
        "19+": {"male": 15, "female": 15},
        "unit": "mg"
    },
    
    "vitamin-k": {
        "19+": {"male": 120, "female": 90},
        "unit": "mcg"
    },
    
    # VITAMIN C
    "vitamin-c": {
        "19+": {"male": 90, "female": 75},
        "unit": "mg",
        "note": "Boosts iron absorption! Abundant in plant foods."
    },
    
    # CHOLINE (vitamin-like)
    "choline": {
        "19+": {"male": 550, "female": 425},
        "unit": "mg"
    },
}


# Comprehensive vegan food database with nutrient content
VEGAN_FOODS = {
    # ============================================================================
    # OMEGA-3 SOURCES
    # ============================================================================
    "omega-3": [
        {
            "name": "Ground Flaxseeds",
            "serving": "1 tbsp (7g)",
            "amount": 2.35,
            "unit": "g",
            "tips": "Grind fresh for best absorption - whole seeds pass through undigested",
            "cost": "$",
            "versatility": "Smoothies, oatmeal, baking, yogurt"
        },
        {
            "name": "Chia Seeds",
            "serving": "1 tbsp (12g)",
            "amount": 5.0,
            "unit": "g",
            "tips": "Soak in water for chia pudding or add to smoothies",
            "cost": "$",
            "versatility": "Pudding, smoothies, jams, egg replacer"
        },
        {
            "name": "Walnuts",
            "serving": "6 halves (14g)",
            "amount": 2.5,
            "unit": "g",
            "tips": "Also great for brain health!",
            "cost": "$$",
            "versatility": "Snack, salads, baking, pesto"
        },
        {
            "name": "Algae Oil (DHA/EPA)",
            "serving": "½ tsp",
            "amount": 0.5,
            "unit": "g",
            "tips": "Direct DHA/EPA - no conversion needed! Where fish get their omega-3",
            "cost": "$$",
            "versatility": "Supplement form or add to smoothies"
        },
        {
            "name": "Hemp Seeds",
            "serving": "3 tbsp (30g)",
            "amount": 2.8,
            "unit": "g",
            "tips": "Complete protein source too!",
            "cost": "$$",
            "versatility": "Smoothies, salads, yogurt, oatmeal"
        }
    ],
    
    # ============================================================================
    # IRON SOURCES
    # ============================================================================
    "iron": [
        {
            "name": "Cooked Lentils",
            "serving": "1 cup (200g)",
            "amount": 6.6,
            "unit": "mg",
            "tips": "Pair with vitamin C (tomatoes, lemon) for better absorption",
            "cost": "$",
            "versatility": "Curries, soups, salads, dal"
        },
        {
            "name": "Spinach (cooked)",
            "serving": "1 cup (180g)",
            "amount": 6.4,
            "unit": "mg",
            "tips": "Cooking increases iron availability",
            "cost": "$",
            "versatility": "Sautéed, soups, curries, pasta"
        },
        {
            "name": "Tofu (firm)",
            "serving": "½ cup (126g)",
            "amount": 3.4,
            "unit": "mg",
            "tips": "Press before cooking for better texture",
            "cost": "$",
            "versatility": "Stir-fry, scrambles, grilled, curries"
        },
        {
            "name": "Fortified Cereal",
            "serving": "1 cup (40g)",
            "amount": 18.0,
            "unit": "mg",
            "tips": "Check label - some cereals provide 100% daily iron!",
            "cost": "$",
            "versatility": "Breakfast with plant milk"
        },
        {
            "name": "Pumpkin Seeds",
            "serving": "¼ cup (30g)",
            "amount": 4.2,
            "unit": "mg",
            "tips": "Also high in zinc and magnesium",
            "cost": "$",
            "versatility": "Snack, salad topping, trail mix"
        }
    ],
    
    # ============================================================================
    # PROTEIN SOURCES
    # ============================================================================
    "protein": [
        {
            "name": "Cooked Lentils",
            "serving": "1 cup (200g)",
            "amount": 18,
            "unit": "g",
            "tips": "Also provides fiber and iron",
            "cost": "$",
            "versatility": "Curries, soups, salads, dal"
        },
        {
            "name": "Tempeh",
            "serving": "½ cup (85g)",
            "amount": 15,
            "unit": "g",
            "tips": "Fermented soy, more protein than tofu",
            "cost": "$$",
            "versatility": "Marinate and grill, crumble for tacos"
        },
        {
            "name": "Cooked Chickpeas",
            "serving": "1 cup (164g)",
            "amount": 15,
            "unit": "g",
            "tips": "Versatile and affordable protein source",
            "cost": "$",
            "versatility": "Hummus, curries, roasted snack"
        },
        {
            "name": "Black Beans (cooked)",
            "serving": "1 cup (172g)",
            "amount": 15,
            "unit": "g",
            "tips": "Complete protein when paired with rice",
            "cost": "$",
            "versatility": "Burritos, soups, burgers"
        },
        {
            "name": "Tofu (firm)",
            "serving": "½ cup (126g)",
            "amount": 10,
            "unit": "g",
            "tips": "Press and marinate for best flavor",
            "cost": "$",
            "versatility": "Stir-fry, scrambles, baked, grilled"
        }
    ],
    
    # ============================================================================
    # B12 SOURCES
    # ============================================================================
    "vitamin-b12": [
        {
            "name": "B12 Supplement",
            "serving": "1 tablet",
            "amount": 25,
            "unit": "mcg",
            "tips": "Take 25-100mcg daily or 1000mcg twice weekly",
            "cost": "$",
            "versatility": "Supplement - cyanocobalamin or methylcobalamin"
        },
        {
            "name": "Fortified Nutritional Yeast",
            "serving": "1 tbsp (5g)",
            "amount": 2.4,
            "unit": "mcg",
            "tips": "Adds cheesy flavor! Check label for fortification",
            "cost": "$",
            "versatility": "Pasta, popcorn, sauces, 'parmesan'"
        },
        {
            "name": "Fortified Plant Milk",
            "serving": "1 cup (240ml)",
            "amount": 1.2,
            "unit": "mcg",
            "tips": "Check label - not all brands fortify",
            "cost": "$",
            "versatility": "Cereal, coffee, smoothies, cooking"
        },
        {
            "name": "Fortified Cereal",
            "serving": "¾ cup (30g)",
            "amount": 6.0,
            "unit": "mcg",
            "tips": "Check label for B12 content",
            "cost": "$",
            "versatility": "Breakfast with plant milk"
        }
    ],
    
    # ============================================================================
    # CALCIUM SOURCES
    # ============================================================================
    "calcium": [
        {
            "name": "Fortified Plant Milk",
            "serving": "1 cup (240ml)",
            "amount": 300,
            "unit": "mg",
            "tips": "Shake well - calcium settles at bottom!",
            "cost": "$",
            "versatility": "Cereal, coffee, smoothies, cooking"
        },
        {
            "name": "Tofu (calcium-set)",
            "serving": "½ cup (126g)",
            "amount": 434,
            "unit": "mg",
            "tips": "Look for calcium sulfate in ingredients",
            "cost": "$",
            "versatility": "Stir-fry, scrambles, smoothies"
        },
        {
            "name": "Collard Greens (cooked)",
            "serving": "1 cup (190g)",
            "amount": 268,
            "unit": "mg",
            "tips": "Better calcium absorption than dairy!",
            "cost": "$",
            "versatility": "Sautéed, soups, wraps"
        },
        {
            "name": "Tahini",
            "serving": "2 tbsp (30g)",
            "amount": 128,
            "unit": "mg",
            "tips": "Made from sesame seeds - great in sauces",
            "cost": "$$",
            "versatility": "Hummus, dressings, sauces"
        },
        {
            "name": "Fortified Orange Juice",
            "serving": "1 cup (240ml)",
            "amount": 350,
            "unit": "mg",
            "tips": "Check for calcium fortification",
            "cost": "$",
            "versatility": "Breakfast drink, smoothies"
        }
    ],
    
    # ============================================================================
    # ZINC SOURCES
    # ============================================================================
    "zinc": [
        {
            "name": "Hemp Seeds",
            "serving": "3 tbsp (30g)",
            "amount": 3.0,
            "unit": "mg",
            "tips": "Complete protein, great mineral source",
            "cost": "$$",
            "versatility": "Smoothies, yogurt, salads"
        },
        {
            "name": "Pumpkin Seeds (Pepitas)",
            "serving": "¼ cup (30g)",
            "amount": 2.9,
            "unit": "mg",
            "tips": "Roasted or raw, great source of minerals",
            "cost": "$",
            "versatility": "Snack, salad topping, trail mix"
        },
        {
            "name": "Oats (dry)",
            "serving": "½ cup (40g)",
            "amount": 1.5,
            "unit": "mg",
            "tips": "Affordable breakfast staple",
            "cost": "$",
            "versatility": "Oatmeal, overnight oats, baking"
        },
        {
            "name": "Chickpeas (cooked)",
            "serving": "1 cup (164g)",
            "amount": 2.5,
            "unit": "mg",
            "tips": "Also provides 15g protein!",
            "cost": "$",
            "versatility": "Hummus, curries, roasted snack"
        },
        {
            "name": "Cashews",
            "serving": "¼ cup (30g)",
            "amount": 1.6,
            "unit": "mg",
            "tips": "Creamy when blended for sauces",
            "cost": "$$",
            "versatility": "Snack, cashew cream, stir-fry"
        }
    ],
    
    # ============================================================================
    # VITAMIN D SOURCES (Limited vegan sources - supplementation recommended)
    # ============================================================================
    "vitamin-d": [
        {
            "name": "Vegan D3 Supplement (from lichen)",
            "serving": "1 capsule",
            "amount": 1000,
            "unit": "IU",
            "tips": "D3 more effective than D2. Get 15min sunlight daily if possible!",
            "cost": "$",
            "versatility": "Daily supplement"
        },
        {
            "name": "Fortified Plant Milk",
            "serving": "1 cup (240ml)",
            "amount": 100,
            "unit": "IU",
            "tips": "Check label - most brands fortify with D2",
            "cost": "$",
            "versatility": "Cereal, coffee, smoothies, cooking"
        },
        {
            "name": "Fortified Orange Juice",
            "serving": "1 cup (240ml)",
            "amount": 100,
            "unit": "IU",
            "tips": "Check for vitamin D fortification",
            "cost": "$",
            "versatility": "Breakfast drink"
        },
        {
            "name": "UV-Exposed Mushrooms",
            "serving": "3 oz (85g)",
            "amount": 400,
            "unit": "IU",
            "tips": "Look for UV-treated mushrooms or sun-dry your own!",
            "cost": "$$",
            "versatility": "Sautéed, soups, stir-fry"
        }
    ],
    
    # ============================================================================
    # VITAMIN C SOURCES
    # ============================================================================
    "vitamin-c": [
        {
            "name": "Red Bell Pepper (raw)",
            "serving": "1 medium (119g)",
            "amount": 152,
            "unit": "mg",
            "tips": "More vitamin C than oranges!",
            "cost": "$",
            "versatility": "Salads, stir-fry, raw snack"
        },
        {
            "name": "Orange",
            "serving": "1 medium (131g)",
            "amount": 70,
            "unit": "mg",
            "tips": "Classic vitamin C source",
            "cost": "$",
            "versatility": "Fresh fruit, juice, salads"
        },
        {
            "name": "Strawberries",
            "serving": "1 cup (152g)",
            "amount": 89,
            "unit": "mg",
            "tips": "Great in smoothies!",
            "cost": "$$",
            "versatility": "Fresh, smoothies, desserts"
        },
        {
            "name": "Broccoli (cooked)",
            "serving": "1 cup (156g)",
            "amount": 101,
            "unit": "mg",
            "tips": "Steam lightly to preserve vitamin C",
            "cost": "$",
            "versatility": "Steamed, stir-fry, roasted"
        },
        {
            "name": "Kiwi",
            "serving": "1 medium (69g)",
            "amount": 64,
            "unit": "mg",
            "tips": "Eat the skin for extra fiber!",
            "cost": "$$",
            "versatility": "Fresh fruit, smoothies, salads"
        }
    ],
    
    # ============================================================================
    # VITAMIN A SOURCES (as beta-carotene)
    # ============================================================================
    "vitamin-a": [
        {
            "name": "Sweet Potato (baked)",
            "serving": "1 medium (114g)",
            "amount": 1403,
            "unit": "mcg RAE",
            "tips": "One sweet potato = 150% daily need!",
            "cost": "$",
            "versatility": "Baked, mashed, fries, curry"
        },
        {
            "name": "Carrot (raw)",
            "serving": "1 large (72g)",
            "amount": 601,
            "unit": "mcg RAE",
            "tips": "Beta-carotene converts to vitamin A",
            "cost": "$",
            "versatility": "Raw snack, juiced, roasted, soups"
        },
        {
            "name": "Spinach (cooked)",
            "serving": "1 cup (180g)",
            "amount": 943,
            "unit": "mcg RAE",
            "tips": "Cooking increases nutrient availability",
            "cost": "$",
            "versatility": "Sautéed, soups, curries"
        },
        {
            "name": "Butternut Squash (cooked)",
            "serving": "1 cup (205g)",
            "amount": 1144,
            "unit": "mcg RAE",
            "tips": "Rich, creamy texture when roasted",
            "cost": "$",
            "versatility": "Roasted, soup, curry"
        }
    ],
    
    # ============================================================================
    # VITAMIN E SOURCES
    # ============================================================================
    "vitamin-e": [
        {
            "name": "Sunflower Seeds",
            "serving": "¼ cup (30g)",
            "amount": 12.3,
            "unit": "mg",
            "tips": "One serving = 80% daily need!",
            "cost": "$",
            "versatility": "Snack, salads, granola"
        },
        {
            "name": "Almonds",
            "serving": "1 oz (28g, ~23 almonds)",
            "amount": 7.3,
            "unit": "mg",
            "tips": "Also provides healthy fats",
            "cost": "$$",
            "versatility": "Snack, almond butter, baking"
        },
        {
            "name": "Spinach (cooked)",
            "serving": "1 cup (180g)",
            "amount": 3.7,
            "unit": "mg",
            "tips": "Powerhouse of multiple nutrients",
            "cost": "$",
            "versatility": "Sautéed, soups, curries"
        },
        {
            "name": "Avocado",
            "serving": "½ avocado (68g)",
            "amount": 2.1,
            "unit": "mg",
            "tips": "Also provides healthy monounsaturated fats",
            "cost": "$$",
            "versatility": "Toast, salads, guacamole"
        }
    ],
    
    # ============================================================================
    # VITAMIN K SOURCES
    # ============================================================================
    "vitamin-k": [
        {
            "name": "Kale (cooked)",
            "serving": "1 cup (130g)",
            "amount": 1062,
            "unit": "mcg",
            "tips": "One serving = 10x daily need!",
            "cost": "$",
            "versatility": "Sautéed, smoothies, salads"
        },
        {
            "name": "Spinach (cooked)",
            "serving": "1 cup (180g)",
            "amount": 888,
            "unit": "mcg",
            "tips": "Loaded with multiple vitamins",
            "cost": "$",
            "versatility": "Sautéed, soups, curries"
        },
        {
            "name": "Broccoli (cooked)",
            "serving": "1 cup (156g)",
            "amount": 220,
            "unit": "mcg",
            "tips": "Also provides vitamin C and fiber",
            "cost": "$",
            "versatility": "Steamed, roasted, stir-fry"
        },
        {
            "name": "Brussels Sprouts (cooked)",
            "serving": "1 cup (156g)",
            "amount": 218,
            "unit": "mcg",
            "tips": "Roast with olive oil for best flavor",
            "cost": "$",
            "versatility": "Roasted, sautéed"
        }
    ],
    
    # ============================================================================
    # B-VITAMIN SOURCES (Folate/B9)
    # ============================================================================
    "folate": [
        {
            "name": "Cooked Lentils",
            "serving": "1 cup (200g)",
            "amount": 358,
            "unit": "mcg",
            "tips": "Nearly 90% of daily need in one serving!",
            "cost": "$",
            "versatility": "Curries, soups, salads"
        },
        {
            "name": "Spinach (cooked)",
            "serving": "1 cup (180g)",
            "amount": 263,
            "unit": "mcg",
            "tips": "Nutrient powerhouse",
            "cost": "$",
            "versatility": "Sautéed, soups, curries"
        },
        {
            "name": "Black Beans (cooked)",
            "serving": "1 cup (172g)",
            "amount": 256,
            "unit": "mcg",
            "tips": "Also high in protein and fiber",
            "cost": "$",
            "versatility": "Burritos, soups, salads"
        },
        {
            "name": "Asparagus (cooked)",
            "serving": "1 cup (180g)",
            "amount": 268,
            "unit": "mcg",
            "tips": "Roast or steam lightly",
            "cost": "$$",
            "versatility": "Side dish, salads, pasta"
        }
    ],
    
    # ============================================================================
    # MAGNESIUM SOURCES
    # ============================================================================
    "magnesium": [
        {
            "name": "Pumpkin Seeds",
            "serving": "¼ cup (30g)",
            "amount": 168,
            "unit": "mg",
            "tips": "One serving = 40% daily need!",
            "cost": "$",
            "versatility": "Snack, salads, trail mix"
        },
        {
            "name": "Almonds",
            "serving": "1 oz (28g)",
            "amount": 76,
            "unit": "mg",
            "tips": "Great for heart health",
            "cost": "$$",
            "versatility": "Snack, almond butter, baking"
        },
        {
            "name": "Spinach (cooked)",
            "serving": "1 cup (180g)",
            "amount": 157,
            "unit": "mg",
            "tips": "Multiple nutrients in one food",
            "cost": "$",
            "versatility": "Sautéed, soups, curries"
        },
        {
            "name": "Black Beans (cooked)",
            "serving": "1 cup (172g)",
            "amount": 120,
            "unit": "mg",
            "tips": "Also high in protein",
            "cost": "$",
            "versatility": "Burritos, soups, salads"
        }
    ],
    
    # ============================================================================
    # SELENIUM SOURCES
    # ============================================================================
    "selenium": [
        {
            "name": "Brazil Nuts",
            "serving": "1-2 nuts (5g)",
            "amount": 95,
            "unit": "mcg",
            "tips": "DO NOT EAT MORE THAN 2/DAY - too much selenium is harmful!",
            "cost": "$$",
            "versatility": "Snack (limit to 1-2 daily)"
        },
        {
            "name": "Sunflower Seeds",
            "serving": "¼ cup (30g)",
            "amount": 22,
            "unit": "mcg",
            "tips": "Also high in vitamin E",
            "cost": "$",
            "versatility": "Snack, salads, granola"
        },
        {
            "name": "Brown Rice (cooked)",
            "serving": "1 cup (195g)",
            "amount": 19,
            "unit": "mcg",
            "tips": "Whole grain goodness",
            "cost": "$",
            "versatility": "Side dish, bowls, stir-fry"
        }
    ],
    
    # ============================================================================
    # POTASSIUM SOURCES
    # ============================================================================
    "potassium": [
        {
            "name": "White Beans (cooked)",
            "serving": "1 cup (179g)",
            "amount": 1004,
            "unit": "mg",
            "tips": "More potassium than a banana!",
            "cost": "$",
            "versatility": "Soups, salads, dips"
        },
        {
            "name": "Sweet Potato (baked)",
            "serving": "1 medium (114g)",
            "amount": 542,
            "unit": "mg",
            "tips": "Nutrient-dense and delicious",
            "cost": "$",
            "versatility": "Baked, mashed, fries"
        },
        {
            "name": "Banana",
            "serving": "1 medium (118g)",
            "amount": 422,
            "unit": "mg",
            "tips": "Classic potassium source",
            "cost": "$",
            "versatility": "Fresh, smoothies, baking"
        },
        {
            "name": "Spinach (cooked)",
            "serving": "1 cup (180g)",
            "amount": 839,
            "unit": "mg",
            "tips": "Nutrient powerhouse",
            "cost": "$",
            "versatility": "Sautéed, soups, curries"
        }
    ],
}


# Tips for better nutrient absorption
NUTRIENT_TIPS = {
    "iron": {
        "tip": "Plant-based iron (non-heme) is better absorbed with vitamin C",
        "enhancers": ["Vitamin C foods (citrus, tomatoes, bell peppers)", "Lemon juice on meals"],
        "inhibitors": ["Tea/coffee with meals", "Calcium supplements at same time"]
    },
    
    "calcium": {
        "tip": "Vitamin D helps calcium absorption",
        "enhancers": ["Vitamin D (sunlight or supplement)", "Spread intake throughout day"],
        "inhibitors": ["Excessive salt", "Too much caffeine"]
    },
    
    "zinc": {
        "tip": "Zinc competes with iron - take separately if supplementing both",
        "enhancers": ["Soaking/sprouting beans and grains"],
        "inhibitors": ["Phytates in grains (reduced by soaking)"]
    },
    
    "omega-3": {
        "tip": "Ground flaxseeds are better absorbed than whole seeds",
        "enhancers": ["Grind fresh", "Store in fridge"],
        "inhibitors": ["High omega-6 intake (vegetable oils)"]
    },
    
    "vitamin-d": {
        "tip": "15-30 minutes of sunlight exposure provides vitamin D",
        "enhancers": ["Take with fat-containing meals", "Supplement if limited sun"],
        "inhibitors": ["Sunscreen blocks D production"]
    },
    
    "vitamin-a": {
        "tip": "Beta-carotene (from plants) is better absorbed with fat",
        "enhancers": ["Eat with healthy fats (avocado, nuts, olive oil)"],
        "inhibitors": []
    },
    
    "vitamin-k": {
        "tip": "Fat-soluble vitamin - absorb better with dietary fat",
        "enhancers": ["Eat with healthy fats"],
        "inhibitors": []
    },
    
    "folate": {
        "tip": "Heat-sensitive - don't overcook vegetables",
        "enhancers": ["Lightly steam vegetables", "Eat raw leafy greens"],
        "inhibitors": ["Excessive cooking"]
    },
}


# Normalize nutrient names (handle variations)
NUTRIENT_ALIASES = {
    "omega3": "omega-3",
    "omega 3": "omega-3",
    "b12": "vitamin-b12",
    "b-12": "vitamin-b12",
    "vitamin b12": "vitamin-b12",
    "cobalamin": "vitamin-b12",
    
    "b1": "thiamin",
    "b-1": "thiamin",
    "vitamin b1": "thiamin",
    
    "b2": "riboflavin",
    "b-2": "riboflavin",
    "vitamin b2": "riboflavin",
    
    "b3": "niacin",
    "b-3": "niacin",
    "vitamin b3": "niacin",
    
    "b5": "pantothenic-acid",
    "b-5": "pantothenic-acid",
    "vitamin b5": "pantothenic-acid",
    "pantothenic acid": "pantothenic-acid",
    
    "b6": "pyridoxine",
    "b-6": "pyridoxine",
    "vitamin b6": "pyridoxine",
    
    "b9": "folate",
    "b-9": "folate",
    "vitamin b9": "folate",
    "folic acid": "folate",
    
    "vitamin d": "vitamin-d",
    "vitamin d3": "vitamin-d",
    "vitamin d2": "vitamin-d",
    
    "vitamin a": "vitamin-a",
    "vitamin e": "vitamin-e",
    "vitamin k": "vitamin-k",
    "vitamin c": "vitamin-c",
    
    "vit a": "vitamin-a",
    "vit c": "vitamin-c",
    "vit d": "vitamin-d",
    "vit e": "vitamin-e",
    "vit k": "vitamin-k",
}