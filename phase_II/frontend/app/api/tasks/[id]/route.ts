import { proxyRequest } from "../../_proxy";

export async function PUT(req: Request, ctx: { params: { id: string } }) {
  return proxyRequest(req, `/tasks/${ctx.params.id}`);
}

export async function DELETE(req: Request, ctx: { params: { id: string } }) {
  return proxyRequest(req, `/tasks/${ctx.params.id}`);
}
