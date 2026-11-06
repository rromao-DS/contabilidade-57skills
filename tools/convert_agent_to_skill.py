#!/usr/bin/env python3
"""Converte um subagente do Claude Code (.md com frontmatter name/description/tools/model)
em uma skill: skills/<name>/SKILL.md (frontmatter so com name + description) e
dist/<NN>-<name>.zip contendo <name>/SKILL.md.

Uso: convert_agent_to_skill.py <arquivo.md> <NN> [repo_root]
"""
import json, re, sys, zipfile
from pathlib import Path


def split_frontmatter(text):
    m = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n?(.*)\Z", text, re.S)
    if not m:
        raise SystemExit("ERRO: arquivo sem frontmatter YAML")
    return m.group(1), m.group(2)


def parse_fields(fm):
    """Parser simples chave: valor (aceita continuacao indentada)."""
    fields, key = {}, None
    for line in fm.splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s?(.*)$", line)
        if m and not line.startswith((" ", "\t")):
            key = m.group(1)
            fields[key] = m.group(2).strip()
        elif key and line.strip():
            fields[key] += " " + line.strip()
    for k, v in fields.items():
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            fields[k] = v[1:-1]
    return fields


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def main():
    src, num = Path(sys.argv[1]), sys.argv[2]
    root = Path(sys.argv[3]) if len(sys.argv) > 3 else Path("/home/user/contabilidade-57skills")
    fm, body = split_frontmatter(src.read_text(encoding="utf-8"))
    f = parse_fields(fm)
    if not f.get("name") or not f.get("description"):
        raise SystemExit(f"ERRO: {src} sem name/description")
    name = slugify(f["name"])
    desc = re.sub(r"\s+", " ", f["description"]).strip()
    # json.dumps gera string YAML valida (aspas duplas, escapes) -> evita quebra com ':' etc.
    skill_md = f"---\nname: {name}\ndescription: {json.dumps(desc, ensure_ascii=False)}\n---\n\n{body.lstrip()}"
    d = root / "skills" / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(skill_md, encoding="utf-8")
    dist = root / "dist"
    dist.mkdir(exist_ok=True)
    zp = dist / f"{num}-{name}.zip"
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(d / "SKILL.md", f"{name}/SKILL.md")
    print(f"OK {num} {name} -> {zp.name}")


if __name__ == "__main__":
    main()
