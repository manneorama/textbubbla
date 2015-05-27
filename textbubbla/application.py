# -*- coding: utf8 -*-
from flask import Flask, render_template, request, jsonify

from news import top_stories, get_categories_as_columns, get_page

app = Flask(__name__)


DEFAULT_PAGES = {
    100: {
        'func': top_stories,
        'template': 'news_items.html'
    },
    999: {
        'func': get_categories_as_columns,
        'template': 'categories.html'
    }
}


@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return main_page()


@app.route('/navigate', methods=['POST'])
def navigate():
    if 'page' not in request.json:
        return jsonify({'error': 'page key not in request data'})

    if request.json['page'] in DEFAULT_PAGES:
        func = DEFAULT_PAGES[request.json['page']]['func']
        template = DEFAULT_PAGES[request.json['page']]['template']
        return render_template(template, **func())
    else:
        item = get_page(request.json['page'])
        return render_template('single_item.html', item=item)


def main_page():
    return render_template(
        'news.html',
        **top_stories()
    )


if __name__ == '__main__':
    app.run(debug=True)
