from google.adk.a2a.utils.agent_to_a2a import to_a2a
from .agent import root_agent

app = to_a2a(root_agent, port=8002)