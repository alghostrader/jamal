# Build Spec — Xtream ⇄ M3U URL Generator (client-side)

**Site:** iptvesp.com · **Type:** Tier-2 link magnet #3 · **Market:** the Spanish "listas iptv" cluster (1,900/mo)
**Absolute rule:** 100% client-side. Credentials/URLs never leave the browser — no network calls,
no storage, visible privacy note ("Nada sale de tu dispositivo — todo se procesa en tu navegador").

## What it is
Not a file converter — a URL builder/parser:
- Xtream → M3U: (servidor, usuario, contraseña) → `http://SERVER/get.php?username=U&password=P&type=m3u_plus&output=ts` (+ variants) with copy button
- M3U → Xtream: paste a get.php URL → parsed server/user/pass + player-ready fields
- Bonus: EPG URL (`xmltv.php`) generated alongside

## Page
`/generador-m3u` — "Generador M3U ⇄ Xtream: convierte tus datos IPTV (2026)". Two tabs
(Xtream→M3U / M3U→Xtream), copy-to-clipboard, per-field validation, FAQ (4 items: qué es
xtream, es seguro [sí: client-side], funciona con cualquier proveedor, cómo usar la lista en
VLC/Smarters). SoftwareApplication + FAQPage JSON-LD. 600+ words of supporting ES copy around
the tool (qué es una lista m3u, xtream codes api, etc.). Static page + one client component.

## Copy-paste prompt
```
>>> TARGET WEBSITE: iptvesp.com <<<
Switch to the iptvesp.com project. Do NOT touch any other site.

Build /generador-m3u — a 100% client-side Xtream ⇄ M3U URL generator (Spanish):
1. Tab "Xtream → M3U": inputs servidor (URL), usuario, contraseña → generates
   get.php?username=..&password=..&type=m3u_plus&output=ts URL (+ output=m3u8 variant) and the
   EPG URL (xmltv.php?...). Copy-to-clipboard buttons. Validate inputs client-side.
2. Tab "M3U → Xtream": paste a get.php URL → parse and display servidor/usuario/contraseña.
3. HARD RULE: zero network calls with user data, zero storage — pure in-browser string work.
   Show the privacy note "🔒 Nada sale de tu dispositivo — todo se procesa en tu navegador."
4. Page: H1 "Generador M3U ⇄ Xtream", title ≤60 keyword-first ("Generador M3U desde Xtream
   Codes (2026) — gratis"), meta ≤160, 600+ words ES supporting copy (qué es una lista M3U /
   Xtream Codes API / cómo usarla en VLC, IPTV Smarters, TiviMate), FAQ 4 items.
   SoftwareApplication + FAQPage JSON-LD, self-canonical, add to sitemap.xml.
5. Internal links: one link from /blog/telegram-listas-iptv-espana and the listas-related posts;
   one contextual CTA to /suscripciones ("¿Buscas un servicio con listas siempre actualizadas?").
6. Design: existing components/tokens, static page + one small client component, Lighthouse ≥90.
VERIFY: route 200 server-rendered (copy visible in view-source); generator works with a dummy
example (server=http://ejemplo.com:8080, user=test, pass=1234) shown as placeholder; JSON-LD
valid; no fetch/XHR containing user input (check the bundle); sitemap updated.
Commits: feat(generador-m3u): <item>.
```
