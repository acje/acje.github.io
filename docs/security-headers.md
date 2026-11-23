# Security headers on GitHub Pages

GitHub Pages cannot set HTTP response headers, so no `<meta http-equiv>`
tag can produce a real header.

Browsers ignore `X-Frame-Options`, `X-XSS-Protection` and
`Content-Security-Policy` in meta form: `XSS-Protection` is deprecated and
withdrawn, and frame-ancestors cannot be expressed by a meta CSP. Keeping
them advertised protection the site did not have, so they were removed.

Among the remaining markup only `<meta name="referrer">` is honoured:
`Referrer-Policy: strict-origin-when-cross-origin`.

`X-Content-Type-Options: nosniff` was removed too, since browsers honour
it only as a real header. Serve it, HSTS, frame-ancestors and CSP from a
proxy/CDN in front of Pages.
