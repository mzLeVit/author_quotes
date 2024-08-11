import pika
from models import Contact


def callback(ch, method, properties, body):
    contact_id = body.decode()
    contact = Contact.objects(id=contact_id).first()
    if contact:
        print(f"Відправка SMS до {contact.name} ({contact.phone_number})")


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='sms_queue')
channel.basic_consume(queue='sms_queue', on_message_callback=callback, auto_ack=True)

print('Очікування повідомлень. Для виходу натисніть CTRL+C')
channel.start_consuming()
