"""Test específico para la ruta de MCP tools."""

import asyncio
from app.agent.mcp import get_mcp_tools

async def test_get_tools():
    print("🔍 Probando get_mcp_tools()...")
    try:
        tools = await get_mcp_tools()
        print(f"✅ Éxito: Obtenidos {len(tools)} tools")
        print(f"   Tools: {tools}")
        return tools
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("Testing MCP tools function...\n")
    result = asyncio.run(test_get_tools())
    
    if result is not None:
        print("\n✅ La función get_mcp_tools() funciona correctamente")
        print(f"   Devuelve: {type(result)}")
        print(f"   Cantidad: {len(result)}")
    else:
        print("\n❌ Hay un problema con get_mcp_tools()")

