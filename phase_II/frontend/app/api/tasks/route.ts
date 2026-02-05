import { proxyRequest } from "../_proxy";

export async function GET(req: Request) {
  return proxyRequest(req, "/tasks");
}

export async function POST(req: Request) {
  return proxyRequest(req, "/tasks");
}
