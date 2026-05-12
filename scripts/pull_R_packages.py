#!/usr/bin/python

"""
    This script will scrape the r-project.org machine learning selection and
    format the packages in github markdown style for this
    awesome-machine-learning repo.
"""

import codecs
try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

CRAN_MACHINE_LEARNING_URL = (
    'http://cran.r-project.org/web/views/MachineLearning.html'
)
CRAN_WEB_BASE_URL = 'http://cran.r-project.org/web'


def read_url(url, **kw):
    return urlopen(url).read()


def load_pyquery():
    from pyquery import PyQuery as pq
    return pq


def normalize_package_link(package_link, base_url=CRAN_WEB_BASE_URL):
    if '..' in package_link:
        return package_link.replace('..', base_url)
    return package_link


def format_package_row(package_name, package_link, package_description):
    return " [%s](%s) - %s \n" % (package_name, package_link,
                                  package_description)


def scrape_packages(source_url=CRAN_MACHINE_LEARNING_URL, opener=read_url,
                    pyquery_factory=None):
    pq = pyquery_factory or load_pyquery()
    d = pq(url=source_url, opener=lambda url, **kw: opener(url, **kw))

    for e in d("li").items():
        package_name = e("a").html()
        package_link = e("a")[0].attrib['href']
        normalized_link = normalize_package_link(package_link)
        if normalized_link != package_link:
            dd = pq(url=normalized_link,
                    opener=lambda url, **kw: opener(url, **kw))
            package_description = dd("h2").html()
            yield package_name, normalized_link, package_description


def write_packages(output_path="Packages.txt",
                   source_url=CRAN_MACHINE_LEARNING_URL, opener=read_url,
                   pyquery_factory=None):
    with codecs.open(output_path, encoding='utf-8', mode="w") as text_file:
        for package_name, package_link, package_description in scrape_packages(
                source_url=source_url, opener=opener,
                pyquery_factory=pyquery_factory):
            text_file.write(format_package_row(package_name, package_link,
                                               package_description))


if __name__ == "__main__":
    write_packages()
