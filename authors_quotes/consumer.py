import pika
from models import Contact


def send_email(contact):
    print(f"Відправка електронної пошти для {contact.full_name} на {contact.email}")

    contact.email_sent = True
    contact.save()


def callback(ch, method, properties, body):
    contact_id = body.decode()
    contact = Contact.objects(id=contact_id).first()
    if contact and not contact.email_sent:
        send_email(contact)
        print(f"Електронну пошту відправлено для {contact.full_name}")


def start_consuming():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='email_queue')
    channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

    print('Очікування повідомлень. Для виходу натисніть CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    start_consuming()
