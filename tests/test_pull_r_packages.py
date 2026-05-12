from pathlib import Path
from types import SimpleNamespace
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import pull_R_packages


class FakeAnchor:
    def __init__(self, name, href):
        self._name = name
        self._node = SimpleNamespace(attrib={"href": href})

    def html(self):
        return self._name

    def __getitem__(self, index):
        if index != 0:
            raise IndexError(index)
        return self._node


class FakeListItem:
    def __init__(self, name, href):
        self._anchor = FakeAnchor(name, href)

    def __call__(self, selector):
        assert selector == "a"
        return self._anchor


class FakeHeading:
    def __init__(self, text):
        self._text = text

    def html(self):
        return self._text


class FakeDocument:
    def __init__(self, items=None, heading=None):
        self._items = items or []
        self._heading = heading

    def __call__(self, selector):
        if selector == "li":
            return self
        if selector == "h2":
            return FakeHeading(self._heading)
        raise AssertionError(selector)

    def items(self):
        return iter(self._items)


def test_normalize_package_link_expands_cran_relative_path():
    assert pull_R_packages.normalize_package_link(
        "../packages/pkg/index.html"
    ) == "http://cran.r-project.org/web/packages/pkg/index.html"


def test_normalize_package_link_keeps_absolute_url():
    assert pull_R_packages.normalize_package_link(
        "https://example.com/pkg"
    ) == "https://example.com/pkg"


def test_format_package_row_uses_existing_markdown_layout():
    row = pull_R_packages.format_package_row(
        "caret", "https://cran.example/caret", "Classification tools"
    )

    assert row == " [caret](https://cran.example/caret) - Classification tools \n"


def test_scrape_packages_fetches_only_relative_package_links():
    fetched_urls = []

    def fake_pyquery(url, opener):
        fetched_urls.append(url)
        if url.endswith("MachineLearning.html"):
            return FakeDocument([
                FakeListItem("caret", "../packages/caret/index.html"),
                FakeListItem("external", "https://example.com/external"),
            ])
        return FakeDocument(heading="Caret package")

    packages = list(pull_R_packages.scrape_packages(
        pyquery_factory=fake_pyquery,
        opener=lambda url, **kw: b"",
    ))

    assert packages == [(
        "caret",
        "http://cran.r-project.org/web/packages/caret/index.html",
        "Caret package",
    )]
    assert fetched_urls == [
        pull_R_packages.CRAN_MACHINE_LEARNING_URL,
        "http://cran.r-project.org/web/packages/caret/index.html",
    ]


def test_write_packages_writes_formatted_rows(tmp_path):
    output_path = tmp_path / "Packages.txt"

    def fake_pyquery(url, opener):
        if url.endswith("MachineLearning.html"):
            return FakeDocument([
                FakeListItem("mlr", "../packages/mlr/index.html"),
            ])
        return FakeDocument(heading="Machine learning in R")

    pull_R_packages.write_packages(
        output_path=str(output_path),
        pyquery_factory=fake_pyquery,
        opener=lambda url, **kw: b"",
    )

    assert output_path.read_text(encoding="utf-8") == (
        " [mlr](http://cran.r-project.org/web/packages/mlr/index.html) - "
        "Machine learning in R \n"
    )
