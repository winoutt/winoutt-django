from django.http import JsonResponse
from urllib.parse import urljoin, urlparse
from django.utils.translation import ugettext_lazy as _
import requests
import bs4
import re

def get_url(content):
    regex = r"https?\:\/\/[^\" ]+"
    url = re.findall(regex, content)
    return url[0] if len(url)>0 else None

def get_metadata(url):
    """This function looks for the page of a given URL, extracts the page content and parses the content
    with bs4. searching for the page meta tags giving priority to the Open Graph Protocol
    https://ogp.me/, then it returns the metadata in case there is any, or tries to build one.
    :requires:
    :param url: Any valid URL to search for.
    :returns:
    A dictionary with metadata from a given webpage.
    """
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = f"http://{parsed_url.path}"

    try:
        response = requests.get(url, timeout=0.9)
        response.raise_for_status()

    except requests.exceptions.ConnectionError:
        return JsonResponse(
            {"message": _(f"We detected the url {url} but it appears to be invalid.")}
        )

    except requests.exceptions.Timeout as e:
        return JsonResponse(
            _(
                f"We found an error trying to connect to the site {url}, please find more info here:{e}"
            )
        )

    soup = bs4.BeautifulSoup(response.content)
    ogs = soup.html.head.find_all(property=re.compile(r"^og"))
    data = {og.get("property")[3:]: og.get("content") for og in ogs}
    if not data.get("url"):
        data["url"] = url

    if not data.get("title"):
        data["title"] = soup.html.title.text

    if not data.get("image"):
        images = soup.find_all("img")
        if len(images) > 0:
            data["image"] = urljoin(url, images[0].get("src"))

    if not data.get("description"):
        data["description"] = ""
        for text in soup.body.find_all(string=True):
            if (
                text.parent.name != "script"
                and text.parent.name != "style"
                and not isinstance(text, bs4.Comment)
            ):
                data["description"] += text

    data["description"] = re.sub("\n|\r|\t", " ", data["description"])
    data["description"] = re.sub(" +", " ", data["description"])
    data["description"] = data["description"].strip()[:255]

    return data