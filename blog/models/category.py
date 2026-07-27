from django.db import models


# =========================================================
# CATEGORY — a simple table (one category has many posts)
# =========================================================
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
