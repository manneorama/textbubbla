import requests
import xml.etree.ElementTree as et

from page_handling import calculate_category_name_and_link_number, calculate_category_start

BASE_URL = 'http://bubb.la/rss/{}'
CATEGORIES_URL = 'http://bubb.la/rss_feeds.json'


def get_categories():
    cats = requests.get(CATEGORIES_URL).json()
    names = [name for name in cats.iterkeys()]
    print names
    return names


def get_categories_as_columns():
    names = get_categories()
    starts = calculate_category_start(len(names))
    names_and_pages = zip(names, starts)
    col1, col2 = (names_and_pages[:len(names_and_pages) / 2],
                  names_and_pages[len(names_and_pages) / 2:])
    return {
        'left_col': [{'name': name, 'page': page} for name, page in col1],
        'right_col': [{'name': name, 'page': page} for name, page in col2],
    }


def get_page(page_number):
    names = get_categories()
    category_name, item_index = calculate_category_name_and_link_number(
        names, page_number)
    return get_itemized_news(
        BASE_URL.format(category_name),
        limit=item_index)[-1]


def get_itemized_news(url, limit=None):
    content = requests.get(url.replace('Senaste', 'Nyheter')).content
    root = et.fromstring(content)

    items = []
    for item in root.iter('item'):
        items.append({
            'title': item.find('title').text,
            'url': item.find('link').text,
            'category': item.find('category').text,
            'date': item.find('pubDate').text
        })
    return items if limit is None else items[:limit + 1]


def get_simple_news(url, limit=None):
    print url
    content = requests.get(url.replace('Senaste', 'Nyheter')).content
    root = et.fromstring(content)

    items = []
    for item in root.iter('item'):
        items.append({
            'title': item.find('title').text,
            'category': item.find('category').text,
            'url': item.find('link').text
        })
    return items if limit is None else items[:limit]


def top_stories():
    top_stories = {
        'item{}'.format(index + 1): story
        for index, story in enumerate(get_simple_news(BASE_URL.format('nyheter'), limit=4))
    }
    return top_stories
