import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

/**
 * Proxy history requests to Python backend
 */

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function GET(_req: Request, { params }: { params: Promise<{ threadId: string }> }) {
  try {
    const { threadId } = await params;

    const response = await fetch(`${BACKEND_URL}/api/agent/history/${threadId}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error("Error proxying to backend:", error);
    return NextResponse.json({ error: "Failed to fetch thread history" }, { status: 500 });
  }
}
