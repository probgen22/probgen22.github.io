"""
Process abstracts to create book.
"""
import csv
import collections
import sys
import textwrap
import dataclasses
import random
from typing import List
import html

import markdown_strings


def md_esc(s):
    return markdown_strings.esc_format(s)


def html_esc(s):
    return html.escape(s)


@dataclasses.dataclass
class Abstract:
    author: str
    coauthors: str
    id: str
    affiliations: str
    title: str
    text: str
    keywords: str
    topics: str

    def _normalise_keywords(self):
        kwds = self.keywords.split(",;")
        self.keywords = ", ".join(kw.title() for kw in kwds)

    def __post_init__(self):
        author = self.author
        j = author.find("[")
        if j != -1:
            author = self.author[:j]
        self.author_last_name = author.split()[-1]
        self.author_first_name = author.split()[0]

        if self.coauthors.startswith(self.author):
            self.coauthors = self.coauthors[len(self.author) :]

        self.author_list = self.author
        if len(self.coauthors) > 0:
            if not self.coauthors.startswith(","):
                self.author_list += ","
            self.author_list += f" {self.coauthors}"
        self.author = author

        self._normalise_keywords()

    def as_html(self, out):
        print(f"<table id='{self.id}'>\n", file=out)

        print("<tr>\n", file=out)
        anchor = (
            f"<a href='abstracts/index.html#{self.id}' title='{self.id}'>{self.id}</a>"
        )
        print(f"\t<td class='date' rowspan='6'>{anchor}</td>\n", file=out)
        print(f"\t<td class='title'>{html_esc(self.title)}</td>\n", file=out)
        print("</tr>\n", file=out)

        authors = html_esc(self.author_list)
        print("<tr>\n", file=out)
        print(f"\t<td class='speaker'>{authors}</td>\n", file=out)
        print("</tr>\n", file=out)

        print("<tr>\n", file=out)
        print(
            "\t<td class='speaker'><b>Affiliations:</b> "
            f"{html_esc(self.affiliations)}</td>\n",
            file=out,
        )
        print("</tr>\n", file=out)

        print("<tr>\n", file=out)
        print(
            f"\t<td class='speaker'><b>Topics:</b> {html_esc(self.topics)}</td>\n",
            file=out,
        )
        print("</tr>\n", file=out)

        print("<tr>\n", file=out)
        if len(self.keywords) > 0:
            print(
                f"\t<td class='speaker'><b>Keywords:</b> "
                f"{html_esc(self.keywords)}</td>\n",
                file=out,
            )
        print("</tr>\n", file=out)

        text = textwrap.indent(textwrap.fill(html_esc(self.text)), prefix="\t\t")
        print("<tr>\n", file=out)
        print(f"\t<td class='abstract'>\n{text}</td>", file=out)
        print("</tr>\n", file=out)
        print("</table>", file=out)


class AbstractBook:
    def __init__(self, abstracts):
        self.abstracts = abstracts

    def as_markdown(self, out):
        for id, abstract in enumerate(self.abstracts):
            abstract.as_markdown(out, id)

    def as_html(self, out):
        for abstract in self.abstracts:
            abstract.as_html(out)


def process_talks(out):

    infile = "data/talks-cleaned.csv"
    abstracts = []
    with open(infile) as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            # print(list(line.keys()))
            id = int(line["Talk Number"])
            abstract = Abstract(
                # email=line["Username"],
                author=line["Presenter name"],
                id=f"T{id:02d}",
                coauthors=line["Coauthors"],
                affiliations=line["Affiliations"],
                title=line["Title"],
                text=line["Abstract (max 1500 characters)"],
                keywords=line["Keywords"],
                topics=", ".join(line["Topics (select all that apply)"].split(";")),
            )
            abstracts.append(abstract)

    abstracts.sort(key=lambda x: x.id)

    title = "Talks"
    print(f"<h3><a name='{title}'>{title}</a></h3>", file=out)
    book = AbstractBook(abstracts)
    book.as_html(out)
    return abstracts


def process_posters(out):

    infile = "data/posters-cleaned.csv"
    abstracts = []
    with open(infile) as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            # print(list(line.keys()))
            abstract = Abstract(
                # email=line["Username"],
                author=line["Presenter name"],
                id=None,
                coauthors=line["Coauthors"],
                affiliations=line["Affiliations"],
                title=line["Title"],
                text=line["Abstract (max 1500 characters)"],
                keywords=line["Keywords"],
                topics=", ".join(line["Topics (select all that apply)"].split(";")),
            )
            abstracts.append(abstract)

    abstracts.sort(key=lambda x: (x.author_last_name, x.author_first_name))
    for j, ab in enumerate(abstracts, 1):
        ab.id = f"P{j:02d}"
        # print(f"{ab.id}-{ab.author_last_name}")

    title = "Posters"
    print(f"<h3><a name='{title}'>{title}</a></h3>", file=out)
    book = AbstractBook(abstracts)
    book.as_html(out)
    return abstracts


def process_authors(abstracts, out):
    by_name = collections.defaultdict(list)
    for ab in abstracts:
        by_name[ab.author_last_name[0]].append(ab)

    print("<h3><a name='Presenter_index'>Presenter index</a></h3>", file=out)
    for letter in sorted(by_name.keys()):
        print(f"<h4>{letter.upper()}</h4>", file=out)
        s = ""
        for abstract in by_name[letter]:
            s += f"<a href='abstracts/index.html#{abstract.id}'>{abstract.author}</a>, "
        s = s[:-2]
        print("<p>", s, "</p>", file=out)


if __name__ == "__main__":
    with open("tmp.html", "w") as f:
        ab1 = process_talks(f)
        ab2 = process_posters(f)
        process_authors(ab1 + ab2, f)
