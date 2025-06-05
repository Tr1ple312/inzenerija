from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    transaction_date = models.DateTimeField(auto_now_add=True,  db_index=True)

    cat =  models.ForeignKey('Category', on_delete=models.PROTECT, related_name='transactions')

    class Meta:
        ordering = ['-transaction_date']
        indexes = [
            models.Index(fields=['-transaction_date'])
        ]

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.amount} {self.transaction_type}"


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # <- вот здесь добавь null=True, blank=True
    name = models.CharField(max_length=20, unique=True, db_index=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    slug  =  models.SlugField(max_length=20, unique=True,  db_index=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['-pk']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name