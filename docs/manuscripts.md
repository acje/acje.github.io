# Manuscripts

The unpublished book *Unsafe at Any State* lives outside this repository:

```
~/Documents/manuscripts/acje.github.io/book/
```

It is deliberately not in git. These are unreviewed drafts, and keeping them
in `content/` made every local build publish `/book/` and `/uas/` pages that
CI never builds — so "it builds here" was not evidence of what deploys.

Backup (git is not a backup for this directory):

```
tar -czf ~/Documents/manuscripts/acje.github.io/book-backup-$(date +%F).tar.gz \
  -C ~/Documents/manuscripts/acje.github.io book
```

Preview the manuscript pages locally:

```
cp hugo.local.yaml.example hugo.local.yaml   # set the path once
hugo server --config hugo.yaml,hugo.local.yaml
```

`hugo.local.yaml` is gitignored, and the deploy build never loads it, so the
published site never contains these pages.
