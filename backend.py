from fastapi import FastAPI
from enum import Enum

app = FastAPI()

food_items = {
    'indian': ['samosa', 'dosa'],
    'american': ['hot dog', 'apple pie'],
    'italian': ['pizza', 'lasagna']
}

class AvailableCuisines(str, Enum):
    indian = 'indian'
    american = 'american'
    italian = 'italian'

@app.get("/get_items/{region}")
async def fetch_menu(region: AvailableCuisines):

    """ ## manual validation
    if region not in food_items.keys():
        return f"supported cusinie are {food_items.keys()}"
    """

    return food_items.get(region)

coupon_code = {
    1: "10%",
    2: "20%",
    3: "30%"
}

@app.get("/apply_coupon/{code}")
async def check_code(code: int):
    return coupon_code.get(code)