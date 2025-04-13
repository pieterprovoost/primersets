import pandas as pd
from pathlib import Path
from html import escape


def linkify_code(code):
    return f'<a href="#primer-{escape(code)}">{escape(code)}</a>' if code else ""


def linkify_url(url):
    return f'<a href="{escape(url)}" target="_blank">{escape(url)}</a>' if url else ""


def gene_badge(gene):
    if not gene:
        return ""
    slug = gene.lower().replace(" ", "")
    classes = {
        "coi": "badge-coi",
        "16s": "badge-16s",
        "18s": "badge-18s",
        "12s": "badge-12s",
        "its": "badge-its",
        "its1": "badge-its1",
        "its2": "badge-its2",
        "rbcl": "badge-rbcl",
        "trnl": "badge-trnl",
        "cytb": "badge-cytb",
    }
    css_class = classes.get(slug, "badge-unknown")
    return f'<span class="badge-muted {css_class}">{escape(gene)}</span>'


sets_df = pd.read_csv("sets.tsv", sep="\t").fillna("")
primers_df = pd.read_csv("primers.tsv", sep="\t").fillna("")

sets_df["forward"] = sets_df["forward"].apply(linkify_code)
sets_df["reverse"] = sets_df["reverse"].apply(linkify_code)
sets_df["link"] = sets_df["link"].apply(linkify_url)

sets_df["target_gene"] = sets_df["target_gene"].apply(gene_badge)
primers_df["target_gene"] = primers_df["target_gene"].apply(gene_badge)

primers_df["code"] = primers_df["code"].apply(
    lambda code: f'<a id="primer-{escape(code)}">{escape(code)}</a>' if code else ""
)
primers_df["link"] = primers_df["link"].apply(linkify_url)

primers_df["based_on"] = primers_df["based_on"].apply(
    lambda code: f'<a href="#primer-{escape(code)}">{escape(code)}</a>' if code else ""
)

primers_df["sequence"] = primers_df["sequence"].apply(
    lambda seq: f'<span class="sequence">{seq}</span>' if seq else ""
)

sets_html = sets_df.to_html(index=False, escape=False, classes="table table-striped table-sm")
primers_html = primers_df.to_html(index=False, escape=False, classes="table table-striped table-sm")

template = Path("templates/index.html").read_text()
html = template.replace("{{SETS_TABLE}}", sets_html).replace("{{PRIMERS_TABLE}}", primers_html)

Path("docs").mkdir(parents=True, exist_ok=True)
Path("docs/.nojekyll").write_text("")
Path("docs/index.html").write_text(html)
