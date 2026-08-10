# acje.github.io

Anders Jensen's personal site. Built with [Hugo](https://gohugo.io/) and
the [hugo-book](https://themes.gohugo.io/themes/hugo-book/) theme.
Deployed to GitHub Pages by
[`.github/workflows/hugo.yaml`](.github/workflows/hugo.yaml) on push to `main`.

## Build locally

```
hugo server -D
```

## Toolchain

Hugo and Go versions are pinned in the `env:` block of
[`.github/workflows/hugo.yaml`](.github/workflows/hugo.yaml) — read that
file for the versions actually in use; they change without this README
being updated.

## Links

- https://gohugo.io/host-and-deploy/host-on-github-pages/
- https://themes.gohugo.io/
- https://themes.gohugo.io/themes/hugo-book/
