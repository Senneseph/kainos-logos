Organize in this directory any custom, ad-hoc tools you create for interacting with this project.

## op-plan/repair-encoding.py

One-off repair for mojibake (double-encoded UTF-8) that the `project-management/op`
Perl CLI used to introduce: `JSON::PP::encode_json` treated raw UTF-8 bytes from
`@ARGV` as Latin-1 and re-encoded them, so `—` (E2 80 94) was stored as
`â\x80\x94` (C3 A2 C2 80 C2 94) in OpenProject. Manual edits then left orphan
control chars (`\x80\x93`, lone `\x93`, `-\x80\x94`, …).

```bash
python3 .scripts/op-plan/repair-encoding.py --dry-run   # preview
python3 .scripts/op-plan/repair-encoding.py --apply     # PATCH OpenProject
```

It reverses the double-encoding windowed (longest valid UTF-8 run first) and
then fixes the specific leftover patterns left by manual edits. It only touches
subjects/descriptions and leaves unrelated rich-text edits (HTML tables,
`&quot;` entities, emphasis markers) alone. Verified against the canonical
`.scripts/op-plan/*.full.md` / `tasks/*.md` seed sources — the 22 WPs that were
seeded verbatim match their files byte-for-byte after repair.

The root cause in `project-management/op` is fixed (decode `@ARGV` as UTF-8,
`use open ':std', ':encoding(UTF-8)'`), so new writes are clean — this script
should not need to run again unless data was written by an old copy of `op`.
