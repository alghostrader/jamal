export const config = { matcher: '/(.*)' };

export default function middleware(req) {
  const auth = req.headers.get('authorization') || '';
  if (auth.startsWith('Basic ')) {
    try {
      const [, pass] = atob(auth.slice(6)).split(/:(.*)/s);
      if (pass === 'leblanc15M@$') return; // any username, this password
    } catch (e) {}
  }
  return new Response('Authentication required', {
    status: 401,
    headers: { 'WWW-Authenticate': 'Basic realm="IPTV SEO Dashboard", charset="UTF-8"' },
  });
}
