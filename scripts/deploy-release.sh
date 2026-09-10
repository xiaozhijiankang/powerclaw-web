#!/usr/bin/env bash
set -euo pipefail

release=${1:?Release ID required}
[[ "$release" =~ ^[0-9]+-[0-9]+$ ]] || exit 2
base=/srv/powerclaw
incoming="$HOME/incoming/$release"
target="$base/releases/$release"
test ! -e "$target"
cd "$incoming"
sha256sum -c site.tar.gz.sha256
python3 - "$target" <<'PY'
import pathlib, sys, tarfile
target = pathlib.Path(sys.argv[1])
with tarfile.open('site.tar.gz', 'r:gz') as archive:
    members = archive.getmembers()
    for item in members:
        path = pathlib.PurePosixPath(item.name)
        if not item.isfile() or path.is_absolute() or '..' in path.parts:
            raise SystemExit('Unsafe archive member')
        if not (item.name.endswith('/index.html') or item.name == 'index.html' or item.name.startswith('assets/')):
            raise SystemExit('Non-public archive member')
    target.mkdir(mode=0o755)
    for item in members:
        output = target / item.name
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(archive.extractfile(item).read())
        output.chmod(0o644)
PY
for path in index.html privacy/index.html terms/index.html support/index.html en/index.html en/privacy/index.html en/terms/index.html en/support/index.html; do
    test -s "$target/$path"
done
previous=$(readlink "$base/current")
ln -s "$target" "$base/current-$release"
mv -Tf "$base/current-$release" "$base/current"
rollback() {
    ln -s "$previous" "$base/rollback-$release"
    mv -Tf "$base/rollback-$release" "$base/current"
}
trap rollback ERR
for path in index.html privacy/index.html terms/index.html support/index.html en/index.html en/privacy/index.html en/terms/index.html en/support/index.html; do
    curl --fail --silent --show-error --max-time 15 "http://127.0.0.1:8080/$path" -o "$incoming/response.html"
    cmp "$target/$path" "$incoming/response.html"
done
trap - ERR
printf 'Release %s verified; previous release: %s\n' "$release" "$previous"
