import { proxyRequest } from "../../../_proxy";

export async function PATCH(req: Request, ctx: { params: { id: string } }) {
  return proxyRequest(req, `/tasks/${ctx.params.id}/complete`);
}
