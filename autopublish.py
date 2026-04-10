#!/usr/bin/env python3
"""
Vincularmente — Auto-publish pipeline
Detecta .md nuevos en seomachine/drafts/, convierte a HTML, publica en GitHub Pages.

Uso:
  python3 autopublish.py              # Procesar todos los .md nuevos
  python3 autopublish.py --dry-run    # Solo mostrar qué haría
  python3 autopublish.py --force      # Procesar todos (incluso ya publicados)
"""

import os
import sys
import re
import glob
import subprocess
import hashlib
from datetime import datetime
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════

SITE_DIR = Path("/home/facajgs/vincularmente-site")
DRAFTS_DIR = Path("/home/facajgs/seomachine/drafts")
POSTS_DIR = SITE_DIR / "posts"
STATE_FILE = SITE_DIR / ".published_state"
LOG_FILE = Path("/home/facajgs/logs/autopublish-maestro.log")

# ═══════════════════════════════════════════════════════════════
# FUNCIONES
# ═══════════════════════════════════════════════════════════════

def log(msg):
    """Escribe en log con timestamp."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(line + "\n")


def load_published_state():
    """Carga estado de archivos ya publicados."""
    if STATE_FILE.exists():
        return set(STATE_FILE.read_text().strip().split('\n'))
    return set()


def save_published_state(published):
    """Guarda estado de archivos publicados."""
    STATE_FILE.write_text('\n'.join(sorted(published)))


def file_hash(filepath):
    """Hash del contenido del archivo."""
    return hashlib.md5(Path(filepath).read_bytes()).hexdigest()


def slugify(text):
    """Convierte texto a slug URL-friendly."""
    text = text.lower().strip()
    text = re.sub(r'[áàä]', 'a', text)
    text = re.sub(r'[éèë]', 'e', text)
    text = re.sub(r'[íìï]', 'i', text)
    text = re.sub(r'[óòö]', 'o', text)
    text = re.sub(r'[úùü]', 'u', text)
    text = re.sub(r'ñ', 'n', text)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text


def md_to_html(md_text):
    """Convierte Markdown a HTML limpio."""
    lines = md_text.split('\n')
    html_lines = []

    for line in lines:
        stripped = line.strip()

        # Skip empty lines (we handle spacing in CSS)
        if not stripped:
            html_lines.append('')
            continue

        # H2
        if re.match(r'^## (.+)$', stripped):
            html_lines.append(f'<h2>{re.sub(r"^## ", "", stripped)}</h2>')
            continue

        # H3
        if re.match(r'^### (.+)$', stripped):
            html_lines.append(f'<h3>{re.sub(r"^### ", "", stripped)}</h3>')
            continue

        # Horizontal rule
        if stripped == '---':
            html_lines.append('<hr>')
            continue

        # Bullet list items
        if re.match(r'^[-*] ', stripped):
            content = re.sub(r'^[-*] ', '', stripped)
            content = format_inline(content)
            html_lines.append(f'<li>{content}</li>')
            continue

        # Numbered list items
        if re.match(r'^\d+\. ', stripped):
            content = re.sub(r'^\d+\. ', '', stripped)
            content = format_inline(content)
            html_lines.append(f'<li>{content}</li>')
            continue

        # Regular paragraph
        formatted = format_inline(stripped)
        html_lines.append(f'<p>{formatted}</p>')

    # Wrap consecutive <li> in <ul>
    result = '\n'.join(html_lines)
    result = re.sub(r'((?:<li>.*?</li>\n?)+)', r'<ul>\1</ul>', result)

    return result


def format_inline(text):
    """Aplica formato inline: bold, italic, links."""
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Links
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" target="_blank">\1</a>', text)
    return text


def extract_title(md_text):
    """Extrae el título H1 del markdown."""
    m = re.search(r'^# (.+)$', md_text, re.MULTILINE)
    return m.group(1) if m else "Sin título"


def extract_description(md_text):
    """Extrae una descripción del primer párrafo."""
    lines = md_text.split('\n')
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('#') and not stripped.startswith('---') and len(stripped) > 50:
            # Clean up markdown formatting
            stripped = re.sub(r'\*\*(.+?)\*\*', r'\1', stripped)
            stripped = re.sub(r'\*(.+?)\*', r'\1', stripped)
            if len(stripped) > 150:
                stripped = stripped[:147] + "..."
            return stripped
    return ""


def generate_article_html(title, html_content, description, slug, date=None):
    """Genera la página HTML completa del artículo (nuevo diseño editorial)."""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    canonical_url = f"https://mankuy.github.io/vincularmente-site/posts/{slug}.html"
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Vincularmente</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{canonical_url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:image" content="https://mankuy.github.io/vincularmente-site/assets/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@vincularmente">
  <meta name="twitter:image" content="https://mankuy.github.io/vincularmente-site/assets/og-image.png">
  <link rel="stylesheet" href="../assets/css/style.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{title}",
    "author": {{"@type": "Person", "name": "vincularmente"}},
    "publisher": {{"@type": "Organization", "name": "vincularmente"}},
    "datePublished": "{date}",
    "url": "{canonical_url}"
  }}
  </script>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🧠</text></svg>">
</head>
<body>

<button class="theme-toggle" onclick="toggleTheme()" title="Cambiar tema">☀</button>

<header>
  <a href="../index.html" class="logo">vincular<span>mente</span></a>
  <nav>
    <a href="../index.html">Artículos</a>
    <a href="../index.html#ebooks">Ebooks</a>
    <a href="../contacto.html">Sesiones</a>
  </nav>
</header>

<article>

<h1>{title}</h1>
<p class="meta">vincularmente · <a href="https://x.com/vincularmente" target="_blank">@vincularmente</a></p>

{html_content}

<div class="cta-box">
  <h3>¿Te resonó algo de esto?</h3>
  <p>Escribí dos ebooks para la gente que siente que algo está mal pero no sabe nombrarlo. Psicología de a pie. Sin jerga, sin vueltas, las cosas como son.</p>
  <a href="https://go.hotmart.com/Q105244008P" class="btn btn-primary" target="_blank">"No estás Rot@" — $4.99</a>
  <a href="https://go.hotmart.com/I105316653N?dp=1" class="btn btn-primary" target="_blank">"Amás como amás" — $4.99</a>
  <a href="../contacto.html" class="btn btn-secondary">Pedí tu sesión</a>
</div>

</article>

<footer>
  <span>vincularmente · <a href="https://x.com/vincularmente" target="_blank">@vincularmente</a></span>
  <span><a href="../contacto.html">Contacto</a></span>
</footer>

<script>
function toggleTheme() {{
  const body = document.body;
  const btn = document.querySelector('.theme-toggle');
  if (body.getAttribute('data-theme') === 'light') {{
    body.removeAttribute('data-theme');
    btn.textContent = '☀';
    localStorage.setItem('theme', 'dark');
  }} else {{
    body.setAttribute('data-theme', 'light');
    btn.textContent = '☾';
    localStorage.setItem('theme', 'light');
  }}
}}
(function() {{
  const saved = localStorage.getItem('theme');
  if (saved === 'light') {{
    document.body.setAttribute('data-theme', 'light');
    document.querySelector('.theme-toggle').textContent = '☾';
  }}
}})();
</script>

</body>
</html>'''


def update_sitemap(slug):
    """Agrega la URL del artículo al sitemap.xml."""
    sitemap_path = SITE_DIR / "sitemap.xml"
    if not sitemap_path.exists():
        log(f"  ⚠️ sitemap.xml no encontrado, creando uno nuevo")
        sitemap_path.write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n</urlset>\n')

    sitemap = sitemap_path.read_text()
    url = f"https://mankuy.github.io/vincularmente-site/posts/{slug}.html"

    if url in sitemap:
        log(f"  ⏭️ Ya existe en sitemap.xml")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    entry = f'''  <url>
    <loc>{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
'''

    # Insert before closing </urlset> tag
    if '</urlset>' in sitemap:
        sitemap = sitemap.replace('</urlset>', entry + '</urlset>')
        sitemap_path.write_text(sitemap)
        log(f"  ✅ URL agregada al sitemap.xml")
    else:
        log(f"  ⚠️ Tag </urlset> no encontrado en sitemap.xml")


def update_index(title, slug, description, category="relaciones"):
    """Agrega el artículo al index.html con categoría."""
    index_path = SITE_DIR / "index.html"
    index = index_path.read_text()

    # Check for duplicate slug
    if f"/posts/{slug}.html" in index:
        log(f"  ⏭️ Ya existe en index.html, no se duplica")
        return

    category_labels = {
        "relaciones": "Relaciones",
        "autoconocimiento": "Autoconocimiento",
        "salud-mental": "Salud mental",
    }
    tag_label = category_labels.get(category, "Relaciones")

    card_html = f'''
    <div class="post-card" data-category="{category}">
      <span class="post-tag">{tag_label}</span>
      <h3><a href="posts/{slug}.html">{title}</a></h3>
      <p>{description}</p>
    </div>'''

    # Insert before the comment marker
    marker = '<!-- Nuevos artículos se agregan arriba de esta línea -->'
    if marker in index:
        index = index.replace(marker, card_html + '\n\n    ' + marker)
        index_path.write_text(index)
        log(f"  ✅ Artículo agregado al index.html (categoría: {tag_label})")
    else:
        log(f"  ⚠️ Marker no encontrado en index.html, no se actualizó")


def git_push():
    """Hace git add, commit y push."""
    try:
        subprocess.run(['git', 'add', '-A'], cwd=str(SITE_DIR), capture_output=True, check=True)

        # Check if there are changes
        result = subprocess.run(['git', 'status', '--porcelain'], cwd=str(SITE_DIR), capture_output=True, text=True)
        if not result.stdout.strip():
            log("  ℹ️ No hay cambios para commitear")
            return True

        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        commit_msg = f"Auto-publish: artículo nuevo ({ts})"
        subprocess.run(['git', 'commit', '-m', commit_msg], cwd=str(SITE_DIR), capture_output=True, check=True)

        result = subprocess.run(['git', 'push'], cwd=str(SITE_DIR), capture_output=True, text=True)
        if result.returncode == 0:
            log("  ✅ Push exitoso a GitHub")
            return True
        else:
            log(f"  ❌ Error en git push: {result.stderr}")
            return False

    except subprocess.CalledProcessError as e:
        log(f"  ❌ Error git: {e.stderr if hasattr(e, 'stderr') else str(e)}")
        return False


def process_article(md_path, dry_run=False):
    """Procesa un artículo .md y lo publica."""
    md_path = Path(md_path)
    log(f"\n📄 Procesando: {md_path.name}")

    # Read markdown
    md_text = md_path.read_text(encoding='utf-8')

    # Extract info
    title = extract_title(md_text)
    description = extract_description(md_text)
    slug = slugify(md_path.stem)

    log(f"  Título: {title}")
    log(f"  Slug: {slug}")
    log(f"  Palabras: {len(md_text.split())}")

    if dry_run:
        log(f"  [DRY RUN] No se publicaría: /posts/{slug}.html")
        return True

    # Remove H1 from content (template already renders it)
    md_text = re.sub(r'^# .+\n+', '', md_text, count=1, flags=re.MULTILINE)

    # Convert to HTML
    html_content = md_to_html(md_text)

    # Remove CTA markdown lines (they're replaced by the template)
    html_content = html_content.replace(
        '<p>*Si algo de esto te resonó, escribí un ebook sobre esto. Se llama "No estás Rot@" y está en Hotmart por $4.99. No es autoayuda. Es psicología de a pie. Sin jerga, sin vueltas, las cosas como son.*</p>', ''
    )
    html_content = html_content.replace(
        '<p>*¿Querés charlar sobre esto? Escribime por WhatsApp: 59899148716*</p>', ''
    )
    html_content = html_content.replace(
        '<p>*Seguime en @vincularmente para más contenido así.*</p>', ''
    )

    # Generate full HTML page
    full_html = generate_article_html(title, html_content, description, slug)

    # Write to posts/
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = POSTS_DIR / f"{slug}.html"
    output_path.write_text(full_html, encoding='utf-8')
    log(f"  ✅ HTML generado: {output_path}")

    # Update index
    update_index(title, slug, description)

    # Update sitemap
    update_sitemap(slug)

    return True


def main():
    log("=" * 60)
    log("🚀 AUTOPUBLISH — Iniciando")
    log("=" * 60)

    dry_run = '--dry-run' in sys.argv
    force = '--force' in sys.argv

    if dry_run:
        log("⚠️ MODO DRY RUN — No se publicará nada")

    # Find .md files
    md_files = sorted(glob.glob(str(DRAFTS_DIR / "*.md")))

    if not md_files:
        log("ℹ️ No se encontraron archivos .md en drafts/")
        return

    log(f"📂 Encontrados {len(md_files)} archivos .md")

    # Load published state
    published = load_published_state()

    processed = 0
    for md_file in md_files:
        file_id = f"{md_file}:{file_hash(md_file)}"

        if not force and file_id in published:
            log(f"⏭️ Saltando (ya publicado): {Path(md_file).name}")
            continue

        if process_article(md_file, dry_run=dry_run):
            published.add(file_id)
            processed += 1

    # Save state
    if not dry_run:
        save_published_state(published)

    # Git push if anything was processed
    if processed > 0 and not dry_run:
        log(f"\n📤 Publicando {processed} artículo(s)...")
        git_push()
    elif processed == 0:
        log("ℹ️ No hay artículos nuevos para publicar")

    log(f"\n✅ DONE — {processed} artículo(s) procesado(s)")


if __name__ == "__main__":
    main()
