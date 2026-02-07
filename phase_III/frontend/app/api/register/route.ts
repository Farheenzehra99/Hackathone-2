import { NextResponse } from "next/server";

const HF_API_BASE =
  process.env.HF_API_BASE || "https://farheenzehra99-phase-2.hf.space/api/v1";

export async function POST(req: Request) {
  try {
    const body = await req.text();

    const res = await fetch(`${HF_API_BASE}/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body,
      cache: "no-store",
    });

    const contentType = res.headers.get("content-type") || "";
    const data = contentType.includes("application/json")
      ? await res.json()
      : await res.text();

    return NextResponse.json(data, { status: res.status });
  } catch {
    return NextResponse.json({ message: "Server error" }, { status: 500 });
  }
}
