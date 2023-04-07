"""
simple file to get few images from google for testing image annotation process
@https://stackoverflow.com/questions/51676983/python-error-downloading-image-from-web-http-error-400-bad-request
"""

import urllib.request as ulib
import os
from bs4 import BeautifulSoup as Soup
import json

url_a = 'https://www.google.com/search?ei=1m7NWePfFYaGmQG51q7IBg&hl=en&q={}'
url_b = '\&tbm=isch&ved=0ahUKEwjjovnD7sjWAhUGQyYKHTmrC2kQuT0I7gEoAQ&start={}'
url_c = '\&yv=2&vet=10ahUKEwjjovnD7sjWAhUGQyYKHTmrC2kQuT0I7gEoAQ.1m7NWePfFYaGmQG51q7IBg'
# url_d = '\.i&ijn=1&asearch=ichunk&async=_id:rg_s,_pms:s'
url_d = '\.i&ijn=1'
# url_d = ''
url_base = ''.join((url_a, url_b, url_c, url_d))

headers = {'User-Agent': 'Mozilla/60.0 Chrome/63.0.3239.108'}

def get_links(search_name):
    search_name = search_name.replace(' ', '+')
    url = url_base.format(search_name, 0)
    request = ulib.Request(url, None, headers)
    # pdb.set_trace()
    json_string = ulib.urlopen(request).read()
    # page = json.loads(json_string)
    # page = json.loads(json_string.decode("utf-8"))
    # pdb.set_trace()
    # new_soup = Soup(page[1][1], 'lxml')
    new_soup = Soup(json_string, 'lxml')
    images = new_soup.find_all('img')
    links = [image['src'] for image in images]
    return links

def save_images(links, search_name):
    directory = search_name.replace(' ', '_')
    directory = 'images'
    if not os.path.isdir(directory):
        os.mkdir(directory)

    for i, link in enumerate(links):
        savepath = os.path.join(directory, '{:06}.png'.format(i))
        ulib.urlretrieve(link, savepath)

if __name__ == '__main__':
    search_name = 'fidget spinner'
    links = get_links(search_name)
    save_images(links, search_name)