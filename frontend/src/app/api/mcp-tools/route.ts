import { NextResponse } from "next/server";

/**
 * Proxy endpoint for MCP tools - forwards to Python backend
 */
export async function GET() {
  try {
    // Get backend URL from environment
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    
    // Fetch from Python backend
    const response = await fetch(`${backendUrl}/api/mcp-servers/tools`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`Backend returned ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    
    // Transform backend response to match frontend format
    // Backend returns: { tools: [...], total: N }
    // Frontend expects: { serverGroups: {...}, totalCount: N }
    
    const tools = data.tools || [];
    const serverGroups: any = {};
    
    for (const tool of tools) {
      const serverName = tool.server || "default";
      
      if (!serverGroups[serverName]) {
        serverGroups[serverName] = {
          tools: [],
          count: 0,
        };
      }
      
      serverGroups[serverName].tools.push({
        name: tool.name,
        description: tool.description,
      });
      serverGroups[serverName].count++;
    }
    
    return NextResponse.json({
      serverGroups,
      totalCount: tools.length,
    });
  } catch (error) {
    console.error("Error fetching MCP tools from backend:", error);
    return NextResponse.json(
      {
        error: "Failed to fetch MCP tools",
        serverGroups: {},
        totalCount: 0,
      },
      { status: 500 },
    );
  }
}
