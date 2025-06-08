from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from ..models import Transaction, Category


class BasicViewsTest(TestCase):
    def setUp(self):
        # Przygotowanie testowego klienta i danych testowych
        self.client = Client()
        self.user = User.objects.create_user(username='user1', password='pass')
        self.category = Category.objects.create(name='TestCat', slug='testcat', user=self.user)
        self.transaction = Transaction.objects.create(
            user=self.user,
            amount=100,
            transaction_type='income',
            cat=self.category
        )

    def test_transaction_list_requires_login(self):
        """Sprawdzenie, czy lista transakcji wymaga zalogowania"""
        url = reverse('transaction')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # przekierowanie do logowania

        self.client.login(username='user1', password='pass')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('numbered_transactions', response.context)

    def test_category_view(self):
        """Test widoku kategorii — dostęp po zalogowaniu"""
        url = reverse('category')
        self.client.login(username='user1', password='pass')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('categories', response.context)

    def test_statistic_view(self):
        """Test widoku statystyk — dostęp po zalogowaniu"""
        url = reverse('statistic')
        self.client.login(username='user1', password='pass')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_in', response.context)
        self.assertIn('cat_stat', response.context)
