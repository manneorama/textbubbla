# -*- coding: utf8 -*-
import requests
import xml.etree.ElementTree as et

import cache
from page_handling import calculate_category_name_and_link_number, calculate_category_start


BASE_URL = 'http://bubb.la/rss/{}'
CATEGORIES_URL = 'http://bubb.la/rss_feeds.json'


def get_categories():
    cats = requests.get(CATEGORIES_URL).json()
    names = [name for name in cats.iterkeys()]
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
    items = get_itemized_news(
        category_name)
    try:
        return items[item_index]
    except IndexError:
        return {
            'title': 'Denna sida har ingen publicering',
            'url': '#',
            'date': 'aldrig',
            'category': category_name,
        }


def get_itemized_news(category):
    if not itemize_news_for_category(category):
        return None
    items = cache.get(category)
    return items


def itemize_news():
    for category in get_categories():
        itemize_news_for_category(category)


def itemize_news_for_category(category):
    if not cache.must_repopulate(category):
        return True
    url = BASE_URL.format(category).replace('Senaste', 'Nyheter')
    return cache.populate_from_url(category, url, itemize)


def itemize(request_content):
    root = et.fromstring(request_content)

    items = []
    for item in root.iter('item'):
        items.append({
            'title': item.find('title').text,
            'url': item.find('link').text,
            'category': item.find('category').text,
            'date': item.find('pubDate').text
        })
    return items


def get_simple_news(limit=None):
    if itemize_news_for_category('Nyheter'):
        items = cache.get('Nyheter')
        return items if limit is None else items[:limit]


def top_stories():
    top_stories = {
        'item{}'.format(index + 1): story
        for index, story in enumerate(get_simple_news(limit=4))
    }
    return top_stories
