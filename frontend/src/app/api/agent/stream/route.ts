import { NextRequest } from "next/server";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

/**
 * SSE proxy endpoint that forwards requests to the Python FastAPI backend.
 * This eliminates the need for LangGraph.js logic in the frontend.
 */
export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  
  // Get backend URL from environment or default
  const backendUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  
  // Forward all query parameters to the backend
  const backendStreamUrl = `${backendUrl}/api/agent/stream?${searchParams.toString()}`;

  try {
    // Fetch from Python backend
    const response = await fetch(backendStreamUrl, {
      method: "GET",
      headers: {
        "Accept": "text/event-stream",
      },
    });

    if (!response.ok) {
      throw new Error(`Backend returned ${response.status}: ${response.statusText}`);
    }

    // Return the SSE stream directly from backend
    return new Response(response.body, {
      headers: {
        "Content-Type": "text/event-stream; charset=utf-8",
        "Cache-Control": "no-cache, no-transform",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no",
      },
    });
  } catch (error) {
    console.error("Error proxying to backend:", error);
    
    // Return error as SSE
    const errorStream = new ReadableStream({
      start(controller) {
        const encoder = new TextEncoder();
        const errorMessage = error instanceof Error ? error.message : "Unknown error";
        controller.enqueue(
          encoder.encode(`event: error\ndata: ${JSON.stringify({ message: errorMessage })}\n\n`)
        );
        controller.close();
      },
    });

    return new Response(errorStream, {
      headers: {
        "Content-Type": "text/event-stream; charset=utf-8",
        "Cache-Control": "no-cache",
      },
    });
  }
}
