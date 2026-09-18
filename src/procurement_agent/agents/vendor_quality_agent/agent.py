from google.adk.agents import Agent
from dotenv import load_dotenv
load_dotenv()

QUALITY_DATA = {
    "vendor_a": {"defect_rate_pct": 1.2, "on_time_delivery_pct": 91},
    "vendor_b": {"defect_rate_pct": 0.4, "on_time_delivery_pct": 97},
}

def get_quality_rating(vendor: str) -> dict:
    """Return quality/reliability metrics for a given vendor (e.g. 'vendor_a', 'Vendor A')."""
    key = vendor.strip().lower().replace(" ", "_").replace("-", "_")
    return QUALITY_DATA.get(key, {"Error": f"Unknown vendor {vendor}"})

root_agent = Agent(
    model="gemini-3.5-flash-lite",
    name="vendor_quality_agent",
    instruction="You report vendor quality and reliability metrics. Use get_quality_rating.",
    tools=[get_quality_rating],
)