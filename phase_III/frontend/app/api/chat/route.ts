import { NextResponse } from "next/server";

const HF_API_BASE =
  process.env.HF_API_BASE || "https://farheenzehra99-phase-2.hf.space/api/v1";

const buildHeaders = (req: Request) => {
  const headers = new Headers();
  const contentType = req.headers.get("content-type");
  const authorization = req.headers.get("authorization");

  if (contentType) headers.set("content-type", contentType);
  if (authorization) headers.set("authorization", authorization);

  return headers;
};

export async function POST(req: Request) {
  let payload: { user_id?: string; message?: string; conversation_id?: string | null };
  try {
    payload = await req.json();
  } catch {
    return NextResponse.json(
      { success: false, error: { code: "INVALID_JSON", message: "Invalid JSON" } },
      { status: 400 }
    );
  }

  const userId = payload.user_id;
  if (!userId) {
    return NextResponse.json(
      { success: false, error: { code: "MISSING_USER_ID", message: "user_id is required" } },
      { status: 400 }
    );
  }

  const url = `${HF_API_BASE}/${userId}/chat`;

  const res = await fetch(url, {
    method: "POST",
    headers: buildHeaders(req),
    cache: "no-store",
    body: JSON.stringify({
      message: payload.message,
      conversation_id: payload.conversation_id ?? null,
    }),
  });

  const contentType = res.headers.get("content-type") || "";
  const body = contentType.includes("application/json")
    ? await res.json()
    : await res.text();

  return NextResponse.json(body, { status: res.status });
}
