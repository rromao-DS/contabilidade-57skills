#!/usr/bin/env python3
"""Aplica descricoes <=1024 chars (short_descriptions.json) nas skills que excedem o limite.
O texto original completo e preservado no corpo do SKILL.md (secao 'Descricao completa')."""
import json, re, sys, zipfile
from pathlib import Path
import yaml
root = Path("/home/user/contabilidade-57skills")
short = json.loads((root / "tools/short_descriptions.json").read_text(encoding="utf-8"))
for name, new in short.items():
    p = root / "skills" / name / "SKILL.md"
    t = p.read_text(encoding="utf-8")
    m = re.match(r"\A---\n(.*?)\n---\n\n?(.*)\Z", t, re.S)
    old = yaml.safe_load(m.group(1))["description"]
    if len(old) <= 1024:
        continue
    assert len(new) <= 1024, (name, len(new))
    body = f"> **Descrição completa (original):** {old}\n\n{m.group(2)}"
    p.write_text(f"---\nname: {name}\ndescription: {json.dumps(new, ensure_ascii=False)}\n---\n\n{body}", encoding="utf-8")
    zp = next(q for q in (root / "dist").glob(f"*-{name}.zip") if q.name[3:] == f"{name}.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(p, f"{name}/SKILL.md")
    print("ok", name, len(old), "->", len(new))
