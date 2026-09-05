// Edge Middleware: HTTP Basic Auth for the whole dashboard (all pages, incl. sales/clients).
// Credentials come from Vercel environment variables DASH_USER / DASH_PASS when set;
// the fallbacks below are used until the owner sets them (Vercel → Settings → Environment Variables → redeploy).
export const config = { matcher: "/:path*" };

export default function middleware(request) {
  const user = process.env.DASH_USER || "iptv";
  const pass = process.env.DASH_PASS || "YtPXaKyplbOupt";
  const auth = request.headers.get("authorization") || "";
  if (auth.startsWith("Basic ")) {
    let decoded = "";
    try { decoded = atob(auth.slice(6)); } catch (e) { decoded = ""; }
    const i = decoded.indexOf(":");
    const u = decoded.slice(0, i), p = decoded.slice(i + 1);
    if (u === user && p === pass) return; // authorised → serve the static page
  }
  return new Response("Authentication required", {
    status: 401,
    headers: { "WWW-Authenticate": 'Basic realm="IPTV Portfolio", charset="UTF-8"',
               "Cache-Control": "no-store" },
  });
}
