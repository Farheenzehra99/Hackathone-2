import { proxyRequest } from "../../_proxy";

export async function POST(
  req: Request,
  { params }: { params: { userId: string } }
) {
  return proxyRequest(req, `/${params.userId}/chat`);
}
