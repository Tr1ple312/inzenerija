from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from ..models import Transaction, Category


class CategoryModelTest(TestCase):
    def setUp(self):
        # Tworzenie użytkownika do testów
        self.user = User.objects.create_user(username='user1', password='pass')

    def test_slug_creation_and_unique_slug(self):
        """Testowanie tworzenia slug i unikalności slugów"""
        cat1 = Category.objects.create(name='Food', slug='food', user=self.user)
        cat1.save()
        cat2 = Category(name='Food', slug='food-1', user=self.user)
        # Sprawdzamy, czy walidacja podnosi błąd, jeśli slug jest nieunikalny dla użytkownika
        with self.assertRaises(ValidationError):
            cat2.full_clean()

    def test_unique_category_per_user_constraint(self):
        """Sprawdzanie unikalności nazwy kategorii dla danego użytkownika"""
        Category.objects.create(name='Books', slug='books', user=self.user)
        cat = Category(name='Books', slug='books-2', user=self.user)
        with self.assertRaises(ValidationError):
            cat.full_clean()

    def test_base_category_name_conflict(self):
        """Testowanie konfliktu nazwy kategorii bazowej"""
        # Tworzymy kategorię bazową bez przypisanego użytkownika
        Category.objects.create(name='Other', slug='other', user=None, is_base=True)
        cat = Category(name='Other', slug='other-1', user=self.user)
        with self.assertRaises(ValidationError):
            cat.full_clean()


class TransactionModelTest(TestCase):
    def setUp(self):
        # Tworzenie użytkownika i kategorii do testów transakcji
        self.user = User.objects.create_user(username='user1', password='pass')
        self.category = Category.objects.create(name='Salary', slug='salary', user=self.user)

    def test_create_transaction(self):
        """Testowanie tworzenia transakcji i jej reprezentacji tekstowej"""
        trans = Transaction.objects.create(
            user=self.user,
            amount=200,
            transaction_type='income',
            cat=self.category
        )
        self.assertEqual(str(trans), f"Transaction {trans.transaction_id} - 200 income")

    def test_negative_amount_validation(self):
        """Testowanie walidacji negatywnej wartości amount"""
        trans = Transaction(
            user=self.user,
            amount=-50,
            transaction_type='expense',
            cat=self.category
        )
        with self.assertRaises(ValidationError):
            trans.full_clean()
