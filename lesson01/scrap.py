from sys import argv
import requests
from bs4 import BeautifulSoup


def get_url_html(url: str):
    """Takes the url and return it's html if possible or None otherwise"""
    try:
        response = requests.get(url, stream=True)
    except:
        return None

    if response.status_code == 200:
        if response.headers.get('content-type', 'none').startswith('text/html'):
            return response.text

    return None


def get_site_x_links(site: str):
    """Takes the url and returns set of links to other sites"""
    html = get_url_html(site)
    if not html:
        return []

    soup = BeautifulSoup(html, 'html.parser')
    return set([a['href'] for a in soup.find_all('a') if a.get('href', '').startswith('http')])


def get_site_x_links_recursive(site: str):
    """Takes the url and returns set of links from the url and the child-urls"""
    links_to_go = get_site_x_links(site)
    result = links_to_go.copy()

    while len(links_to_go) > 0:
        link = links_to_go.pop()

        x_links = get_site_x_links(link)
        for x_link in x_links:
            result.add(x_link)

    return result


recursive_links = get_site_x_links_recursive('https://putty.org')

# assume, that the parameter is a file name
if len(argv) > 1:
    file_name = argv[1]
    f = open(file_name, 'wt')
else:
    f = None

# writing result
for recursive_link in recursive_links:
    print(recursive_link, file=f)

# closing file is necessary
if f:
    f.close()

exit(0)
