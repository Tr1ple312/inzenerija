# Generated by Django 5.2.1 on 2025-05-12 15:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=20, unique=True)),
                (
                    "description",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("slug", models.SlugField(max_length=20, unique=True)),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                ("transaction_id", models.AutoField(primary_key=True, serialize=False)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "transaction_type",
                    models.CharField(
                        choices=[("income", "Income"), ("expense", "Expense")],
                        max_length=10,
                    ),
                ),
                (
                    "transaction_date",
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "cat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="category",
                        to="testsite.category",
                    ),
                ),
            ],
            options={
                "ordering": ["-transaction_date"],
                "indexes": [
                    models.Index(
                        fields=["-transaction_date"],
                        name="testsite_tr_transac_8b9d32_idx",
                    )
                ],
            },
        ),
    ]
