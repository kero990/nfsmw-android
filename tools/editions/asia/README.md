# Asia (Chinese) edition

`default.xex` SHA-256 `0cd7b9fa3957de08...`. Created with
`tools/editions/crear_arbol.py cht tools/editions/asia/tabla.tsv <xex> --parejas
tools/editions/asia/parejas_corregidas.json`.

`parejas_corregidas.json` follows the other editions. `tabla.tsv` is committed here although
the other editions do not ship theirs: it is the address map that `emparejar.py` produces from
the reference and this edition's executables, and shipping it means a player needs only their own
disc, not a PAL Spanish one as well. It holds nothing but addresses, section names
(`.text`, `.rdata`, `.data`, `.embsec_`) and match verdicts -- no game content.

The XEX and every file derived from it stay out of the repository, as everywhere else:
`crear_arbol.py` regenerates `app_cht/` from `app/` plus these two files.
