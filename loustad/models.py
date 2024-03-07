from django.db import models


class VDemo(models.Model):
    doc = models.ForeignKey("Document", on_delete=models.CASCADE,null=True, default=None, verbose_name="Document")
    query = models.CharField(max_length=500)
    response = models.TextField(max_length=10000, verbose_name="Réponse", blank=True)


    def __str__(self):
        return self.query
    


class Document(models.Model):
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=100, default="")
    corpus_id = models.PositiveIntegerField(default=0)
    api_key = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.name

