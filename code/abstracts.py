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
    email: str
    author: str
    coauthors: str
    id: str
    affiliations: str
    title: str
    text: str
    keywords: str
    topics: str

    def __post_init__(self):
        self.author_last_name = self.author.split()[-1]

    def check_authors(self):
        if self.coauthors.startswith(self.author):
            self.coauthors = self.coauthors[len(self.author):]

    def as_markdown(self, out, submission_id=None):
        print(f"# {md_esc(self.title)}", file=out)

        if submission_id is not None:
            print(f"**Submission ID:** {submission_id}", file=out)
            print(file=out)
        authors = md_esc(self.author)
        if len(self.coauthors) > 0:
            if not self.coauthors.startswith(","):
                authors += ","
            authors += f" {md_esc(self.coauthors)}"
        print(f"**Authors:** {authors}", file=out)
        print(file=out)
        affiliations = md_esc(self.affiliations)
        print(f"**Affiliations:** {affiliations}", file=out)
        print(file=out)
        keywords = md_esc(self.keywords)
        print(f"**Keywords:** {keywords}", file=out)
        print(file=out)
        topics = md_esc(self.topics)
        print(f"**Topics:** {topics}", file=out)
        print(file=out)
        text = textwrap.fill(md_esc(self.text))
        print(text, file=out)
        print(file=out)
        print("\n\\newpage\n", file=out)


    def as_html(self, out):
        print(f"<table id='{self.id}'>\n", file=out)

        print("<tr>\n", file=out)
        anchor = f"<a name='{self.id}'>{self.id}</a>"
        print(f"\t<td class='date' rowspan='4'>{anchor}</td>\n", file=out)
        print(f"\t<td class='title'>{html_esc(self.title)}</td>\n", file=out)
        print("</tr>\n", file=out)

        authors = html_esc(self.author)
        if len(self.coauthors) > 0:
            if not self.coauthors.startswith(","):
                authors += ","
            authors += f" {html_esc(self.coauthors)}"
        print("<tr>\n", file=out)
        print(f"\t<td class='speaker'>{authors}</td>\n", file=out)
        print("</tr>\n", file=out)

        print("<tr>\n", file=out)
        print(f"\t<td class='speaker'>{html_esc(self.affiliations)}</td>\n", file=out)
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


def process_talks():

    infile = sys.argv[1]
    abstracts = []
    with open(infile) as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            # print(list(line.keys()))
            id = int(line["Talk Number"])
            abstract = Abstract(
                email=line["Username"],
                author=line["Presenter name"],
                id = f"T{id:02d}",
                coauthors=line["Coauthors"],
                affiliations=line["Affiliations"],
                title=line["Title"],
                text=line["Abstract (max 1500 characters)"],
                keywords=line["Keywords"],
                topics=", ".join(line["Topics (select all that apply)"].split(";")),
            )
            abstract.check_authors()
            abstracts.append(abstract)
    # for abstracts in

    abstracts.sort(key=lambda x: x.id)
    # for ab in abstracts:
    #     print(ab.id)
    # talks = [ab for ab in abstracts if ab.is_talk]
    # posters = [ab for ab in abstracts if not ab.is_talk]
    ids = set()
    # for prefix, the_abstracts in zip("TP", [talks, posters]):
    prefix = "T"
    for j, ab in enumerate(abstracts, 1):
        ab.id = f"{prefix}{j:02d}"
        ids.add(ab.id)

    by_name = collections.defaultdict(list)
    for abstract in abstracts:
        by_name[abstract.author_last_name[0]].append(abstract)

    # for title, the_abstracts in zip(["Talks", "Posters"], [talks, posters]):
    title = "Talks"

    print(f"<h3><a name='{title}'>{title}</a></h3>")
    book = AbstractBook(abstracts)
    book.as_html(sys.stdout)

    # print("<h3><a name='Author_index'>Author index</a></h3>")
    # for letter in sorted(by_name.keys()):
    #     print(f"<h4>{letter.upper()}</h4>")
    #     s = ""
    #     for abstract in by_name[letter]:
    #         s += f"<a href='abstracts/index.html#{abstract.id}'>{abstract.author}</a>, "
    #     s = s[:-2]
    #     print("<p>", s, "</p>")

    # book.as_markdown(sys.stdout)

def process_posters():

    infile = sys.argv[1]
    abstracts = []
    with open(infile) as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            # print(list(line.keys()))
            abstract = Abstract(
                email=line["Username"],
                author=line["Presenter"],
                # id = f"T{id:02d}",
                id=None,
                coauthors=line["Coauthors"],
                affiliations=line["Affiliations"],
                title=line["Title"],
                text=line["Abstract (max 1500 characters)"],
                keywords=line["Keywords"],
                topics=", ".join(line["Topics (select all that apply)"].split(";")),
            )
            abstract.check_authors()
            abstracts.append(abstract)
    # for abstracts in

    abstracts.sort(key=lambda x: x.author_last_name)
    for j, ab in enumerate(abstracts, 1):
        ab.id = f"P{j:02d}"
        # print(f"{ab.id}-{ab.author_last_name}")

    # for title, the_abstracts in zip(["Talks", "Posters"], [talks, posters]):
    title = "Posters"

    print(f"<h3><a name='{title}'>{title}</a></h3>")
    book = AbstractBook(abstracts)
    book.as_html(sys.stdout)

    # print("<h3><a name='Author_index'>Author index</a></h3>")
    # for letter in sorted(by_name.keys()):
    #     print(f"<h4>{letter.upper()}</h4>")
    #     s = ""
    #     for abstract in by_name[letter]:
    #         s += f"<a href='abstracts/index.html#{abstract.id}'>{abstract.author}</a>, "
    #     s = s[:-2]
    #     print("<p>", s, "</p>")

    # book.as_markdown(sys.stdout)


if __name__ == "__main__":
    # main()
    # process_talks()
    process_posters()
