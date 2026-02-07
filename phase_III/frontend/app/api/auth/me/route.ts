import { proxyRequest } from "../../_proxy";

export async function GET(req: Request) {
  return proxyRequest(req, "/auth/me");
}
