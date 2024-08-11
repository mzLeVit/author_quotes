from mongoengine import Document, StringField, ReferenceField, ListField, connect
from mongoengine import Document, StringField, BooleanField, connect


connect(db="<dbname>", host="mongodb+srv://mezeoq:pTjnrWHQcraXzaIJ@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority")

class Contact(Document):
    name = StringField(required=True)
    email = StringField(required=True)
    phone_number = StringField(required=True)
    preferred_contact_method = StringField(choices=['email', 'sms'], required=True)
    email_sent = BooleanField(default=False)


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, required=True)
    quote = StringField(required=True)
