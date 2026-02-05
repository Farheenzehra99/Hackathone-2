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

export const proxyRequest = async (req: Request, path: string) => {
  const url = `${HF_API_BASE}${path}`;
  const method = req.method.toUpperCase();

  const init: RequestInit = {
    method,
    headers: buildHeaders(req),
    cache: "no-store",
  };

  if (!["GET", "HEAD", "OPTIONS"].includes(method)) {
    init.body = await req.text();
  }

  const res = await fetch(url, init);
  const contentType = res.headers.get("content-type") || "";
  const body = contentType.includes("application/json")
    ? await res.json()
    : await res.text();

  return NextResponse.json(body, { status: res.status });
};
