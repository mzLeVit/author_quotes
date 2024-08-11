import json
from models import Author, Quote

# Завантаження авторів
def load_authors():
    with open('authors.json', 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        for author in authors_data:
            new_author = Author(
                fullname=author['fullname'],
                born_date=author.get('born_date', ''),
                born_location=author.get('born_location', ''),
                description=author.get('description', '')
            )
            new_author.save()

# Завантаження цитат
def load_quotes():
    with open('quotes.json', 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote in quotes_data:
            author_name = quote['author']
            author = Author.objects(fullname=author_name).first()
            if author:
                new_quote = Quote(
                    tags=quote['tags'],
                    author=author,
                    quote=quote['quote']
                )
                new_quote.save()

if __name__ == '__main__':
    load_authors()
    load_quotes()
