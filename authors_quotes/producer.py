import pika
from faker import Faker
from models import Contact


def send_to_queue(contact_id, queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=str(contact_id))
    connection.close()


fake = Faker()

for _ in range(10):  
    contact = Contact(
        name=fake.name(),
        email=fake.email(),
        phone_number=fake.phone_number(),
        preferred_contact_method=fake.random_element(elements=('email', 'sms'))
    )
    contact.save()

    queue_name = 'email_queue' if contact.preferred_contact_method == 'email' else 'sms_queue'
    send_to_queue(contact.id, queue_name)



def generate_contacts(count=10):
    fake = Faker()
    contacts = []
    for _ in range(count):
        contact = Contact(
            full_name=fake.name(),
            email=fake.email()
        )
        contact.save()
        contacts.append(contact.id)
    return contacts

if __name__ == "__main__":
    contact_ids = generate_contacts(10)
    for contact_id in contact_ids:
        send_to_queue(contact_id)
        print(f"Відправлено контакт {contact_id} у чергу")
