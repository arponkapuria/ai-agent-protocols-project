from google.adk.agents import Agent
from dotenv import load_dotenv
load_dotenv()

# Toy pricing logic standing in for a real vendor's system
CATALOG = {
    "steel_bolts": {
        "vendor_a": {"unit_price": 2.10, "lead_time_days": 5},
        "vendor_b": {"unit_price": 1.95, "lead_time_days": 3}
    }
}

def get_quote(component: str, quantity: int) -> dict:
    """Return a price quote from both known vendors for a component and quantity."""
    key = component.strip().lower().replace(" ", "_").replace("-", "_")
    if key not in CATALOG:
        return {"error": f"No pricing data for {component}"}
    return {
        vendor: {"total": round(info["unit_price"] * quantity, 2),
                 "lead_time_days": info["lead_time_days"]}
        for vendor, info in CATALOG[key].items()
    }

root_agent = Agent(
    model="gemini-3.5-flash-lite",
    name="vendor_pricing_agent",
    instruction="You provide price quotes for components across vendors. Use get_quote.",
    tools=[get_quote],
)