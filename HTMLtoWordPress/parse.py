#!/usr/bin/env python

import json
import os
import re
from datetime import datetime

from bs4 import BeautifulSoup, NavigableString, Tag

directory = r'html'
try:
    os.remove("out/articles.json")
except FileNotFoundError:
    print("File not found")

try:
    os.remove("out/images.csv")
except FileNotFoundError:
    print("File not found")

article_titles = []
articles = []
categories = {
    "Free UK Genealogy": 23,
    "FreeBMD": 27,
    "FreeCEN": 28,
    "FreeREG": 26,
    "Genealogy": 24,
    "Guest Post": 25,
    "Irish Genealogy": 30,
    "Open Data": 29
}
site_links = {
    "http://www.freeukgenealogy.org.uk": "/",
    "https://www.freeukgenealogy.org.uk": "/",
    "https://www.freeukgenealogy.org.uk/files/Documents/Privacy-Notice.pdf": "/privacy-notice-2",
    "http://www.freeukgenealogy.org.uk/files/Documents/Privacy-Notice.pdf": "/privacy-notice-2",
    "https://www.freeukgenealogy.org.uk/files/Misc-images/Blog-post-images/34-FH-Qs.pdf": "34-fh-qs",
    "https://www.freeukgenealogy.org.uk/about/donate/": "/donate",
    "http://www.freeukgenealogy.org.uk/about/donate/": "/donate"
}
article_count = 0


def extract_categories():
    article_categories = []
    for anc in article.find_all('a'):
        try:
            if anc['href'].startswith("https://www.freeukgenealogy.org.uk/news/category/"):
                if anc.get_text() in categories:
                    article_categories.append(categories[anc.get_text()])
            elif anc['href'] in site_links:
                anc['href'] = site_links[anc['href']]
        except Exception:
            pass
    if not article_categories:
        article_categories.append(1)
    article_out["categories"] = article_categories


def update_image_links():
    for img in article.find_all('img'):
        image = {}
        try:
            if img['src'].startswith("/files"):
                image['url'] = "https://www.freeukgenealogy.org.uk{}".format(img['src'])
            elif img['src'].startswith("https://www.freeukgenealogy.org.uk"):
                image['url'] = img['src']
        except Exception:
            pass

        try:
            image['filename'] = image['url'].split('/')[-1]
            img['src'] = "/wp-content/uploads/2020/12/" + image['filename']
        except KeyError:
            pass


def replace_content_special_characters():
    article_out["content"] = content.replace("\n", "").replace("'", "&apos;").replace(" ",
                                                                                      "&nbsp;").replace(
        '\"', "'")


def extract_content():
    global content
    for section in article.find_all('section'):
        for child in section.children:
            if isinstance(child, NavigableString):
                content = content + child
            elif isinstance(child, Tag):
                content = content + child.prettify(formatter="html")
            else:
                pass

        content = content + "<br/>"


def extract_footer():
    global footer
    if article.footer:
        footer = article.footer.get_text()
        author = footer.partition("Posted on ")[0][3:].strip()
        if author == "Denise Colbert":
            article_out["author"] = 11
        else:
            article_out["author"] = 7

        posted = re.sub(r'(\d)(st|nd|rd|th)', r'\1',
                        footer.partition("Posted on ")[2].partition("Comments")[0]).strip()
        posted = str(posted)
        try:
            posted_date = datetime.strptime(posted, "%d %B %Y")
        except ValueError:
            print("Unable to parse date {}, using default".format(posted))
            posted = '26 November 2020'

        posted_gmt = datetime.strftime(posted_date, '%Y-%m-%dT%H:%M:%S')
        article_out["date_gmt"] = posted_gmt
    else:
        article_out["author"] = 11
        article_out["date_gmt"] = '2018-04-01T00:00:00'


def update_source_links():
    for source in article.find_all('source'):
        src = {}
        try:
            if source['src'].startswith("https://www.freeukgenealogy.org.uk"):
                src['url'] = source['src']
        except Exception:
            pass

        try:
            src['filename'] = src['url'].split('/')[-1]
            source['src'] = "/wp-content/uploads/2020/12/" + src['filename']
        except KeyError:
            pass


for entry in os.scandir(directory):
    if (entry.path.endswith(".html")) and entry.is_file():
        with open(entry, 'r') as f:
            contents = f.read()

            soup = BeautifulSoup(contents, 'lxml')

            root = soup.body

            for article in soup.find_all('article'):
                metas = article.findAll('meta')
                for meta in metas:
                    meta.extract()
                styles = article.findAll('style')
                for style in styles:
                    style.extract()
                title = article.header.h1.get_text()

                if title in article_titles:
                    pass
                else:
                    print("Publishing article title: {} from file {}".format(title, entry.path))
                    article_titles.append(title)

                    article_out = {}
                    content = ""
                    article_out["title"] = title.replace('\"', "&quot;")

                    extract_categories()
                    update_image_links()
                    update_source_links()
                    extract_footer()
                    extract_content()
                    replace_content_special_characters()
                    articles.append(article_out)
                    article_count += 1


def articles_out():
    out = open("out/articles.json", "x")
    out.write(json.dumps(articles, indent=4))
    out.close()


articles_out()
print("{} articles published".format(article_count))
