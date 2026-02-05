import { proxyRequest } from "../_proxy";

export async function POST(req: Request) {
  return proxyRequest(req, "/login");
}
