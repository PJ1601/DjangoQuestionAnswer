"""
Question 1: By default are django signals executed synchronously or asynchronously? 
Please support your answer with a code snippet that conclusively proves your stance. 
The code does not need to be elegant and production ready, we just need to understand your logic.

Answer: Yes, Django signals are executed synchronously by default.
"""
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import time

class NewModel(models.Model):
  name = models.CharField(max_length=10)

@receiver(post_save, sender=NewModel)
def signal_handler(sender, instance, create, **kwargs):
    print("Signal handler started")
    time.sleep(5)  # Simulate a slow operation
    print("Signal handler finished")

print("Before")
NewModel.objects.create(name="Test")
print("After")


"""
Question 2: Do django signals run in the same thread as the caller? 
Please support your answer with a code snippet that conclusively proves your stance. 
The code does not need to be elegant and production ready, we just need to understand your logic.

Answer: Yes, by default django signals run in the same thread as the caller.
"""

import threading
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class NewModel(models.Model):
  name = models.CharField(max_length=10)

@receiver(post_save, sender=NewModel)
def thread_handler(sender, instance, create, **kwargs):
  print(f"Signal handler thread is {threading.current_thread().name}")

print(f"View thread: {threading.current_thread().name}")
NewModel.objects.create(name="Test")

"""
Question 3: By default do django signals run in the same database transaction as the caller? 
Please support your answer with a code snippet that conclusively proves your stance. 
The code does not need to be elegant and production ready, we just need to understand your logic.

Answer: Yes, by default Django signals run in the same database transaction as the caller.
"""

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class NewModel(models.Model):
  name = models.CharField(max_length=20)
  signal_ran = models.BooleanField(default=False)

@receiver(post_save, sender=NewModel)
def handler(sender, instance, create, **kwargs):
  instance.signal_ran = True
  instance.save()
  raise Exception("Rollback")

try:
  with transaction.atomic():
    NewModel.objects.create(name="Jhonny Test")
except Exception as e:
  print(f"Transaction rolled back {e}")

print(NewModel.objects.get(name="Jhonny Test").signal_ran)
  
