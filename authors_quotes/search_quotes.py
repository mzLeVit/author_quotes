import json
import redis
from mongoengine import connect, Document, StringField, ReferenceField, ListField
from mongoengine.queryset.visitor import Q

connect(db="your_db_name", host="your_mongodb_atlas_uri")

redis_client = redis.Redis(host='localhost', port=6379, db=0)


class Author(Document):
    fullname = StringField(required=True)


class Quote(Document):
    author = ReferenceField(Author)
    quote = StringField(required=True)
    tags = ListField(StringField())


def load_data():
    with open('authors.json') as f:
        authors_data = json.load(f)
        for author in authors_data:
            Author(fullname=author['fullname']).save()

    with open('quotes.json') as f:
        quotes_data = json.load(f)
        for quote in quotes_data:
            author = Author.objects(fullname=quote['author']).first()
            if author:
                Quote(author=author, quote=quote['quote'], tags=quote['tags']).save()


def search_by_name(name):
    cached_result = redis_client.get(f'name:{name}')
    if cached_result:
        return json.loads(cached_result)

    quotes = Quote.objects(author__fullname__istartswith=name)
    result = [quote.quote for quote in quotes]

    redis_client.set(f'name:{name}', json.dumps(result))
    return result


def search_by_tag(tag):
    cached_result = redis_client.get(f'tag:{tag}')
    if cached_result:
        return json.loads(cached_result)

    quotes = Quote.objects(tags__istartswith=tag)
    result = [quote.quote for quote in quotes]

    redis_client.set(f'tag:{tag}', json.dumps(result))
    return result


def main():
    while True:
        user_input = input("Введіть команду (name: або tag: або tags:): ").strip()

        if user_input == 'exit':
            break

        if user_input.startswith("name:"):
            name_query = user_input.split(":", 1)[1].strip()
            result = search_by_name(name_query)
            if result:
                print("Цитати автора:")
                for r in result:
                    print(f"- {r}")
            else:
                print("Цитати не знайдено.")

        elif user_input.startswith("tag:"):
            tag_query = user_input.split(":", 1)[1].strip()
            result = search_by_tag(tag_query)
            if result:
                print("Цитати з тегом:")
                for r in result:
                    print(f"- {r}")
            else:
                print("Цитати не знайдено.")

        elif user_input.startswith("tags:"):
            tags_query = user_input.split(":", 1)[1].strip().split(',')
            quotes = Quote.objects(Q(tags__in=tags_query))
            if quotes:
                print("Цитати з тегами:")
                for quote in quotes:
                    print(f"- {quote.quote}")
            else:
                print("Цитати не знайдено.")


if __name__ == "__main__":
    main()
