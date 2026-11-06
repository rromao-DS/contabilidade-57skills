#!/usr/bin/env python3
"""Valida todas as skills: cada dist/*.zip precisa ter <name>/SKILL.md com frontmatter
YAML valido contendo name (== pasta, [a-z0-9-], <=64) e description (nao vazia, <=1024)."""
import re, sys, zipfile
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/home/user/contabilidade-57skills")
zips = sorted((root / "dist").glob("*.zip"))
bad, names = 0, {}
for zp in zips:
    errs = []
    try:
        with zipfile.ZipFile(zp) as z:
            if z.testzip():
                errs.append("zip corrompido")
            members = [n for n in z.namelist() if not n.endswith("/")]
            skills = [n for n in members if n.endswith("/SKILL.md") and n.count("/") == 1]
            if len(skills) != 1:
                errs.append(f"esperado 1 <pasta>/SKILL.md, achei {members}")
            else:
                folder = skills[0].split("/")[0]
                text = z.read(skills[0]).decode("utf-8")
                m = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
                if not m:
                    errs.append("sem frontmatter")
                else:
                    meta = yaml.safe_load(m.group(1)) if yaml else None
                    if meta is None:
                        errs.append("YAML invalido/vazio")
                    else:
                        extra = set(meta) - {"name", "description"}
                        if extra:
                            errs.append(f"campos extras: {sorted(extra)}")
                        n, d = meta.get("name"), meta.get("description")
                        if not isinstance(n, str) or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", n) or len(n) > 64:
                            errs.append(f"name invalido: {n!r}")
                        elif n != folder:
                            errs.append(f"name {n!r} != pasta {folder!r}")
                        if not isinstance(d, str) or not d.strip() or len(d) > 1024:
                            errs.append("description ausente/vazia/>1024")
                        names.setdefault(n, []).append(zp.name)
    except Exception as e:
        errs.append(f"erro: {e}")
    if errs:
        bad += 1
        print(f"FALHA {zp.name}: {'; '.join(errs)}")
dups = {k: v for k, v in names.items() if len(v) > 1}
if dups:
    bad += 1
    print("NAMES DUPLICADOS:", dups)
print(f"{len(zips)} zips, {len(zips) - bad if not dups else '?'} ok, {bad} com problema")
sys.exit(1 if bad else 0)
