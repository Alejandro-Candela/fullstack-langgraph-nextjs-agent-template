import { NextRequest, NextResponse } from "next/server";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

/**
 * Proxy threads requests to Python backend
 */

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function GET() {
  try {
    const response = await fetch(`${BACKEND_URL}/api/agent/threads`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error("Error proxying to backend:", error);
    return NextResponse.json({ error: "Failed to fetch threads" }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    // Try to read body, but handle empty body gracefully
    let body = null;
    try {
      const text = await request.text();
      if (text) {
        body = JSON.parse(text);
      }
    } catch (e) {
      // No body or invalid JSON - that's ok
    }
    
    // If no body provided, create default thread data
    const threadData = body || { title: "New Conversation" };
    
    const response = await fetch(`${BACKEND_URL}/api/agent/threads`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(threadData),
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error("Error proxying to backend:", error);
    return NextResponse.json({ error: "Failed to create thread" }, { status: 500 });
  }
}
