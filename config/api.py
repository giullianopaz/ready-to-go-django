from ninja import NinjaAPI, Schema

from apps.accounts.api import router as accounts_router
from apps.audit.api import router as audit_router

api = NinjaAPI(
    title="Ready to Go Django API",
    version="1.0.0",
    description="High-Velocity Django Monolith API with automatic OpenAPI documentation and AI Agent tool integration.",
    docs_url="/docs",
)

# Mount Routers
api.add_router("", accounts_router)
api.add_router("/audit", audit_router)


# ── AI Agent Tool Discovery & Execution (MCP) ────────────────────────────────


class MCPToolDefinition(Schema):
    name: str
    description: str
    parameters: dict


@api.get("/mcp/tools", response=list[MCPToolDefinition], tags=["AI & MCP"])
def list_mcp_tools(request):
    """
    Expose registered application capabilities as structured tool definitions
    compatible with Model Context Protocol (MCP) and LLM tool calling.
    """
    return [
        {
            "name": "get_system_health",
            "description": "Check current health of database, worker queue, and API server.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
        {
            "name": "lookup_user",
            "description": "Search user account details by username or email.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Username or email"},
                },
                "required": ["query"],
            },
        },
    ]


@api.post("/mcp/tools/execute", tags=["AI & MCP"])
def execute_mcp_tool(request, tool_name: str, arguments: dict):
    """Execute a structured tool invoked by an autonomous AI agent."""
    if tool_name == "get_system_health":
        from apps.core.views import health_check

        response = health_check(request)
        return {"result": response.content.decode("utf-8")}

    if tool_name == "lookup_user":
        from apps.accounts.models import User

        query = arguments.get("query", "")
        user = (
            User.objects.filter(username=query).first() or User.objects.filter(email=query).first()
        )
        if not user:
            return {"result": f"User '{query}' not found."}
        return {
            "result": {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat(),
            }
        }

    return {"error": f"Tool '{tool_name}' is not recognized."}
