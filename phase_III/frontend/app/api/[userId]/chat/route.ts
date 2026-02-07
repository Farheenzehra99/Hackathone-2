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

const forward = async (req: Request, url: string, bodyText: string) => {
  const res = await fetch(url, {
    method: "POST",
    headers: buildHeaders(req),
    cache: "no-store",
    body: bodyText,
  });

  const contentType = res.headers.get("content-type") || "";
  const body = contentType.includes("application/json")
    ? await res.json()
    : await res.text();

  return NextResponse.json(body, { status: res.status });
};

export async function POST(
  req: Request,
  { params }: { params: { userId: string } }
) {
  const bodyText = await req.text();

  // Primary: /{userId}/chat (current backend)
  const primaryUrl = `${HF_API_BASE}/${params.userId}/chat`;
  const primaryResponse = await forward(req, primaryUrl, bodyText);

  if (primaryResponse.status !== 404 && primaryResponse.status !== 405) {
    return primaryResponse;
  }

  // Fallback: /chat (older backend shape)
  const fallbackUrl = `${HF_API_BASE}/chat`;
  return forward(req, fallbackUrl, bodyText);
}
