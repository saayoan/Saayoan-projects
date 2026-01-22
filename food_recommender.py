# -*- coding: utf-8 -*-

@author: saayo
"""

"""
Food Recommendation System for Spyder
Based on gender, bodyweight, height, daily activity, and dietary preferences
"""


import math
from typing import List, Dict, Tuple

# Food database with nutritional info (calories per 100g)
FOOD_DATABASE = {
    "vegetarian": {
        "proteins": {
            "Tofu": {"calories": 76, "protein": 8, "carbs": 2, "fat": 4},
            "Lentils": {"calories": 116, "protein": 9, "carbs": 20, "fat": 0.4},
            "Chickpeas": {"calories": 164, "protein": 8.9, "carbs": 27, "fat": 2.6},
            "Greek Yogurt": {"calories": 59, "protein": 10, "carbs": 3.6, "fat": 0.4},
            "Quinoa": {"calories": 120, "protein": 4.4, "carbs": 22, "fat": 1.9},
            "Black Beans": {"calories": 132, "protein": 8.9, "carbs": 24, "fat": 0.5},
            "Almonds": {"calories": 579, "protein": 21, "carbs": 22, "fat": 50},
        },
        "carbs": {
            "Brown Rice": {"calories": 111, "protein": 2.6, "carbs": 23, "fat": 0.9},
            "Sweet Potato": {"calories": 86, "protein": 1.6, "carbs": 20, "fat": 0.1},
            "Oats": {"calories": 389, "protein": 17, "carbs": 66, "fat": 7},
            "Whole Wheat Bread": {"calories": 247, "protein": 13, "carbs": 41, "fat": 4.2},
        },
        "vegetables": {
            "Broccoli": {"calories": 34, "protein": 2.8, "carbs": 7, "fat": 0.4},
            "Spinach": {"calories": 23, "protein": 2.9, "carbs": 3.6, "fat": 0.4},
            "Bell Peppers": {"calories": 31, "protein": 1, "carbs": 7, "fat": 0.3},
            "Carrots": {"calories": 41, "protein": 0.9, "carbs": 10, "fat": 0.2},
        },
        "fats": {
            "Avocado": {"calories": 160, "protein": 2, "carbs": 9, "fat": 15},
            "Olive Oil": {"calories": 884, "protein": 0, "carbs": 0, "fat": 100},
            "Walnuts": {"calories": 654, "protein": 15, "carbs": 14, "fat": 65},
        }
    },
    "vegan": {
        "proteins": {
            "Tempeh": {"calories": 193, "protein": 19, "carbs": 9, "fat": 11},
            "Lentils": {"calories": 116, "protein": 9, "carbs": 20, "fat": 0.4},
            "Chickpeas": {"calories": 164, "protein": 8.9, "carbs": 27, "fat": 2.6},
            "Quinoa": {"calories": 120, "protein": 4.4, "carbs": 22, "fat": 1.9},
            "Black Beans": {"calories": 132, "protein": 8.9, "carbs": 24, "fat": 0.5},
            "Almonds": {"calories": 579, "protein": 21, "carbs": 22, "fat": 50},
            "Chia Seeds": {"calories": 486, "protein": 17, "carbs": 42, "fat": 31},
        },
        "carbs": {
            "Brown Rice": {"calories": 111, "protein": 2.6, "carbs": 23, "fat": 0.9},
            "Sweet Potato": {"calories": 86, "protein": 1.6, "carbs": 20, "fat": 0.1},
            "Oats": {"calories": 389, "protein": 17, "carbs": 66, "fat": 7},
        },
        "vegetables": {
            "Broccoli": {"calories": 34, "protein": 2.8, "carbs": 7, "fat": 0.4},
            "Spinach": {"calories": 23, "protein": 2.9, "carbs": 3.6, "fat": 0.4},
            "Bell Peppers": {"calories": 31, "protein": 1, "carbs": 7, "fat": 0.3},
        },
        "fats": {
            "Avocado": {"calories": 160, "protein": 2, "carbs": 9, "fat": 15},
            "Olive Oil": {"calories": 884, "protein": 0, "carbs": 0, "fat": 100},
            "Walnuts": {"calories": 654, "protein": 15, "carbs": 14, "fat": 65},
        }
    },
    "omnivore": {
        "proteins": {
            "Chicken Breast": {"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6},
            "Salmon": {"calories": 208, "protein": 20, "carbs": 0, "fat": 12},
            "Eggs": {"calories": 155, "protein": 13, "carbs": 1.1, "fat": 11},
            "Lean Beef": {"calories": 250, "protein": 26, "carbs": 0, "fat": 17},
            "Turkey": {"calories": 189, "protein": 29, "carbs": 0, "fat": 7},
            "Tuna": {"calories": 144, "protein": 30, "carbs": 0, "fat": 1},
            "Greek Yogurt": {"calories": 59, "protein": 10, "carbs": 3.6, "fat": 0.4},
        },
        "carbs": {
            "Brown Rice": {"calories": 111, "protein": 2.6, "carbs": 23, "fat": 0.9},
            "Sweet Potato": {"calories": 86, "protein": 1.6, "carbs": 20, "fat": 0.1},
            "Oats": {"calories": 389, "protein": 17, "carbs": 66, "fat": 7},
            "Whole Wheat Bread": {"calories": 247, "protein": 13, "carbs": 41, "fat": 4.2},
        },
        "vegetables": {
            "Broccoli": {"calories": 34, "protein": 2.8, "carbs": 7, "fat": 0.4},
            "Spinach": {"calories": 23, "protein": 2.9, "carbs": 3.6, "fat": 0.4},
            "Bell Peppers": {"calories": 31, "protein": 1, "carbs": 7, "fat": 0.3},
            "Carrots": {"calories": 41, "protein": 0.9, "carbs": 10, "fat": 0.2},
        },
        "fats": {
            "Avocado": {"calories": 160, "protein": 2, "carbs": 9, "fat": 15},
            "Olive Oil": {"calories": 884, "protein": 0, "carbs": 0, "fat": 100},
            "Walnuts": {"calories": 654, "protein": 15, "carbs": 14, "fat": 65},
        }
    },
    "keto": {
        "proteins": {
            "Chicken Breast": {"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6},
            "Salmon": {"calories": 208, "protein": 20, "carbs": 0, "fat": 12},
            "Eggs": {"calories": 155, "protein": 13, "carbs": 1.1, "fat": 11},
            "Bacon": {"calories": 541, "protein": 37, "carbs": 1.4, "fat": 42},
            "Beef": {"calories": 250, "protein": 26, "carbs": 0, "fat": 17},
        },
        "vegetables": {
            "Spinach": {"calories": 23, "protein": 2.9, "carbs": 3.6, "fat": 0.4},
            "Broccoli": {"calories": 34, "protein": 2.8, "carbs": 7, "fat": 0.4},
            "Cauliflower": {"calories": 25, "protein": 1.9, "carbs": 5, "fat": 0.3},
            "Zucchini": {"calories": 17, "protein": 1.2, "carbs": 3.4, "fat": 0.2},
        },
        "fats": {
            "Avocado": {"calories": 160, "protein": 2, "carbs": 9, "fat": 15},
            "Olive Oil": {"calories": 884, "protein": 0, "carbs": 0, "fat": 100},
            "Butter": {"calories": 717, "protein": 0.9, "carbs": 0.1, "fat": 81},
            "Coconut Oil": {"calories": 862, "protein": 0, "carbs": 0, "fat": 100},
        }
    }
}

# Activity multipliers
ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,      # Little to no exercise
    "light": 1.375,        # Light exercise 1-3 days/week
    "moderate": 1.55,      # Moderate exercise 3-5 days/week
    "active": 1.725,       # Hard exercise 6-7 days/week
    "very_active": 1.9    # Very hard exercise, physical job
}


def calculate_bmr(gender: str, weight_kg: float, height_cm: float, age: int = 30) -> float:
    """
    Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation
    """
    if gender.lower() in ["male", "m"]:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:  # female
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    return bmr


def calculate_tdee(bmr: float, activity_level: str) -> float:
    """
    Calculate Total Daily Energy Expenditure
    """
    multiplier = ACTIVITY_MULTIPLIERS.get(activity_level.lower(), 1.2)
    return bmr * multiplier


def get_food_recommendations(
    dietary_preference: str,
    daily_calories: float,
    meals_per_day: int = 3
) -> List[Dict]:
    """
    Generate food recommendations based on dietary preference and calorie needs
    """
    if dietary_preference.lower() not in FOOD_DATABASE:
        dietary_preference = "omnivore"  # Default
    
    food_db = FOOD_DATABASE[dietary_preference.lower()]
    calories_per_meal = daily_calories / meals_per_day
    
    recommendations = []
    
    # Macro distribution (approximate)
    protein_ratio = 0.30  # 30% calories from protein
    carb_ratio = 0.40     # 40% calories from carbs (0% for keto)
    fat_ratio = 0.30      # 30% calories from fat
    
    if dietary_preference.lower() == "keto":
        carb_ratio = 0.05  # 5% for keto
        fat_ratio = 0.65   # 65% for keto
    
    for meal_num in range(1, meals_per_day + 1):
        meal = {
            "meal": f"Meal {meal_num}",
            "foods": [],
            "total_calories": 0,
            "protein_g": 0,
            "carbs_g": 0,
            "fat_g": 0
        }
        
        # Add protein source
        proteins = list(food_db["proteins"].items())
        if proteins:
            protein_name, protein_info = proteins[meal_num % len(proteins)]
            protein_cals = calories_per_meal * protein_ratio
            protein_grams = (protein_cals / protein_info["calories"]) * 100
            meal["foods"].append({
                "name": protein_name,
                "amount_g": round(protein_grams, 1),
                "calories": round(protein_cals, 1)
            })
            meal["total_calories"] += protein_cals
            meal["protein_g"] += (protein_grams / 100) * protein_info["protein"]
        
        # Add carb source (skip for keto)
        if dietary_preference.lower() != "keto" and "carbs" in food_db:
            carbs = list(food_db["carbs"].items())
            if carbs:
                carb_name, carb_info = carbs[meal_num % len(carbs)]
                carb_cals = calories_per_meal * carb_ratio
                carb_grams = (carb_cals / carb_info["calories"]) * 100
                meal["foods"].append({
                    "name": carb_name,
                    "amount_g": round(carb_grams, 1),
                    "calories": round(carb_cals, 1)
                })
                meal["total_calories"] += carb_cals
                meal["carbs_g"] += (carb_grams / 100) * carb_info["carbs"]
        
        # Add vegetable
        if "vegetables" in food_db:
            veggies = list(food_db["vegetables"].items())
            if veggies:
                veg_name, veg_info = veggies[meal_num % len(veggies)]
                veg_cals = calories_per_meal * 0.10  # 10% from vegetables
                veg_grams = (veg_cals / veg_info["calories"]) * 100
                meal["foods"].append({
                    "name": veg_name,
                    "amount_g": round(veg_grams, 1),
                    "calories": round(veg_cals, 1)
                })
                meal["total_calories"] += veg_cals
                meal["carbs_g"] += (veg_grams / 100) * veg_info.get("carbs", 0)
        
        # Add healthy fat
        if "fats" in food_db:
            fats = list(food_db["fats"].items())
            if fats:
                fat_name, fat_info = fats[meal_num % len(fats)]
                fat_cals = calories_per_meal * fat_ratio
                fat_grams = (fat_cals / fat_info["calories"]) * 100
                meal["foods"].append({
                    "name": fat_name,
                    "amount_g": round(fat_grams, 1),
                    "calories": round(fat_cals, 1)
                })
                meal["total_calories"] += fat_cals
                meal["fat_g"] += (fat_grams / 100) * fat_info["fat"]
        
        # Round totals
        meal["total_calories"] = round(meal["total_calories"], 1)
        meal["protein_g"] = round(meal["protein_g"], 1)
        meal["carbs_g"] = round(meal["carbs_g"], 1)
        meal["fat_g"] = round(meal["fat_g"], 1)
        
        recommendations.append(meal)
    
    return recommendations


def print_recommendations(recommendations: List[Dict], tdee: float):
    """
    Pretty print the food recommendations
    """
    print("\n" + "="*60)
    print("FOOD RECOMMENDATIONS")
    print("="*60)
    print(f"\nDaily Calorie Target: {tdee:.0f} calories")
    print(f"Total Meals: {len(recommendations)}\n")
    
    for meal in recommendations:
        print(f"\n{meal['meal']}:")
        print("-" * 40)
        for food in meal["foods"]:
            print(f"  • {food['name']}: {food['amount_g']}g ({food['calories']:.0f} cal)")
        print(f"\n  Meal Totals: {meal['total_calories']:.0f} cal | "
              f"Protein: {meal['protein_g']:.1f}g | "
              f"Carbs: {meal['carbs_g']:.1f}g | "
              f"Fat: {meal['fat_g']:.1f}g")
    
    # Daily totals
    daily_totals = {
        "calories": sum(m["total_calories"] for m in recommendations),
        "protein": sum(m["protein_g"] for m in recommendations),
        "carbs": sum(m["carbs_g"] for m in recommendations),
        "fat": sum(m["fat_g"] for m in recommendations)
    }
    
    print("\n" + "="*60)
    print("DAILY TOTALS:")
    print(f"  Calories: {daily_totals['calories']:.0f} cal")
    print(f"  Protein: {daily_totals['protein']:.1f}g")
    print(f"  Carbs: {daily_totals['carbs']:.1f}g")
    print(f"  Fat: {daily_totals['fat']:.1f}g")
    print("="*60 + "\n")


def main():
    """
    Main function to get user input and generate recommendations
    """
    print("="*60)
    print("FOOD RECOMMENDATION SYSTEM")
    print("="*60)
    print("\nPlease provide the following information:\n")
    
    # Get user inputs
    gender = input("Gender (male/female): ").strip()
    weight_kg = float(input("Body weight (kg): "))
    height_cm = float(input("Height (cm): "))
    age = int(input("Age (years) [default: 30]: ") or "30")
    
    print("\nActivity levels:")
    print("  - sedentary: Little to no exercise")
    print("  - light: Light exercise 1-3 days/week")
    print("  - moderate: Moderate exercise 3-5 days/week")
    print("  - active: Hard exercise 6-7 days/week")
    print("  - very_active: Very hard exercise, physical job")
    
    activity = input("\nDaily activity level: ").strip()
    
    print("\nDietary preferences:")
    print("  - omnivore: All foods")
    print("  - vegetarian: No meat, includes dairy/eggs")
    print("  - vegan: No animal products")
    print("  - keto: Low carb, high fat")
    
    dietary_pref = input("\nDietary preference: ").strip()
    meals_per_day = int(input("Meals per day [default: 3]: ") or "3")
    
    # Calculate
    bmr = calculate_bmr(gender, weight_kg, height_cm, age)
    tdee = calculate_tdee(bmr, activity)
    
    print(f"\nYour BMR (Basal Metabolic Rate): {bmr:.0f} calories/day")
    print(f"Your TDEE (Total Daily Energy Expenditure): {tdee:.0f} calories/day")
    
    # Get recommendations
    recommendations = get_food_recommendations(dietary_pref, tdee, meals_per_day)
    
    # Print results
    print_recommendations(recommendations, tdee)


if __name__ == "__main__":

    main()
