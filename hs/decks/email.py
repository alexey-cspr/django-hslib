from django.core.mail import send_mail
from multiprocessing import Process, Manager
import static_vars


from lab3.settings import EMAIL_HOST


def process_sent_queue(queue):
    while True:
        if not queue.empty():
            address, subject, message = queue.get()
            send_mail(subject, message, EMAIL_HOST, [address], False)


@static_vars.static_vars(IS_ACTIVE=False)
def send_email(address, subject, message):
    if not send_email.IS_ACTIVE:
        send_email.queue = Manager().Queue()
        p = Process(target=process_sent_queue, args=(send_email.queue,))
        p.daemon = True
        p.start()
        send_email.IS_ACTIVE = True

    send_email.queue.put((address, subject, message))

