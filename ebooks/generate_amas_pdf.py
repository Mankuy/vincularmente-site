#!/usr/bin/env python3
"""Generate full PDF for 'Amás como amás' ebook from markdown source."""

from fpdf import FPDF
import re, os

FONT_REG = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
FONT_ITAL = '/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf'

MD_PATH = os.path.join(os.path.dirname(__file__), 'amas-como-amas.md')
OUT_PATH = os.path.join(os.path.dirname(__file__), 'amas-como-amas.pdf')

class EbookPDF(FPDF):
    ACCENT = (147, 51, 234)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font('Sans', '', 7)
        self.set_text_color(170, 170, 170)
        self.cell(0, 5, 'Amás como amás  ·  vincularmente', align='R')
        self.ln(3)
        self.set_draw_color(*self.ACCENT)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), self.w - 10, self.get_y())
        self.ln(5)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-15)
        self.set_font('Sans', 'I', 7)
        self.set_text_color(170, 170, 170)
        self.cell(0, 10, f'{self.page_no()}', align='C')

    def cover_page(self, title, subtitle):
        self.set_y(60)
        self.set_draw_color(*self.ACCENT)
        self.set_line_width(1.5)
        self.line(self.w/2 - 25, self.get_y(), self.w/2 + 25, self.get_y())
        self.ln(12)
        self.set_font('Sans', 'B', 32)
        self.set_text_color(*self.ACCENT)
        self.cell(0, 16, title, align='C')
        self.ln(20)
        self.set_font('Sans', '', 14)
        self.set_text_color(80, 80, 80)
        for line in subtitle.split('\n'):
            self.cell(0, 8, line, align='C')
            self.ln(8)
        self.ln(15)
        self.set_font('Sans', 'I', 12)
        self.set_text_color(130, 130, 130)
        self.cell(0, 8, 'vincularmente', align='C')
        self.ln(6)
        self.set_font('Sans', '', 9)
        self.set_text_color(170, 170, 170)
        self.cell(0, 6, 'Salud mental, vínculos y realidad.', align='C')
        self.add_page()

    def _page_break(self, needed=20):
        if self.get_y() > self.h - needed:
            self.add_page()

    def h1(self, text):
        self._page_break(30)
        self.set_font('Sans', 'B', 16)
        self.set_text_color(*self.ACCENT)
        self.ln(4)
        self.multi_cell(0, 10, text)
        self.ln(6)
        self.set_text_color(0, 0, 0)

    def h2(self, text):
        self._page_break(25)
        self.set_font('Sans', 'B', 13)
        self.set_text_color(*self.ACCENT)
        self.ln(3)
        self.multi_cell(0, 8, text)
        self.ln(5)
        self.set_text_color(0, 0, 0)

    def h3(self, text):
        self._page_break(20)
        self.set_font('Sans', 'B', 12)
        self.set_text_color(60, 60, 60)
        self.ln(2)
        self.multi_cell(0, 8, text)
        self.ln(4)
        self.set_text_color(0, 0, 0)

    def body(self, txt, size=10):
        self._page_break(15)
        self.set_font('Sans', '', size)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, txt)
        self.ln(3)

    def bold_body(self, txt, size=10):
        self._page_break(15)
        self.set_font('Sans', 'B', size)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, txt)
        self.ln(3)

    def bullet(self, txt):
        self._page_break(12)
        self.set_font('Sans', '', 10)
        self.set_text_color(40, 40, 40)
        x = self.get_x()
        self.cell(6, 5.5, chr(8226))
        self.multi_cell(self.w - self.l_margin - self.r_margin - 6, 5.5, txt)
        self.ln(1.5)

    def example(self, txt):
        self._page_break(25)
        self.set_font('Sans', 'I', 9.5)
        self.set_text_color(100, 100, 100)
        self.set_fill_color(248, 245, 255)
        self.set_x(self.l_margin + 5)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 10, 5.5, txt, fill=True)
        self.ln(4)
        self.set_text_color(0, 0, 0)

    def divider(self):
        self.ln(3)
        self.set_draw_color(200, 200, 200)
        self.set_line_width(0.2)
        self.line(self.w/2 - 15, self.get_y(), self.w/2 + 15, self.get_y())
        self.ln(6)

    def cta_box(self, txt):
        self._page_break(40)
        self.ln(4)
        self.set_draw_color(*self.ACCENT)
        self.set_line_width(0.5)
        y0 = self.get_y()
        self.set_x(self.l_margin + 10)
        self.set_font('Sans', 'B', 11)
        self.set_text_color(*self.ACCENT)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 20, 7, txt, align='C')
        y1 = self.get_y()
        self.rect(self.l_margin + 10, y0 - 2, self.w - self.l_margin - self.r_margin - 20, y1 - y0 + 4)
        self.ln(6)
        self.set_text_color(0, 0, 0)


def strip_inline_md(text):
    """Strip bold/italic markers, keep text."""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    return text


def parse_and_render(md_path, pdf):
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Skip front matter until first chapter
    i = 0
    # Find the table of contents and cover
    in_index = False
    toc_lines = []

    while i < len(lines):
        line = lines[i].rstrip('\n')
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            i += 1
            continue

        # Horizontal rule → divider
        if stripped == '---':
            pdf.divider()
            i += 1
            continue

        # Skip cover page lines (before first ## chapter)
        if stripped.startswith('## Índice'):
            in_index = True
            i += 1
            continue

        if in_index and re.match(r'^\d+\.', stripped):
            toc_lines.append(stripped)
            i += 1
            continue

        if in_index and stripped.startswith('## Capítulo'):
            in_index = False
            # Render TOC
            if toc_lines:
                pdf.set_font('Sans', 'B', 14)
                pdf.set_text_color(*pdf.ACCENT)
                pdf.cell(0, 10, 'Índice')
                pdf.ln(12)
                pdf.set_text_color(40, 40, 40)
                for t in toc_lines:
                    pdf.set_font('Sans', '', 10)
                    pdf.cell(0, 7, t)
                    pdf.ln(7)
                pdf.add_page()
                toc_lines = []

        # H2: ## Title
        m = re.match(r'^## (.+)$', stripped)
        if m:
            title = strip_inline_md(m.group(1))
            # Detect chapter vs section
            if title.startswith('Capítulo'):
                pdf.h1(title)
            elif title in ('Cerrando',):
                pdf.h1(title)
            elif title.startswith('¿Querés'):
                # Skip this section entirely
                while i < len(lines) and not lines[i].strip().startswith('---'):
                    i += 1
                continue
            else:
                pdf.h2(title)
            i += 1
            continue

        # H3: ### Title
        m = re.match(r'^### (.+)$', stripped)
        if m:
            pdf.h3(strip_inline_md(m.group(1)))
            i += 1
            continue

        # Bullets: - text
        if stripped.startswith('- '):
            pdf.bullet(strip_inline_md(stripped[2:]))
            i += 1
            continue

        # Regular body text
        text = strip_inline_md(stripped)
        # Detect bold-only lines
        if re.match(r'^".+"$', text) or stripped.startswith('**') and stripped.endswith('**'):
            pdf.bold_body(text.strip('"'))
        elif '→' in text:
            pdf.example(text)
        else:
            pdf.body(text)

        i += 1


# Build PDF
pdf = EbookPDF()
pdf.add_font('Sans', '', FONT_REG)
pdf.add_font('Sans', 'B', FONT_BOLD)
pdf.add_font('Sans', 'I', FONT_ITAL)
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()

# Cover
pdf.cover_page('Amás como amás', 'Estilos de apego y por qué elegís\nsiempre al mismo tipo de persona')

# Content
parse_and_render(MD_PATH, pdf)

# CTA after content
pdf.divider()
pdf.body('Este ebook es el primer paso. El siguiente es el acompañamiento.', size=10)
pdf.ln(2)
pdf.bold_body('¿Querés profundizar?', size=11)
pdf.body('"No estás Rot@" - Mi primer ebook sobre relaciones tóxicas')
pdf.body('go.hotmart.com/Q105244008P ($4.99)')
pdf.ln(2)
pdf.bold_body('¿Querés una sesión?', size=11)
pdf.body('Escribime. Trabajamos tu caso específico.')
pdf.body('WhatsApp: 598 991 48 716')
pdf.ln(2)
pdf.bold_body('Estoy acá.', size=11)

# Final branding
pdf.ln(10)
pdf.set_font('Sans', 'B', 14)
pdf.set_text_color(*pdf.ACCENT)
pdf.cell(0, 8, 'vincularmente', align='C')
pdf.ln(6)
pdf.set_font('Sans', '', 9)
pdf.set_text_color(130, 130, 130)
pdf.cell(0, 6, 'Salud mental, vínculos y realidad.', align='C')
pdf.ln(10)
pdf.set_font('Sans', '', 7)
pdf.set_text_color(170, 170, 170)
pdf.cell(0, 6, '© 2025 vincularmente. Todos los derechos reservados.', align='C')

pdf.output(OUT_PATH)
print(f'PDF generado: {OUT_PATH}')
print(f'Páginas: {pdf.pages_count}')
