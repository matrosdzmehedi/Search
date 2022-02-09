from django.db import models

import random


class Search(models.Model):
    """
    Model for the search table.
    """
    search_keyword = models.TextField()
    username = models.CharField(max_length=100)   # did n't use defauls User Model as foreign key. For Authentication purposes.
    search_result = models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.search_result = default=''.join((random.choice('abcdefghijklmnopqrstuvwxyz')) for x in range(20))
        super(Search, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.search_keyword)