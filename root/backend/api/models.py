from django.db import models

class MatchRecord(models.Model):
    resume_url =  models.URLField()
    resume_summary = models.TextField()
    job_id_list = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"MatchRecord {self.id}"