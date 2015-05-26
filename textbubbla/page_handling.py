import operator

CATSTART, CATEND = 101, 998


def _accumulate(iterable, func=operator.add):
    'Return running totals'
    # accumulate([1,2,3,4,5]) --> 1 3 6 10 15
    # accumulate([1,2,3,4,5], operator.mul) --> 1 2 6 24 120
    it = iter(iterable)
    try:
        total = next(it)
    except StopIteration:
        return
    yield total
    for element in it:
        total = func(total, element)
        yield total


def calculate_category_start(num_categories):
    page_range = CATEND - CATSTART
    pages_per_category = page_range / num_categories
    category_pages = [CATSTART] + [pages_per_category] * (num_categories - 1)
    return list(_accumulate(category_pages))


def calculate_category_name_and_link_number(categories, page_number):
    category_starts = calculate_category_start(len(categories))
    category_start = next(value for value in reversed(category_starts)
                          if value <= page_number)
    print category_start
    category_index = category_starts.index(category_start)
    return (categories[category_index],
            page_number - category_starts[category_index])
