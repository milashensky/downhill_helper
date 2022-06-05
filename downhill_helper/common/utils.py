import os
import hmac
import random


def upload_to(instance, filename):
    _, ext = filename.rsplit('.', 1)
    key, msg = str(random.randint(1, 100000)), str(instance.pk)
    filename = u'{0:s}.{1:s}'.format(hmac.new(key.encode(), msg.encode()).hexdigest(), ext)
    return os.path.join(instance._meta.app_label, instance._meta.model_name, filename)
