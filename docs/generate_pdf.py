"""
Business Signal — Professional Documentation PDF Generator
Author: Ranjith S | AI Engineering Project
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, ListFlowable, ListItem
)
from reportlab.platypus.flowables import Flowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import datetime

# ── Colour palette ─────────────────────────────────────────────────────────────
NAVY       = HexColor("#0A0F1E")
ELECTRIC   = HexColor("#00D4FF")
PURPLE     = HexColor("#7B2FBE")
SLATE      = HexColor("#1E2A3A")
MUTED      = HexColor("#8A9BAE")
WHITE      = HexColor("#FFFFFF")
LIGHT_BG   = HexColor("#F4F7FB")
ACCENT     = HexColor("#00B4D8")
DARK_TEXT  = HexColor("#0D1117")
BODY_TEXT  = HexColor("#1C2B3A")
GRID_LINE  = HexColor("#D0DCE8")
SUCCESS    = HexColor("#00C896")
WARN       = HexColor("#FF8C00")
CODE_BG    = HexColor("#1A2332")
CODE_TEXT  = HexColor("#E2F0FF")

W, H = A4  # 595.27 × 841.89 pt

# ── Page template with header/footer ──────────────────────────────────────────
class PageCanvas:
    def __init__(self, title):
        self.title = title

    def __call__(self, cnv, doc):
        cnv.saveState()
        page = doc.page

        # ── Top accent bar ──
        cnv.setFillColor(ELECTRIC)
        cnv.rect(0, H - 6, W, 6, fill=1, stroke=0)

        if page > 1:
            # Header
            cnv.setFillColor(NAVY)
            cnv.rect(0, H - 36, W, 30, fill=1, stroke=0)
            cnv.setFont("Helvetica-Bold", 7)
            cnv.setFillColor(ELECTRIC)
            cnv.drawString(20, H - 24, "BUSINESS SIGNAL")
            cnv.setFont("Helvetica", 7)
            cnv.setFillColor(MUTED)
            cnv.drawRightString(W - 20, H - 24, self.title)

            # Footer
            cnv.setFillColor(LIGHT_BG)
            cnv.rect(0, 0, W, 28, fill=1, stroke=0)
            cnv.setFillColor(GRID_LINE)
            cnv.setLineWidth(0.5)
            cnv.line(20, 28, W - 20, 28)
            cnv.setFont("Helvetica", 7)
            cnv.setFillColor(MUTED)
            cnv.drawString(20, 10, "Business Signal · AI Engineering Project · Ranjith S · 2026")
            cnv.drawRightString(W - 20, 10, f"Page {page}")

        cnv.restoreState()


# ── Style helpers ──────────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()

    def S(name, **kw):
        return ParagraphStyle(name, **kw)

    return {
        "cover_name":    S("cn",  fontName="Helvetica-Bold",  fontSize=36, leading=44, textColor=WHITE,     spaceAfter=6),
        "cover_sub":     S("cs",  fontName="Helvetica-Bold",  fontSize=16, leading=22, textColor=ELECTRIC,  spaceAfter=4),
        "cover_desc":    S("cd",  fontName="Helvetica",       fontSize=10, leading=16, textColor=MUTED,     spaceAfter=2),
        "cover_tag":     S("ct",  fontName="Helvetica-Bold",  fontSize=7,  leading=10, textColor=ELECTRIC),

        "chapter":       S("ch",  fontName="Helvetica-Bold",  fontSize=18, leading=24, textColor=NAVY,      spaceBefore=10, spaceAfter=6),
        "section":       S("sec", fontName="Helvetica-Bold",  fontSize=13, leading=18, textColor=SLATE,     spaceBefore=10, spaceAfter=4),
        "subsection":    S("sub", fontName="Helvetica-Bold",  fontSize=10, leading=14, textColor=PURPLE,    spaceBefore=6,  spaceAfter=3),
        "body":          S("b",   fontName="Helvetica",       fontSize=9.5,leading=15, textColor=BODY_TEXT, spaceAfter=5,   alignment=TA_JUSTIFY),
        "body_center":   S("bc",  fontName="Helvetica",       fontSize=9,  leading=14, textColor=BODY_TEXT, spaceAfter=4,   alignment=TA_CENTER),
        "bullet":        S("bl",  fontName="Helvetica",       fontSize=9.5,leading=14, textColor=BODY_TEXT, leftIndent=14,  spaceAfter=3),
        "code":          S("co",  fontName="Courier",         fontSize=8,  leading=12, textColor=CODE_TEXT, backColor=CODE_BG, leftIndent=8, rightIndent=8, spaceBefore=3, spaceAfter=3),
        "caption":       S("cap", fontName="Helvetica-Oblique",fontSize=8, leading=11, textColor=MUTED,     alignment=TA_CENTER, spaceAfter=4),
        "label":         S("lb",  fontName="Helvetica-Bold",  fontSize=7.5,leading=10, textColor=ELECTRIC),
        "toc_chapter":   S("tc",  fontName="Helvetica-Bold",  fontSize=10, leading=16, textColor=NAVY),
        "toc_section":   S("ts",  fontName="Helvetica",       fontSize=9,  leading=14, textColor=BODY_TEXT, leftIndent=14),
        "note":          S("nt",  fontName="Helvetica-Oblique",fontSize=8.5,leading=13,textColor=HexColor("#4A5568"), leftIndent=10),
    }

ST = make_styles()

def P(text, style="body"):
    return Paragraph(text, ST[style])

def SP(h=4):
    return Spacer(1, h * mm)

def HR(color=GRID_LINE, thickness=0.5):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=4, spaceBefore=4)

def section_label(text):
    return P(text, "label")

def bullet_list(items, style="bullet"):
    return [P(f"<b>•</b>  {item}", style) for item in items]


# ── Cover page ─────────────────────────────────────────────────────────────────
class CoverPage(Flowable):
    def wrap(self, w, h):
        return w, h

    def draw(self):
        c = self.canv
        # Background gradient simulation
        c.setFillColor(NAVY)
        c.rect(0, 0, W, H, fill=1, stroke=0)

        # Decorative arc top-right
        c.setFillColor(HexColor("#0D1A2E"))
        c.circle(W + 20, H + 20, 260, fill=1, stroke=0)
        c.setFillColor(HexColor("#091527"))
        c.circle(W + 20, H + 20, 180, fill=1, stroke=0)

        # Electric top bar
        c.setFillColor(ELECTRIC)
        c.rect(0, H - 5, W, 5, fill=1, stroke=0)

        # Left neon accent stripe
        c.setFillColor(PURPLE)
        c.rect(0, 0, 4, H, fill=1, stroke=0)
        c.setFillColor(ELECTRIC)
        c.rect(4, 0, 2, H, fill=1, stroke=0)

        # Grid dots  
        c.setFillColor(HexColor("#0F1E35"))
        for x in range(60, int(W), 28):
            for y in range(40, int(H) - 40, 28):
                c.circle(x, y, 1, fill=1, stroke=0)

        # Project label
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(ELECTRIC)
        c.drawString(28, H - 32, "AI  ENGINEERING  PROJECT  SHOWCASE  ·  2026")

        # Title
        c.setFont("Helvetica-Bold", 46)
        c.setFillColor(WHITE)
        c.drawString(28, H - 100, "Business")
        c.setFillColor(ELECTRIC)
        c.drawString(28, H - 150, "Signal")

        # Underline
        c.setFillColor(PURPLE)
        c.rect(28, H - 162, 200, 3, fill=1, stroke=0)

        # Tagline
        c.setFont("Helvetica", 12)
        c.setFillColor(MUTED)
        c.drawString(28, H - 185, "Ask a business question. Find the signal.")

        # Description block
        desc_lines = [
            "An end-to-end AI engineering project that answers natural-language",
            "business questions with structured evidence, SQL intelligence,",
            "retrieval-augmented generation and deterministic risk analysis.",
        ]
        c.setFont("Helvetica", 9)
        c.setFillColor(HexColor("#6A8098"))
        for i, line in enumerate(desc_lines):
            c.drawString(28, H - 210 - i * 14, line)

        # Tech pills
        pills = ["FastAPI", "PostgreSQL", "pgvector", "Next.js", "Docker", "Gemini AI", "RAG", "Sentence-Transformers"]
        px, py = 28, H - 270
        c.setFont("Helvetica-Bold", 7.5)
        for pill in pills:
            tw = c.stringWidth(pill, "Helvetica-Bold", 7.5) + 16
            c.setFillColor(HexColor("#0F2A40"))
            c.roundRect(px, py, tw, 18, 4, fill=1, stroke=0)
            c.setStrokeColor(HexColor("#1A3A50"))
            c.setLineWidth(0.5)
            c.roundRect(px, py, tw, 18, 4, fill=0, stroke=1)
            c.setFillColor(ELECTRIC)
            c.drawString(px + 8, py + 6, pill)
            px += tw + 8
            if px > W - 80:
                px = 28
                py -= 26

        # Divider
        c.setStrokeColor(HexColor("#1A3A50"))
        c.setLineWidth(0.5)
        c.line(28, H - 340, W - 28, H - 340)

        # Stats row
        stats = [
            ("20 + Pages", "Documentation"),
            ("8 + Modules", "Backend"),
            ("21 / 21", "Tests Passing"),
            ("4 / 4", "Evaluations"),
        ]
        sx = 28
        sy = H - 390
        c.setFont("Helvetica-Bold", 18)
        for val, lbl in stats:
            c.setFillColor(ELECTRIC)
            c.drawString(sx, sy + 20, val)
            c.setFont("Helvetica", 8)
            c.setFillColor(MUTED)
            c.drawString(sx, sy + 6, lbl)
            c.setFont("Helvetica-Bold", 18)
            sx += (W - 56) / len(stats)

        # Author block
        c.setFillColor(HexColor("#0D1E30"))
        c.roundRect(28, 70, W - 56, 64, 6, fill=1, stroke=0)
        c.setStrokeColor(ELECTRIC)
        c.setLineWidth(0.5)
        c.roundRect(28, 70, W - 56, 64, 6, fill=0, stroke=1)
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(WHITE)
        c.drawString(44, 114, "Ranjith S")
        c.setFont("Helvetica", 8)
        c.setFillColor(MUTED)
        c.drawString(44, 100, "AI Engineering  ·  Full-Stack Development  ·  GenAI Applications")
        c.drawString(44, 86, "github.com/ranjiths112007/Business-Signal-enterprise-ai")
        c.setFont("Helvetica", 8)
        c.setFillColor(MUTED)
        c.drawRightString(W - 44, 86, f"September 2026")


# ── Metric card flowable ───────────────────────────────────────────────────────
def metric_row(metrics):
    """metrics: list of (value, label, color)"""
    cols = len(metrics)
    cell_w = (W - 56 - (cols - 1) * 6) / cols
    data = [[
        Paragraph(f"<font color='#{c[1:]}' size='18'><b>{v}</b></font><br/>"
                  f"<font color='#8A9BAE' size='7'>{l}</font>", ST["body_center"])
        for v, l, c in metrics
    ]]
    style = TableStyle([
        ("BACKGROUND",  (0, 0), (-1, -1), LIGHT_BG),
        ("TOPPADDING",  (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING",(0,0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",(0, 0), (-1, -1), 8),
        ("ALIGN",       (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("GRID",        (0, 0), (-1, -1), 0.5, GRID_LINE),
        ("ROUNDEDCORNERS", [4]),
    ])
    return Table(data, colWidths=[cell_w] * cols, style=style)


def code_block(lines):
    text = "<br/>".join(
        f'<font color="#E2F0FF">{l}</font>' if not l.startswith("#")
        else f'<font color="#6A9FDA">{l}</font>'
        for l in lines
    )
    return Paragraph(text, ST["code"])


def info_table(headers, rows, col_widths=None):
    data = [headers] + rows
    n_cols = len(headers)
    if not col_widths:
        col_widths = [(W - 56) / n_cols] * n_cols
    style = TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  NAVY),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  ELECTRIC),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, 0),  8),
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",      (0, 1), (-1, -1), 8.5),
        ("TEXTCOLOR",     (0, 1), (-1, -1), BODY_TEXT),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ("GRID",          (0, 0), (-1, -1), 0.4, GRID_LINE),
        ("ALIGN",         (0, 0), (-1, 0),  "CENTER"),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ])
    table_data = []
    for r_idx, row in enumerate(data):
        row_cells = []
        for c_idx, c in enumerate(row):
            if isinstance(c, (Paragraph, Flowable)):
                row_cells.append(c)
            elif r_idx == 0:
                row_cells.append(Paragraph(str(c), ST["label"]))
            else:
                row_cells.append(Paragraph(str(c), ST["body"]))
        table_data.append(row_cells)
    return Table(table_data, colWidths=col_widths, style=style)


def highlight_box(text, color=ELECTRIC, bg=None):
    bg = bg or HexColor("#E8F8FF")
    data = [[Paragraph(text, ST["body"])]]
    style = TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), bg),
        ("LEFTPADDING",  (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING",   (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 10),
        ("LINEAFTER",    (0, 0), (0, -1),  0, bg),
        ("LINEBEFORE",   (0, 0), (0, -1),  4, color),
    ])
    return Table(data, colWidths=[W - 56], style=style)


# ── Build document ─────────────────────────────────────────────────────────────
def build_pdf(output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=28,
        rightMargin=28,
        topMargin=42,
        bottomMargin=36,
        title="Business Signal — AI Engineering Project Documentation",
        author="Ranjith S",
        subject="AI Engineering, RAG, FastAPI, Next.js, PostgreSQL",
        creator="Business Signal PDF Generator",
    )

    story = []
    on_page = PageCanvas("Business Signal · Technical Documentation")

    # ══════════════════════════════════════════════════════════
    # COVER PAGE
    # ══════════════════════════════════════════════════════════
    story.append(CoverPage())
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # TABLE OF CONTENTS
    # ══════════════════════════════════════════════════════════
    story.append(section_label("CONTENTS"))
    story.append(SP(2))
    story.append(P("Table of Contents", "chapter"))
    story.append(HR(ELECTRIC, 1.5))
    story.append(SP(4))

    toc = [
        ("01", "Executive Summary", "3"),
        ("02", "Project Overview", "4"),
        ("03", "Architecture Deep Dive", "5"),
        ("04", "Technology Stack", "7"),
        ("05", "Backend Engineering", "9"),
        ("06", "AI & Intelligence Layer", "12"),
        ("07", "Frontend Application", "15"),
        ("08", "Database Design", "16"),
        ("09", "API Reference", "17"),
        ("10", "Security Engineering", "18"),
        ("11", "Testing & Evaluation", "19"),
        ("12", "Data Ingestion Pipeline", "20"),
        ("13", "Deployment Architecture", "21"),
        ("14", "Performance & Scalability", "22"),
        ("15", "Future Roadmap", "23"),
        ("16", "Conclusion", "24"),
    ]

    for num, chapter, page in toc:
        row_data = [[
            Paragraph(f"<font color='#00D4FF'><b>{num}</b></font>", ST["toc_chapter"]),
            Paragraph(chapter, ST["toc_chapter"]),
            Paragraph(f"<font color='#8A9BAE'>{page}</font>", ST["toc_chapter"]),
        ]]
        t = Table(row_data, colWidths=[25, W - 56 - 25 - 30, 30],
                  style=TableStyle([
                      ("TOPPADDING",    (0, 0), (-1, -1), 5),
                      ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                      ("LEFTPADDING",   (0, 0), (-1, -1), 0),
                      ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
                      ("LINEBELOW",     (0, 0), (-1, -1), 0.3, GRID_LINE),
                      ("ALIGN",         (2, 0), (2, 0), "RIGHT"),
                  ]))
        story.append(t)

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 01 EXECUTIVE SUMMARY
    # ══════════════════════════════════════════════════════════
    story.append(section_label("01  ·  EXECUTIVE SUMMARY"))
    story.append(P("Executive Summary", "chapter"))
    story.append(HR(ELECTRIC, 1.5))
    story.append(SP(3))

    story.append(highlight_box(
        "<b>Business Signal</b> is an end-to-end AI engineering project I built to demonstrate how structured "
        "business data, a natural-language SQL agent, retrieval-augmented generation (RAG), and "
        "deterministic risk analysis can be combined into a single coherent intelligence pipeline — "
        "one that always shows its working and never makes up facts.",
        ELECTRIC, HexColor("#EEF9FF")
    ))
    story.append(SP(5))

    story.append(P(
        "The project answers real business questions — <i>Which customers are at risk? What is our "
        "total revenue? Which industry drives the most growth?</i> — by routing each question to the "
        "right source: a SQL query, a vector similarity search, or a deterministic rule engine. "
        "Every answer is returned alongside the exact evidence that produced it.", "body"
    ))
    story.append(SP(3))
    story.append(P(
        "This document covers the full technical design, every module, the AI engineering decisions, "
        "test coverage, security model, and deployment approach. It is written as a technical showcase "
        "of what I built, how I built it, and why each decision was made.", "body"
    ))
    story.append(SP(5))

    story.append(metric_row([
        ("1,310", "Customers in demo DB", "#00D4FF"),
        ("₹1.6M+", "Demo revenue tracked", "#7B2FBE"),
        ("21 / 21", "Unit tests passing", "#00C896"),
        ("4 / 4",  "Eval tests passing",  "#FF8C00"),
    ]))
    story.append(SP(5))

    story.append(P("What makes this an AI Engineering project — not just a CRUD app:", "section"))
    story.append(SP(2))
    items = [
        "<b>Grounded answers:</b> every response cites structured evidence — no hallucinations, no invented numbers.",
        "<b>Multi-source routing:</b> questions are classified then sent to SQL, retrieval, or rules based on intent.",
        "<b>No-LLM fallback:</b> the system answers 16+ question categories deterministically without any API key.",
        "<b>RAG pipeline:</b> PDF documents are chunked, embedded with Sentence-Transformers, and stored in pgvector.",
        "<b>SQL agent:</b> natural-language questions are converted to safe, read-only PostgreSQL SELECT queries.",
        "<b>Prompt-injection guard:</b> every user question is sanitized before reaching the LLM.",
        "<b>Risk analysis engine:</b> each customer gets a scored risk level driven by revenue trend and ticket data.",
        "<b>Smart CSV mapper:</b> uploads fuzzy-match 40+ common column name variants — no manual mapping required.",
    ]
    for item in bullet_list(items):
        story.append(item)

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 02 PROJECT OVERVIEW
    # ══════════════════════════════════════════════════════════
    story.append(section_label("02  ·  PROJECT OVERVIEW"))
    story.append(P("Project Overview", "chapter"))
    story.append(HR(ELECTRIC, 1.5))
    story.append(SP(3))

    story.append(P("Background & Motivation", "section"))
    story.append(P(
        "I built Business Signal to answer a practical question: <i>what does a well-engineered AI system "
        "that answers structured business questions actually look like under the hood?</i> Not a chatbot "
        "that confidently makes things up, but a system with a deliberate pipeline — classify, retrieve, "
        "reason, cite. The goal was to build something small enough to fully understand end-to-end "
        "while demonstrating real AI engineering depth.", "body"
    ))
    story.append(SP(3))

    story.append(P("Core Problem Statement", "section"))
    story.append(highlight_box(
        "Business analysts spend hours manually querying databases and spreadsheets. "
        "Generic chatbots hallucinate numbers. Business Signal asks: can we build a system that "
        "<b>answers naturally, reasons correctly, and always shows its evidence</b>?",
        PURPLE, HexColor("#F5EEF8")
    ))
    story.append(SP(5))

    story.append(P("The Answer Pipeline", "section"))
    story.append(SP(2))
    pipeline_steps = [
        ("Question In",      "User asks in plain English through the web UI"),
        ("Intent Classify",  "System determines: business data, document, or general query"),
        ("Source Selection", "Routes to SQL agent, vector search, or rule engine"),
        ("Evidence Build",   "Gathers structured facts: revenue, risk scores, ticket counts"),
        ("LLM Synthesis",    "Gemini drafts a grounded answer from the evidence context"),
        ("Fallback Mode",    "Without an API key: deterministic rules answer 16+ categories"),
        ("Answer + Trace",   "Response returned with full evidence trace attached"),
    ]
    for i, (step, desc) in enumerate(pipeline_steps):
        row = [[
            Paragraph(f"<font color='#00D4FF'><b>{i+1:02d}</b></font>", ST["body_center"]),
            Paragraph(f"<b>{step}</b>", ST["body"]),
            Paragraph(desc, ST["body"]),
        ]]
        t = Table(row, colWidths=[22, 110, W - 56 - 22 - 110],
                  style=TableStyle([
                      ("BACKGROUND",    (0, 0), (-1, -1), LIGHT_BG if i % 2 == 0 else WHITE),
                      ("TOPPADDING",    (0, 0), (-1, -1), 7),
                      ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                      ("LEFTPADDING",   (0, 0), (-1, -1), 8),
                      ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
                      ("GRID",          (0, 0), (-1, -1), 0.3, GRID_LINE),
                      ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
                  ]))
        story.append(t)

    story.append(SP(5))
    story.append(P("Demo Dataset", "section"))
    story.append(P(
        "The project ships with a deterministic seeded dataset designed to produce "
        "interesting and realistic signal from the analysis pipeline:", "body"
    ))
    story.append(SP(2))

    demo_data = [
        ["Entity", "Count", "Key Detail"],
        ["Customers", "1,310", "Across 14 industries including SaaS, Fintech, Healthcare, Energy"],
        ["Sales records", "10,000+", "Jan–Aug 2026, realistic seasonal patterns"],
        ["Support tickets", "14 open", "2 high-priority, 12 medium — deliberately skewed for demo"],
        ["At-risk accounts", "2 HIGH", "Apex Logistics (−48.6% revenue), Pulse Media (−34.1%)"],
        ["Industries", "14", "Fintech, Energy, Logistics, Manufacturing, Retail, SaaS and more"],
    ]
    story.append(info_table(
        demo_data[0],
        [[Paragraph(c, ST["body"]) for c in row] for row in demo_data[1:]],
        col_widths=[100, 80, W - 56 - 180]
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 03 ARCHITECTURE
    # ══════════════════════════════════════════════════════════
    story.append(section_label("03  ·  ARCHITECTURE DEEP DIVE"))
    story.append(P("Architecture Deep Dive", "chapter"))
    story.append(HR(ELECTRIC, 1.5))
    story.append(SP(3))

    story.append(P(
        "Business Signal follows a layered architecture where each layer has a single, "
        "well-defined responsibility. The design is intentionally simple — no microservices, "
        "no message queues — because the goal is clarity and demonstrability, not scale.", "body"
    ))
    story.append(SP(4))

    story.append(P("System Layers", "section"))
    layers = [
        ("Presentation Layer",     "Next.js 14",            "React server/client components, CSS variables, real-time fetch"),
        ("API Gateway Layer",      "FastAPI (Python 3.11)",  "Auto-documented REST API, Pydantic validation, CORS middleware"),
        ("Intelligence Layer",     "Decision + SQL + RAG",  "Intent classification, SQL agent, vector retrieval, risk engine"),
        ("Persistence Layer",      "PostgreSQL 17 + pgvector","Relational schema + vector index for document embeddings"),
        ("Embedding Layer",        "Sentence-Transformers", "all-MiniLM-L6-v2 model (384-dim) for semantic document search"),
        ("LLM Layer (optional)",   "Google Gemini",         "Gemini-3.6-flash for natural language synthesis from evidence"),
        ("Container Layer",        "Docker Compose",        "Reproducible dev environment: Postgres + API in containers"),
    ]
    for layer, tech, detail in layers:
        row = [[
            Paragraph(f"<b>{layer}</b>", ST["body"]),
            Paragraph(f"<font color='#7B2FBE'>{tech}</font>", ST["body"]),
            Paragraph(detail, ST["body"]),
        ]]
        t = Table(row, colWidths=[130, 130, W - 56 - 260],
                  style=TableStyle([
                      ("BACKGROUND",    (0, 0), (-1, -1), LIGHT_BG),
                      ("TOPPADDING",    (0, 0), (-1, -1), 7),
                      ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                      ("LEFTPADDING",   (0, 0), (-1, -1), 8),
                      ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
                      ("GRID",          (0, 0), (-1, -1), 0.4, GRID_LINE),
                      ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
                      ("LINEBEFORE",    (0, 0), (0, -1),  3, ELECTRIC),
                  ]))
        story.append(t)
        story.append(SP(1))

    story.append(SP(4))
    story.append(P("Request Flow Diagram (Text)", "section"))
    story.append(code_block([
        "  Browser (localhost:3050)",
        "      │",
        "      │  HTTP POST /api/v1/business/ask  { question: '...' }",
        "      ▼",
        "  FastAPI (localhost:8000)",
        "      │  1. sanitize_question()  ← prompt-injection guard",
        "      │  2. classify_question()  → 'business' | 'document' | 'general'",
        "      │",
        "      ├── [business] build_business_context()",
        "      │       │  SELECT summary, top customers, support breakdown, industry",
        "      │       │  customer_risk() per customer  ← risk score + level",
        "      │       └→ structured evidence dict",
        "      │",
        "      ├── [document] search_documents()",
        "      │       │  encode query → vector (384-dim)",
        "      │       │  pgvector cosine search over documents table",
        "      │       └→ top-K passages with similarity scores",
        "      │",
        "      │  3. LLM_API_KEY present?",
        "      │      YES → Gemini.generate_content(evidence + question)",
        "      │      NO  → deterministic _fallback(evidence, question)",
        "      │",
        "      ▼",
        "  { answer, evidence, confidence }  → Browser renders + scrolls to answer",
    ]))
    story.append(SP(3))

    story.append(P("Key Architectural Decisions", "section"))
    decisions = [
        ("Evidence-first design",
         "The LLM never queries the database directly. It receives a pre-built evidence "
         "dictionary from the deterministic layer. This eliminates hallucination of facts and "
         "makes every answer auditable."),
        ("Deterministic fallback",
         "The system works fully without an LLM API key. 16+ question categories are answered "
         "correctly from structured evidence using pattern matching and data aggregation. This makes "
         "the project runnable and demonstrable even in offline/restricted environments."),
        ("Stateless API",
         "No session state is held in the backend. Each request is fully self-contained. "
         "This simplifies scaling and makes the system trivially testable."),
        ("Docker-first development",
         "PostgreSQL and the API run in Docker containers. The frontend runs locally via npm. "
         "This avoids environment-specific issues while keeping the dev loop fast."),
    ]
    for title, body in decisions:
        story.append(KeepTogether([
            P(f"<b>{title}</b>", "subsection"),
            P(body, "body"),
            SP(2),
        ]))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 04 TECHNOLOGY STACK
    # ══════════════════════════════════════════════════════════
    story.append(section_label("04  ·  TECHNOLOGY STACK"))
    story.append(P("Technology Stack", "chapter"))
    story.append(HR(ELECTRIC, 1.5))
    story.append(SP(3))

    story.append(P(
        "Every technology in Business Signal was chosen deliberately. "
        "Here I explain not just what I used, but why.", "body"
    ))
    story.append(SP(3))

    tech_groups = [
        ("Backend & API", [
            ("FastAPI 0.115+", "Python async web framework",
             "Chosen for automatic OpenAPI documentation, async support, Pydantic validation, "
             "and its native fit with modern Python type hints. FastAPI's dependency injection "
             "makes CORS, auth, and middleware trivial to configure."),
            ("Python 3.11", "Runtime",
             "3.11 gives 10–60% speed improvements over 3.9 via specialising adaptive interpreter. "
             "Used in Docker (Python 3.11-slim image) and locally on Python 3.12."),
            ("Pydantic v2", "Data validation",
             "All API request/response bodies validated via Pydantic models. "
             "Field constraints (min_length, ge) enforce correctness at the boundary."),
            ("Uvicorn", "ASGI server",
             "Production-grade ASGI server with uvloop for event loop acceleration. "
             "Runs inside Docker exposing port 8000."),
        ]),
        ("Database & Vector Store", [
            ("PostgreSQL 17", "Primary database",
             "Battle-tested relational database for customers, sales, and support_tickets. "
             "Used with the pgvector extension to also serve as the vector store."),
            ("pgvector", "Vector similarity search",
             "Official PostgreSQL extension enabling vector columns and cosine/inner-product "
             "similarity search. Stores 384-dimensional sentence embeddings for document RAG. "
             "Eliminates the need for a separate vector database like Pinecone or Weaviate."),
            ("psycopg3", "Database driver",
             "Modern async-compatible PostgreSQL driver. Binary protocol, connection pooling, "
             "and proper Decimal/date type handling. Replaced psycopg2 in this project."),
        ]),
        ("AI & Machine Learning", [
            ("Sentence-Transformers", "Embedding model",
             "all-MiniLM-L6-v2 produces 384-dimensional semantic embeddings. Runs locally — "
             "no API call required. Used for RAG document ingestion and query encoding."),
            ("Google Gemini", "LLM (optional)",
             "gemini-3.6-flash via google-genai SDK. Used when LLM_API_KEY is configured. "
             "Receives a pre-built evidence context — it synthesises, not retrieves."),
            ("pypdf", "PDF processing",
             "Extracts text from uploaded PDF documents page by page. Text is chunked with "
             "900-character windows and 120-character overlap before embedding."),
        ]),
        ("Frontend", [
            ("Next.js 14", "React framework",
             "App Router with client components for interactive state. Server-side rendering "
             "for SEO. Environment variables (NEXT_PUBLIC_*) baked at build time."),
            ("Vanilla CSS", "Styling",
             "CSS custom properties for the full design system. No Tailwind, no CSS-in-JS. "
             "Dark-mode neon aesthetic with glassmorphism, smooth transitions, and "
             "responsive grid layouts."),
            ("TypeScript", "Type safety",
             "Full type annotations on all API response shapes, component props, and state. "
             "Catches mismatches between API contract and UI at compile time."),
        ]),
        ("Infrastructure & Tooling", [
            ("Docker Compose", "Container orchestration",
             "Two-service compose file: postgres (pgvector image) + api (custom Python image). "
             "Health checks ensure API waits for Postgres before starting."),
            ("GitHub Actions", "CI/CD",
             "Automated test pipeline runs on every push. Executes the full pytest suite "
             "and the evaluation harness against a real Postgres instance."),
            ("pytest", "Testing framework",
             "21 unit tests across prompt injection, SQL security, data API, and intelligence "
             "modules. Separate evaluation harness with 4 deterministic risk assessments."),
        ]),
    ]

    for group_name, techs in tech_groups:
        story.append(P(group_name, "section"))
        story.append(SP(2))
        for name, category, desc in techs:
            row = [[
                Paragraph(f"<b>{name}</b><br/><font color='#7B2FBE' size='7'>{category}</font>", ST["body"]),
                Paragraph(desc, ST["body"]),
            ]]
            t = Table(row, colWidths=[120, W - 56 - 120],
                      style=TableStyle([
                          ("BACKGROUND",    (0, 0), (-1, -1), LIGHT_BG),
                          ("TOPPADDING",    (0, 0), (-1, -1), 8),
                          ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                          ("LEFTPADDING",   (0, 0), (-1, -1), 10),
                          ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
                          ("GRID",          (0, 0), (-1, -1), 0.4, GRID_LINE),
                          ("VALIGN",        (0, 0), (-1, -1), "TOP"),
                          ("LINEBEFORE",    (0, 0), (0, -1),  3, PURPLE),
                      ]))
            story.append(t)
            story.append(SP(1.5))
        story.append(SP(3))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 05 BACKEND ENGINEERING
    # ══════════════════════════════════════════════════════════
    story.append(section_label("05  ·  BACKEND ENGINEERING"))
    story.append(P("Backend Engineering", "chapter"))
    story.append(HR(ELECTRIC, 1.5))
    story.append(SP(3))

    story.append(P("Module Structure", "section"))
    story.append(SP(2))
    modules = [
        ("main.py",         "Application entry",  "FastAPI app, CORS, router registration, health setup"),
        ("config.py",       "Configuration",      "Settings dataclass reading from env vars (DATABASE_URL, LLM_API_KEY, etc.)"),
        ("database.py",     "DB connection",      "psycopg3 connection pool, SQLite fallback wrapper for testing"),
        ("business.py",     "Core analytics",     "customer_risk() and top_customers() — pure deterministic analysis"),
        ("business_api.py", "REST endpoints",     "summary, revenue-trend, top-customers, risk, decision, sql, ask routes"),
        ("decision.py",     "Answer engine",      "customer_decision(), answer(), and the _fallback() intelligence"),
        ("intelligence.py", "Evidence builder",   "classify_question(), build_business_context(), gather_evidence()"),
        ("sql_agent.py",    "SQL generation",     "generate_sql() via Gemini, validate_sql() with write-op block"),
        ("data_api.py",     "CSV ingestion",      "analyze, upload with fuzzy column mapping — 40+ alias variants"),
        ("retrieval.py",    "RAG pipeline",       "ingest_pdf(), search_documents() using pgvector cosine similarity"),
        ("prompt_guard.py", "Security",           "sanitize_question() blocks prompt injection patterns"),
        ("health.py",       "System health",      "readiness probe and metrics snapshot endpoint"),
        ("metrics.py",      "Runtime metrics",    "Lightweight uptime/request counter (created this session)"),
    ]
    data_rows = [[Paragraph(m, ST["body"]), Paragraph(f"<font color='#7B2FBE'>{c}</font>", ST["body"]),
                  Paragraph(d, ST["body"])] for m, c, d in modules]
    story.append(info_table(
        [Paragraph(h, ST["label"]) for h in ["Module", "Role", "Responsibility"]],
        data_rows,
        col_widths=[105, 90, W - 56 - 195]
    ))
    story.append(SP(5))

    story.append(P("Risk Scoring Algorithm", "section"))
    story.append(P(
        "The risk engine in <b>business.py</b> is deterministic — no LLM, no probability. "
        "It calculates a 0–100 risk score for each customer using three signals:", "body"
    ))
    story.append(SP(2))
    story.append(code_block([
        "# Revenue trend: compare trailing 90 days vs prior 90 days",
        "revenue_drop = (previous - revenue) / previous * 100  if previous > 0 else 0",
        "",
        "# Risk score formula",
        "score = min(100, max(0,",
        "    int(revenue_drop * 1.2)   # revenue decline weighted 1.2x",
        "  + tickets * 8              # open tickets: 8 pts each",
        "  + open_high * 12           # high-priority tickets: 12 pts each",
        "))",
        "",
        "# Risk level thresholds",
        "level = 'HIGH'   if score >= 60 else",
        "        'MEDIUM' if score >= 30 else 'LOW'",
    ]))
    story.append(SP(3))

    story.append(P("Database Connection Layer", "section"))
    story.append(P(
        "The database module uses a context manager pattern so every connection is automatically "
        "returned to the pool. For the test suite, an in-memory SQLite wrapper "
        "implements the same interface so tests run without Docker.", "body"
    ))
    story.append(code_block([
        "# Production: psycopg3 with connection string from DATABASE_URL",
        "with get_connection() as conn:",
        "    rows = conn.execute('SELECT ...').fetchall()",
        "    conn.commit()",
        "",
        "# Test environment: SQLiteConnectionWrapper",
        "# Same API, zero Docker dependency",
    ]))
    story.append(SP(3))

    story.append(P("API Route Design", "section"))
    api_routes = [
        ["Method", "Route", "Description"],
        ["GET",  "/health",                      "Returns service name and version"],
        ["GET",  "/health/ready",                "Confirms DB connectivity"],
        ["GET",  "/metrics",                     "Uptime and request counters"],
        ["GET",  "/api/v1/business/summary",     "Customer count, total revenue, tickets"],
        ["GET",  "/api/v1/business/revenue-trend","Daily revenue time series"],
        ["GET",  "/api/v1/business/top-customers","Customers ranked by revenue"],
        ["POST", "/api/v1/business/risk",         "Risk score for a specific customer_id"],
        ["POST", "/api/v1/business/decision/{id}","INTERVENE/MONITOR decision with reasons"],
        ["POST", "/api/v1/business/sql",          "Convert question to SQL, execute, return"],
        ["POST", "/api/v1/business/ask",          "Full intelligence pipeline answer"],
        ["POST", "/api/v1/data/analyze",          "Inspect CSV columns, suggest mapping"],
        ["POST", "/api/v1/data/upload",           "Import CSV with resolved column mapping"],
    ]
    story.append(info_table(
        api_routes[0],
        [[Paragraph(c, ST["body"]) for c in row] for row in api_routes[1:]],
        col_widths=[42, 175, W - 56 - 217]
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 06 AI & INTELLIGENCE LAYER
    # ══════════════════════════════════════════════════════════
    story.append(section_label("06  ·  AI & INTELLIGENCE LAYER"))
    story.append(P("AI & Intelligence Layer", "chapter"))
    story.append(HR(ELECTRIC, 1.5))
    story.append(SP(3))

    story.append(P("Question Intent Classification", "section"))
    story.append(P(
        "Before any data is fetched, every question goes through <b>classify_question()</b> in "
        "<i>intelligence.py</i>. This lightweight function uses keyword matching to route the "
        "question to the right data source — no LLM call required.", "body"
    ))
    story.append(code_block([
        "def classify_question(question: str) -> str:",
        "    q = question.lower()",
        "    if any(x in q for x in ['policy', 'contract', 'document', 'refund', 'pdf']):",
        "        return 'document'   # → vector search over uploaded PDFs",
        "    if any(x in q for x in ['customer', 'revenue', 'sales', 'risk', 'churn', ...]):",
        "        return 'business'   # → structured DB queries + risk engine",
        "    return 'general'        # → both sources",
    ]))
    story.append(SP(4))

    story.append(P("Retrieval-Augmented Generation (RAG)", "section"))
    story.append(P(
        "The RAG pipeline in <b>retrieval.py</b> enables the system to answer questions about "
        "uploaded PDF documents. The pipeline has two phases:", "body"
    ))
    story.append(SP(2))

    rag_phases = [
        ("Ingestion (offline)", [
            "PDF is uploaded via the /documents endpoint",
            "pypdf extracts text page by page",
            "Text chunked: 900-char windows with 120-char overlap",
            "each chunk encoded → 384-dim vector via all-MiniLM-L6-v2",
            "Vectors stored in PostgreSQL documents table via pgvector",
        ]),
        ("Retrieval (at query time)", [
            "User question encoded to 384-dim query vector",
            "pgvector cosine similarity search: SELECT ... ORDER BY embedding <=> query",
            "Top-K passages returned (default K=5, configurable via TOP_K env var)",
            "Passages included in evidence context sent to LLM",
            "Source document and page number cited in response",
        ]),
    ]
    for phase, steps in rag_phases:
        story.append(P(f"<b>{phase}</b>", "subsection"))
        for step in steps:
            story.append(P(f"<b>→</b>  {step}", "bullet"))
        story.append(SP(2))

    story.append(SP(2))
    story.append(highlight_box(
        "<b>Why pgvector over a dedicated vector database?</b>  "
        "At this project's scale, adding Pinecone or Weaviate would be operational overhead with no benefit. "
        "pgvector runs inside the existing PostgreSQL instance, keeps the architecture simple, "
        "and supports production workloads at millions of vectors.",
        ACCENT, HexColor("#E8F8FF")
    ))
    story.append(SP(5))

    story.append(P("Natural-Language SQL Agent", "section"))
    story.append(P(
        "The SQL agent in <b>sql_agent.py</b> converts a natural-language question into a "
        "safe PostgreSQL SELECT query. When no LLM key is available, a keyword-based fallback "
        "generates common queries deterministically.", "body"
    ))
    story.append(SP(2))

    story.append(P("Security model for SQL agent:", "subsection"))
    sql_security = [
        "Regex validation blocks any query not starting with SELECT",
        "Forbidden keywords: INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, GRANT, REVOKE, COPY, CALL",
        "Semicolon detection prevents multi-statement injection",
        "Explicit schema provided to LLM — only known tables can be referenced",
        "LIMIT automatically appended if missing — maximum 100 rows returned",
    ]
    for s in bullet_list(sql_security):
        story.append(s)

    story.append(SP(4))
    story.append(P("Deterministic Intelligence Fallback", "section"))
    story.append(P(
        "This is the feature I'm most proud of engineering. When no LLM API key is set, "
        "the <b>_fallback()</b> function in <i>decision.py</i> answers 16+ distinct question "
        "categories correctly from the pre-fetched evidence dictionary. The routing uses "
        "precise keyword matching with priority ordering to avoid ambiguity.", "body"
    ))
    story.append(SP(2))

    fallback_cats = [
        ["Category", "Example Question", "Answer Source"],
        ["Risk analysis",       "Which customers are at risk and why?",   "risk_analysis list, risk_score, revenue_drop"],
        ["Total revenue",       "What is the total revenue?",             "summary.total_revenue"],
        ["Industry revenue",    "Which industry generated most revenue?", "industry_summary[0] sorted by revenue"],
        ["Industry customers",  "Which industries have most customers?",  "industry_summary sorted by count"],
        ["Top customers",       "Show top 5 customers by revenue",        "top_customers[:5]"],
        ["Least revenue",       "Which customer generated least revenue?","top_customers[-1]"],
        ["Customer count",      "How many customers do we have?",         "summary.customers"],
        ["Support breakdown",   "Support breakdown by priority",          "support_breakdown list"],
        ["High-priority",       "High-priority tickets open?",            "summary.high_priority_tickets"],
        ["Support load",        "What is the current support load?",      "summary.open_tickets"],
        ["Business snapshot",   "What is the business health?",           "Full summary combined"],
        ["Revenue trend",       "What is the revenue trend?",             "Context + note about time-series"],
        ["Average sale",        "What is the average sale amount?",       "Revenue / customers with note"],
    ]
    story.append(info_table(
        fallback_cats[0],
        [[Paragraph(c, ST["body"]) for c in row] for row in fallback_cats[1:]],
        col_widths=[90, 150, W - 56 - 240]
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 07 FRONTEND
    # ══════════════════════════════════════════════════════════
    story.append(section_label("07  ·  FRONTEND APPLICATION"))
    story.append(P("Frontend Application", "chapter"))
    story.append(HR(ELECTRIC, 1.5))
    story.append(SP(3))

    story.append(P(
        "The frontend is a Next.js 14 application using the App Router. "
        "It is a single-page experience with three sections: the AI question interface, "
        "the CSV data import panel, and the live results dashboard.", "body"
    ))
    story.append(SP(3))

    story.append(P("Design System", "section"))
    story.append(P(
        "Built entirely with vanilla CSS custom properties — no Tailwind, no CSS framework. "
        "The aesthetic is a dark neon palette with electric cyan and deep purple accents. "
        "Design principles: glassmorphism cards, smooth micro-animations, hover states on "
        "every interactive element, and responsive layouts down to mobile viewports.", "body"
    ))
    story.append(SP(3))

    story.append(P("Key UX Features", "section"))
    ux_features = [
        "<b>Enter to submit:</b> pressing Enter in the question textarea submits immediately; Shift+Enter inserts a newline",
        "<b>Auto-scroll to answer:</b> after an answer arrives, the page smoothly scrolls to the answer block",
        "<b>Question guide:</b> 30+ categorised example questions toggle open/closed with animation",
        "<b>One-click question loading:</b> clicking any example pre-fills the textarea and scrolls to the input",
        "<b>Evidence trace panel:</b> the raw JSON evidence used to produce each answer is displayed live",
        "<b>CSV mapper:</b> drag-and-drop upload with column inspection, fuzzy mapping, and import flow",
        "<b>Live stats dashboard:</b> customer count, total revenue, open tickets, high-priority count",
        "<b>Show all customers:</b> top-customers table expands from 6 to full list on demand",
    ]
    for f in bullet_list(ux_features):
        story.append(f)
    story.append(SP(4))

    story.append(P("State Management", "section"))
    story.append(P(
        "All state is local React <b>useState</b> hooks — no Redux, no Zustand, no Context. "
        "The application is simple enough that global state management would be over-engineering. "
        "Server state is fetched fresh on load via <b>useEffect</b> and after each CSV import.", "body"
    ))
    story.append(SP(3))

    story.append(P("Environment Configuration", "section"))
    story.append(code_block([
        "# frontend/.env.local",
        "NEXT_PUBLIC_API_URL=http://localhost:8000",
        "",
        "# The NEXT_PUBLIC_ prefix is required — Next.js only exposes",
        "# env vars with this prefix to the browser bundle at build time.",
        "# Without this file the variable would be undefined in the client.",
    ]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 08 DATABASE DESIGN
    # ══════════════════════════════════════════════════════════
    story.append(section_label("08  ·  DATABASE DESIGN"))
    story.append(P("Database Design", "chapter"))
    story.append(HR(ELECTRIC, 1.5))
    story.append(SP(3))

    story.append(P("Schema Overview", "section"))
    schema = [
        ["Table", "Columns", "Purpose"],
        ["customers",       "id, name, industry, annual_value",                              "Master customer record"],
        ["sales",           "id, customer_id, amount, sale_date",                            "Individual sale transactions"],
        ["support_tickets", "id, customer_id, priority, status, subject, created_at",        "Customer support requests"],
        ["documents",       "id, source, page, content, embedding (vector 384), created_at", "RAG document chunks + vectors"],
    ]
    story.append(info_table(
        schema[0],
        [[Paragraph(c, ST["body"]) for c in row] for row in schema[1:]],
        col_widths=[90, 210, W - 56 - 300]
    ))
    story.append(SP(4))

    story.append(P("Key SQL Patterns", "section"))
    story.append(code_block([
        "-- Customer risk: 90-day revenue vs prior 90-day window",
        "SELECT COALESCE(SUM(amount), 0) FROM sales",
        "WHERE customer_id = %s",
        "  AND sale_date >= CURRENT_DATE - INTERVAL '90 days'",
        "",
        "-- Industry revenue aggregation (requires explicit alias for ORDER BY)",
        "SELECT c.industry,",
        "       COUNT(DISTINCT c.id),",
        "       COALESCE(SUM(s.amount), 0) AS revenue  -- alias is required!",
        "FROM customers c LEFT JOIN sales s ON s.customer_id = c.id",
        "GROUP BY c.industry ORDER BY revenue DESC",
        "",
        "-- Vector similarity search (cosine distance)",
        "SELECT source, page, content,",
        "       1 - (embedding <=> %s::vector) AS score",
        "FROM documents WHERE embedding IS NOT NULL",
        "ORDER BY embedding <=> %s::vector LIMIT %s",
    ]))
    story.append(SP(3))

    story.append(highlight_box(
        "<b>Bug fixed during development:</b> The industry revenue query originally used "
        "<b>ORDER BY revenue DESC</b> without an explicit column alias. PostgreSQL requires the "
        "alias to exist in the SELECT clause for ORDER BY to reference it by name. SQLite allows "
        "it without the alias, masking the bug in tests. Adding <b>AS revenue</b> fixed the "
        "production crash and made 3 integration tests pass.",
        WARN, HexColor("#FFF8EE")
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 09 API REFERENCE
    # ══════════════════════════════════════════════════════════
    story.append(section_label("09  ·  API REFERENCE"))
    story.append(P("API Reference", "chapter"))
    story.append(HR(ELECTRIC, 1.5))
    story.append(SP(3))

    story.append(P("Business Intelligence Endpoints", "section"))
    endpoints = [
        ("GET /api/v1/business/summary",
         "No body",
         '{ "customers": 1310, "total_revenue": 1606000.6, "open_tickets": 14, "high_priority_tickets": 2 }',
         "Dashboard KPI snapshot"),
        ("GET /api/v1/business/top-customers?limit=10",
         "Query param: limit (1–50)",
         '{ "customers": [{ "customer_id": 10, "customer": "UrbanCart", "industry": "E-commerce", "revenue": 233383.6 }] }',
         "Revenue-ranked customer list"),
        ("POST /api/v1/business/ask",
         '{ "question": "Which customers are at risk?" }',
         '{ "answer": "...", "evidence": { "intent": "business", "business": {...} } }',
         "Full intelligence pipeline"),
        ("POST /api/v1/business/risk",
         '{ "customer_id": 3 }',
         '{ "risk_score": 86, "risk_level": "HIGH", "revenue_drop_percent": 48.6 }',
         "Customer risk assessment"),
    ]
    for route, req, resp, desc in endpoints:
        story.append(KeepTogether([
            P(f"<font color='#00D4FF'><b>{route}</b></font>", "subsection"),
            P(f"<i>Description:</i> {desc}", "body"),
            P(f"<i>Request:</i> <font face='Courier' size='8'>{req}</font>", "body"),
            P(f"<i>Response:</i> <font face='Courier' size='8'>{resp[:120]}...</font>", "body"),
            SP(3),
        ]))

    story.append(P("Data Import Endpoints", "section"))
    story.append(SP(2))
    story.append(P(
        "<b>POST /api/v1/data/analyze</b> — Upload a CSV file and receive the detected dataset type, "
        "auto-suggested column mapping, missing fields, and a 5-row sample. No data is written.", "body"
    ))
    story.append(SP(2))
    story.append(P(
        "<b>POST /api/v1/data/upload</b> — Upload CSV with confirmed column mapping. "
        "Optionally truncate existing data with <i>replace=true</i>. "
        "Supports multi-format date parsing (YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY).", "body"
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 10 SECURITY ENGINEERING
    # ══════════════════════════════════════════════════════════
    story.append(section_label("10  ·  SECURITY ENGINEERING"))
    story.append(P("Security Engineering", "chapter"))
    story.append(HR(ELECTRIC, 1.5))
    story.append(SP(3))

    story.append(P(
        "For a project that takes free-text input and sends it to an LLM and a SQL database, "
        "security is not optional. Business Signal has three layers of protection.", "body"
    ))
    story.append(SP(3))

    story.append(P("1. Prompt Injection Guard", "section"))
    story.append(P(
        "Every question passes through <b>sanitize_question()</b> in <i>prompt_guard.py</i> "
        "before touching the LLM or SQL agent. Four regex patterns detect common injection attempts:", "body"
    ))
    story.append(code_block([
        "INJECTION_PATTERNS = [",
        "    r'ignore\\s+(all\\s+)?previous instructions',",
        "    r'reveal\\s+(the\\s+)?system prompt',",
        "    r'show\\s+(me\\s+)?your\\s+hidden instructions',",
        "    r'disregard\\s+the\\s+rules',",
        "]",
        "",
        "def sanitize_question(text: str) -> str:",
        "    if is_suspicious(text):  # case-insensitive regex match",
        "        raise ValueError('Question rejected by prompt-injection guard')",
        "    return text.strip()",
    ]))
    story.append(SP(4))

    story.append(P("2. SQL Injection Prevention", "section"))
    story.append(P(
        "The SQL agent has a multi-layer defence against SQL injection and data exfiltration:", "body"
    ))
    security_sql = [
        "All queries validated with regex to start with SELECT",
        "Forbidden keywords regex blocks all write/DDL operations (11 keywords)",
        "Semicolon check prevents multi-statement injection",
        "Only the known schema is provided to the LLM — unknown tables are unreferenceable",
        "LIMIT 100 enforced on all results to prevent data dumping",
        "Parameterised queries used everywhere in the business logic layer",
    ]
    for s in bullet_list(security_sql):
        story.append(s)
    story.append(SP(4))

    story.append(P("3. CORS Configuration", "section"))
    story.append(P(
        "Cross-Origin Resource Sharing is explicitly configured to only allow the frontend "
        "origins. The allowed origins list is configurable via the <b>CORS_ORIGINS</b> environment "
        "variable, defaulting to localhost ports 3000 and 3050.", "body"
    ))
    story.append(code_block([
        "app.add_middleware(CORSMiddleware,",
        "    allow_origins=cors_origins,",
        "    allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],",
        "    allow_headers=['*'],",
        "    allow_credentials=False,",
        ")",
    ]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 11 TESTING & EVALUATION
    # ══════════════════════════════════════════════════════════
    story.append(section_label("11  ·  TESTING & EVALUATION"))
    story.append(P("Testing & Evaluation", "chapter"))
    story.append(HR(ELECTRIC, 1.5))
    story.append(SP(3))

    story.append(metric_row([
        ("21 / 21", "Unit tests pass",     "#00C896"),
        ("4 / 4",   "Eval tests pass",     "#00D4FF"),
        ("0",       "Errors or warnings",  "#7B2FBE"),
        ("7.66s",   "Full suite runtime",  "#FF8C00"),
    ]))
    story.append(SP(5))

    story.append(P("Unit Test Coverage", "section"))
    test_files = [
        ["Test file", "Tests", "What is verified"],
        ["test_prompt_guard.py",   "4",  "Normal questions pass, 3 injection patterns detected"],
        ["test_sql_agent.py",      "5",  "SELECT allowed, 4 write/DDL variants blocked"],
        ["test_sql_security.py",   "4",  "Duplicate SQL security coverage in backend/tests/"],
        ["test_data_api.py",       "2",  "Alternate column name aliases resolve correctly"],
        ["test_intelligence.py",   "3",  "Risk context, revenue context, summary evidence all built"],
    ]
    story.append(info_table(
        test_files[0],
        [[Paragraph(c, ST["body"]) for c in row] for row in test_files[1:]],
        col_widths=[150, 40, W - 56 - 190]
    ))
    story.append(SP(4))

    story.append(P("Evaluation Harness", "section"))
    story.append(P(
        "Beyond unit tests, Business Signal has a separate evaluation suite in "
        "<b>evaluation/run.py</b> that tests the full pipeline end-to-end against a live "
        "Postgres database:", "body"
    ))
    story.append(code_block([
        "# evaluation/run.py — 4 deterministic risk assessments",
        "Q001: customer_id=3  (Apex Logistics)   → expected HIGH  ✓ PASS",
        "Q002: customer_id=7  (Pulse Media)       → expected HIGH  ✓ PASS",
        "Q003: customer_id=1  (Nova Retail)       → expected LOW   ✓ PASS",
        "Q004: customer_id=2  (Vertex Systems)    → expected LOW   ✓ PASS",
        "",
        "Result: 4/4 passed",
    ]))
    story.append(SP(3))

    story.append(P("GitHub Actions CI", "section"))
    story.append(P(
        "Every push to the repository triggers an automated pipeline that spins up a "
        "PostgreSQL service container, runs all pytest tests, and runs the evaluation harness. "
        "This ensures no regression is introduced unnoticed.", "body"
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 12 DATA INGESTION PIPELINE
    # ══════════════════════════════════════════════════════════
    story.append(section_label("12  ·  DATA INGESTION PIPELINE"))
    story.append(P("Data Ingestion Pipeline", "chapter"))
    story.append(HR(ELECTRIC, 1.5))
    story.append(SP(3))

    story.append(P(
        "Business Signal accepts CSV uploads for customers, sales, and support tickets. "
        "The ingestion pipeline handles real-world messiness: non-standard column names, "
        "mixed date formats, customer name lookups instead of IDs.", "body"
    ))
    story.append(SP(3))

    story.append(P("Column Alias Resolution", "section"))
    story.append(P(
        "The mapper in <b>data_api.py</b> normalises column names (lower, strip, alphanumeric only) "
        "and checks against 40+ pre-defined alias sets. This means a file with columns named "
        "<i>Company Name</i>, <i>ARR</i>, and <i>Vertical</i> will map correctly to "
        "<i>name</i>, <i>annual_value</i>, and <i>industry</i> automatically.", "body"
    ))
    story.append(SP(2))

    alias_examples = [
        ["Target field",    "Accepted column name variants (partial list)"],
        ["name",           "customer, company, account, organization, client_name"],
        ["annual_value",   "arr, acv, contract_value, yearly_revenue, customer_value"],
        ["sale_date",      "date, closed_at, transaction_date, order_date, invoice_date"],
        ["customer_id",    "account_id, client_id, company_id, customer_name, company"],
        ["priority",       "severity, urgency, ticket_priority"],
        ["status",         "ticket_status, state, case_status"],
    ]
    story.append(info_table(
        alias_examples[0],
        [[Paragraph(c, ST["body"]) for c in row] for row in alias_examples[1:]],
        col_widths=[100, W - 56 - 100]
    ))
    story.append(SP(4))

    story.append(P("Date Format Support", "section"))
    story.append(P(
        "The <b>_parse_date()</b> helper tries four common formats in order, giving informative "
        "error messages when none match:", "body"
    ))
    story.append(code_block([
        "Supported date formats (tried in order):",
        "  YYYY-MM-DD  (ISO 8601, preferred)",
        "  DD/MM/YYYY  (European)",
        "  MM/DD/YYYY  (US)",
        "  DD-MM-YYYY  (hyphenated European)",
    ]))
    story.append(SP(4))

    story.append(P("Customer Reference Resolution", "section"))
    story.append(P(
        "When importing sales or tickets, the <b>customer_id</b> field can be either a numeric ID "
        "or a customer name string. <b>_customer_ref()</b> tries the numeric parse first, then "
        "falls back to a case-insensitive name lookup. This allows importing files that reference "
        "customers by name, not just by database ID.", "body"
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 13 DEPLOYMENT ARCHITECTURE
    # ══════════════════════════════════════════════════════════
    story.append(section_label("13  ·  DEPLOYMENT ARCHITECTURE"))
    story.append(P("Deployment Architecture", "chapter"))
    story.append(HR(ELECTRIC, 1.5))
    story.append(SP(3))

    story.append(P(
        "The project ships with a Docker Compose configuration that makes local setup a "
        "single command. The architecture is intentionally minimal — two containers "
        "plus a local Next.js process.", "body"
    ))
    story.append(SP(3))

    story.append(code_block([
        "# docker-compose.yml",
        "services:",
        "  postgres:",
        "    image: pgvector/pgvector:pg17",
        "    environment:",
        "      POSTGRES_DB: business_signal",
        "      POSTGRES_USER: business_signal",
        "      POSTGRES_PASSWORD: business_signal",
        "    ports: ['5432:5432']",
        "    healthcheck:",
        "      test: ['CMD-SHELL', 'pg_isready -U business_signal']",
        "",
        "  api:",
        "    build: ./backend",
        "    environment:",
        "      DATABASE_URL: postgresql://...",
        "      LLM_API_KEY: ${LLM_API_KEY:-}",
        "    ports: ['8000:8000']",
        "    depends_on:",
        "      postgres: { condition: service_healthy }",
    ]))
    story.append(SP(4))

    story.append(P("One-Command Setup", "section"))
    story.append(code_block([
        "# 1. Start backend + database",
        "docker compose up --build",
        "",
        "# 2. Start frontend (separate terminal)",
        "cd frontend && npm install && npm run dev",
        "",
        "# 3. Open browser",
        "http://localhost:3050",
        "",
        "# Optional: enable Gemini AI answers",
        "# Add LLM_API_KEY=your_gemini_key to .env",
    ]))
    story.append(SP(4))

    story.append(P("Port Configuration", "section"))
    ports = [
        ["Service", "Port", "Note"],
        ["PostgreSQL",   "5432", "Docker-mapped, only accessible from API container and localhost"],
        ["FastAPI API",  "8000", "Docker-mapped, accessible from browser and Next.js frontend"],
        ["Next.js UI",   "3050", "Local dev server (3000 reserved by Windows on this machine)"],
    ]
    story.append(info_table(
        ports[0],
        [[Paragraph(c, ST["body"]) for c in row] for row in ports[1:]],
        col_widths=[100, 50, W - 56 - 150]
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 14 PERFORMANCE
    # ══════════════════════════════════════════════════════════
    story.append(section_label("14  ·  PERFORMANCE & SCALABILITY"))
    story.append(P("Performance & Scalability", "chapter"))
    story.append(HR(ELECTRIC, 1.5))
    story.append(SP(3))

    story.append(P("Response Time Profile", "section"))
    perf = [
        ["Operation",                 "Typical latency",  "Bottleneck"],
        ["GET /summary",              "< 10ms",           "Single SQL aggregation"],
        ["GET /top-customers",        "< 20ms",           "JOIN + ORDER BY"],
        ["POST /ask (no LLM)",        "50–200ms",         "50 customer risk calculations"],
        ["POST /ask (with Gemini)",   "1–4s",             "Gemini network round-trip"],
        ["POST /data/analyze",        "< 100ms",          "CSV parse + mapping check"],
        ["POST /data/upload (1k rows)","200–500ms",       "executemany batch insert"],
        ["PDF ingest (10 pages)",     "2–5s",             "Sentence-Transformer encoding"],
        ["Vector search",             "< 30ms",           "pgvector cosine scan"],
    ]
    story.append(info_table(
        perf[0],
        [[Paragraph(c, ST["body"]) for c in row] for row in perf[1:]],
        col_widths=[155, 80, W - 56 - 235]
    ))
    story.append(SP(4))

    story.append(P("Scalability Considerations", "section"))
    scale_items = [
        "<b>Sentence-Transformer caching:</b> the embedding model is loaded once on first use and cached in-process — no reload per request",
        "<b>Risk calculation at scale:</b> the current loop over all customers is O(n). At 10,000+ customers, precomputing risk on a schedule would be needed",
        "<b>pgvector indexing:</b> for large document collections an IVFFlat or HNSW index on the embedding column should be created",
        "<b>Connection pooling:</b> psycopg3 supports async connection pools — the current synchronous model suits this demo's concurrency needs",
        "<b>LLM cost:</b> Gemini Flash is used specifically for its low cost and high speed — evidence-first design minimises token usage by pruning context",
    ]
    for item in bullet_list(scale_items):
        story.append(item)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 15 FUTURE ROADMAP
    # ══════════════════════════════════════════════════════════
    story.append(section_label("15  ·  FUTURE ROADMAP"))
    story.append(P("Future Roadmap", "chapter"))
    story.append(HR(ELECTRIC, 1.5))
    story.append(SP(3))

    story.append(P(
        "Business Signal is a project showcase, not a production product. These are the "
        "extensions that would make logical next steps if taken to production:", "body"
    ))
    story.append(SP(3))

    roadmap = [
        ("Authentication & Multi-tenancy",
         "Add JWT-based authentication so multiple businesses can each have isolated data. "
         "Row-level security in PostgreSQL would enforce data isolation cleanly."),
        ("Streaming Answers",
         "Use Gemini's streaming API to show the answer token-by-token in the UI. "
         "Server-Sent Events or WebSockets from FastAPI to Next.js."),
        ("Scheduled Risk Alerts",
         "Background job (APScheduler or Celery) that computes risk scores nightly and "
         "sends email/Slack alerts when accounts cross the HIGH threshold."),
        ("Excel / Google Sheets Import",
         "Extend the data ingestion pipeline to accept .xlsx files and Google Sheets URLs, "
         "removing the CSV conversion step for most business users."),
        ("Revenue Forecasting",
         "Add a time-series forecasting module (Prophet or statsmodels) to project revenue "
         "30/60/90 days forward per customer and per industry."),
        ("Interactive Charts",
         "Add Chart.js or Recharts to the frontend to visualise the revenue trend, "
         "risk distribution, and industry breakdown as dynamic charts."),
        ("pgvector HNSW Index",
         "Migrate document embeddings to an HNSW approximate nearest-neighbour index for "
         "sub-millisecond vector search at millions of document chunks."),
        ("LLM Function Calling",
         "Replace the keyword classifier with Gemini function-calling to let the LLM "
         "choose which tools to invoke — a step toward a proper agent architecture."),
    ]

    for i, (title, desc) in enumerate(roadmap):
        row = [[
            Paragraph(f"<font color='#00D4FF'><b>{i+1:02d}</b></font>", ST["body_center"]),
            Paragraph(f"<b>{title}</b><br/>{desc}", ST["body"]),
        ]]
        t = Table(row, colWidths=[26, W - 56 - 26],
                  style=TableStyle([
                      ("BACKGROUND",    (0, 0), (-1, -1), LIGHT_BG if i % 2 == 0 else WHITE),
                      ("TOPPADDING",    (0, 0), (-1, -1), 9),
                      ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
                      ("LEFTPADDING",   (0, 0), (-1, -1), 8),
                      ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
                      ("GRID",          (0, 0), (-1, -1), 0.3, GRID_LINE),
                      ("VALIGN",        (0, 0), (-1, -1), "TOP"),
                  ]))
        story.append(t)

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 16 CONCLUSION
    # ══════════════════════════════════════════════════════════
    story.append(section_label("16  ·  CONCLUSION"))
    story.append(P("Conclusion", "chapter"))
    story.append(HR(ELECTRIC, 1.5))
    story.append(SP(3))

    story.append(P(
        "Business Signal started with a question: <i>what does a responsible AI system "
        "that answers business questions actually look like?</i> Not a wrapper around a chat API "
        "that makes up numbers — but a deliberate pipeline where every answer is earned "
        "through evidence.", "body"
    ))
    story.append(SP(4))

    story.append(highlight_box(
        "The core insight this project demonstrates: <b>AI engineering is not about prompting. "
        "It is about designing the pipeline that decides what evidence the model sees, "
        "validating that evidence is correct, and ensuring the model cannot stray beyond it.</b>",
        ELECTRIC, HexColor("#EEF9FF")
    ))
    story.append(SP(5))

    story.append(P("What I learned and demonstrated:", "section"))
    learnings = [
        "How to build a multi-source evidence pipeline that routes questions to the right tool",
        "How pgvector turns PostgreSQL into a production-ready vector store without a separate service",
        "How to design a deterministic fallback so the system is useful without any API key",
        "How to protect an LLM-integrated system against prompt injection at the boundary",
        "How to validate SQL generated by an LLM so it can never write, drop, or exfiltrate data",
        "How to structure a FastAPI backend with clear module boundaries and a testable connection layer",
        "How to build a polished Next.js frontend with only vanilla CSS and no component library",
        "How to configure Docker Compose health checks so the API never starts before the database is ready",
        "How to write an evaluation harness that tests the full pipeline, not just individual functions",
        "The practical difference between grounded AI answers (citing evidence) and hallucinated ones",
    ]
    for l in bullet_list(learnings):
        story.append(l)

    story.append(SP(5))
    story.append(P("Final Metrics", "section"))
    story.append(metric_row([
        ("13+",  "Backend modules",  "#00D4FF"),
        ("16+",  "API endpoints",    "#7B2FBE"),
        ("21/21","Tests passing",    "#00C896"),
        ("8+",   "Bug fixes shipped",  "#FF8C00"),
    ]))
    story.append(SP(6))

    story.append(P(
        "Thank you for reading. The full source code, commit history, and GitHub Actions "
        "pipeline are available at:", "body_center"
    ))
    story.append(P(
        "<font color='#00D4FF'><b>github.com/ranjiths112007/Business-Signal-enterprise-ai</b></font>",
        "body_center"
    ))
    story.append(SP(8))
    story.append(HR(ELECTRIC, 1.5))
    story.append(SP(3))
    story.append(P(
        f"<font color='#8A9BAE'>Ranjith S  ·  AI Engineering Project  ·  September 2026  ·  "
        f"Built with FastAPI, PostgreSQL, pgvector, Next.js, Docker & Gemini AI</font>",
        "body_center"
    ))

    # ── Build ──────────────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    import os
    out = os.path.join(os.path.dirname(__file__), "Business_Signal_Documentation.pdf")
    build_pdf(out)
