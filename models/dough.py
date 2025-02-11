from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import List, Optional


class DoughType(Enum):
    BAO = "bao"
    BUN = "bun"
    WHOLE_WHEAT = "whole_wheat"
    WHITE = "white"
    SOURDOUGH = "sourdough"


class IngredientName(Enum):
    FLOUR = "flour"
    SALT = "salt"
    SUGAR = "sugar"
    WATER = "water"
    YEAST = "yeast"


class UnitType(Enum):
    GRAMS = "grams"
    KILOGRAM = "kilograms"
    LITERS = "liters"
    MILLILITERS = "milliliters"


class Ingredient(BaseModel):
    name: IngredientName
    brand: Optional[str]
    quantity: float
    unit_type: UnitType
    add_dt: List[datetime]


class Dough(BaseModel):
    dough_type: DoughType
    ingredients: List[Ingredient]
    hydration: float
    create_dt: datetime
    update_dt: datetime

    def _convert_unit_to_grams(self, ingredient: Ingredient) -> float:
        conversion_rates = {
            UnitType.GRAMS: 1,
            UnitType.KILOGRAM: 1000,
            UnitType.LITERS: 1000,
            UnitType.MILLILITERS: 1,
        }
        return ingredient.quantity * conversion_rates.get(ingredient.unit_type, 1)

    def calculate_hydration(self):
        flour_weight, water_weight = 0, 0
        for ingredient in self.ingredients:
            weight_in_grams = self._convert_unit_to_grams(ingredient)

            if ingredient.name == IngredientName.FLOUR:
                flour_weight += weight_in_grams
            if ingredient.name == IngredientName.WATER:
                water_weight += weight_in_grams

        if flour_weight == 0:
            return 0

        hydration = (water_weight / flour_weight) * 100
        return round(hydration, 2)
