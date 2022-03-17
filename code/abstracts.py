"""
Process abstracts to create book.
"""
import csv
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
    affiliations: str
    title: str
    text: str
    is_talk: bool
    keywords: str
    topics: str

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
        print(f"<h1> {html_esc(self.title)}</h1>", file=out)
        print("<p>", file=out)
        authors = html_esc(self.author)
        if len(self.coauthors) > 0:
            if not self.coauthors.startswith(","):
                authors += ","
            authors += f" {html_esc(self.coauthors)}"
        print(f"**Authors:** {authors}", file=out)
        print(file=out)
        affiliations = html_esc(self.affiliations)
        print(f"**Affiliations:** {affiliations}", file=out)
        print(file=out)
        keywords = html_esc(self.keywords)
        print(f"**Keywords:** {keywords}", file=out)
        print(file=out)
        topics = html_esc(self.topics)
        print(f"**Topics:** {topics}", file=out)
        print(file=out)
        text = textwrap.fill(html_esc(self.text))
        print(text, file=out)
        print(file=out)
        print("\n</p>\n", file=out)

class AbstractBook:
    def __init__(self, abstracts):
        self.abstracts = abstracts

    def as_markdown(self, out):
        for id, abstract in enumerate(self.abstracts):
            abstract.as_markdown(out, id)

    def as_html(self, out):
        for abstract in self.abstracts:
            abstract.as_html(out)


def main():

    infile = sys.argv[1]
    abstracts = []
    with open(infile) as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            # print(list(line.keys()))
            abstract = Abstract(
                email=line["Username"],
                author=line["Presenter"],
                coauthors=line["Coauthors"],
                affiliations=line["Affiliations"],
                title=line["Title"],
                text=line["Abstract (max 1500 characters)"],
                is_talk=line["Talk or Poster?"] == "Talk",
                keywords=line["Keywords"],
                topics=", ".join(line["Topics (select all that apply)"].split(";")),
            )
            abstract.check_authors()
            abstracts.append(abstract)

    abstracts.sort(key=lambda x: x.author)
    # random.seed(42)
    # talks[8] = None
    # talks[37] = None
    # random.shuffle(talks)
    # print(len(talks))
    book = AbstractBook(abstracts)
    book.as_html(sys.stdout)
    # book.as_markdown(sys.stdout)
    # for talk in talks:
    #     # print(talk)
    #     if talk is not None:
    #         print(talk.author)
    # for abstract in book.abstracts:
    #     print(abstract.keywords)

if __name__ == "__main__":
    main()
