# acje.github.io

Anders Jensen's personal site. Built with [Hugo](https://gohugo.io/) and
the [hugo-book](https://themes.gohugo.io/themes/hugo-book/) theme.
Deployed to GitHub Pages by
[`.github/workflows/hugo.yaml`](.github/workflows/hugo.yaml) on push to `main`.

## Build locally

```
hugo server
```

`hugo server -D` additionally renders drafts, which the deploy build never
publishes; use it only for previewing draft content.

## Gate locally, exactly as CI does

```
hugo build --gc --minify --baseURL "https://acje.github.io/" --panicOnWarning --printPathWarnings --printI18nWarnings
python3 scripts/check_site.py public
```

The checker takes the destination directory as its argument, so build to a
scratch directory (for example `--destination .ooda/tmp/site`) when you do not
want to disturb `public/`.

## Toolchain

Hugo is pinned in the `env:` block of
[`.github/workflows/hugo.yaml`](.github/workflows/hugo.yaml), together with its
release checksum; read that file for the version actually in use. There is no
Go toolchain in the build.

## Links

- [Manuscripts](docs/manuscripts.md) — unpublished book, kept outside the repo

- [Visual spacing authoring reference](docs/editorial/visual-spacing.md)

- https://gohugo.io/host-and-deploy/host-on-github-pages/
- https://themes.gohugo.io/
- https://themes.gohugo.io/themes/hugo-book/
