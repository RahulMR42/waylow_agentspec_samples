from wayflowcore.tools import tool
from typing import Annotated

@tool("check_temperature")
def temperature_check(
    city_name: Annotated[str, "Name of the city"]) -> str:
    """
    Tool to provide temperature of a city 
    """
    return f"Temperature in {city_name} is -10F"