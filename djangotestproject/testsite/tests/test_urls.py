from urllib.parse import quote
from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.conf import settings

from ..models import Category, Transaction
from ..views import (
    transaction_list, about, exchange_rates, category, statistic_view,
    TransAdd, TransUpdate, TransDelete,
    CategoryAdd, CategoryUpdate, CategoryDelete
)


class URLTests(TestCase):
    def setUp(self):
        # Tworzenie użytkownika i powiązanych obiektów testowych
        self.user = User.objects.create_user(username='user1', password='pass')
        self.category = Category.objects.create(name='TestCat', slug='testcat', user=self.user)
        self.transaction = Transaction.objects.create(
            user=self.user,
            amount=100,
            transaction_type='income',
            cat=self.category,
            transaction_date='2025-01-01'
        )

    def test_public_urls_accessible(self):
        """Testowanie dostępności stron publicznych bez logowania"""
        public_urls = [
            ('about', 200),
            ('exchange', 200),
        ]
        for name, expected_status in public_urls:
            url = reverse(name)
            response = self.client.get(url)
            self.assertEqual(response.status_code, expected_status, f"{name} powinien zwracać status {expected_status}")

    def test_login_required_urls_redirect(self):
        """Sprawdzanie przekierowań dla stron wymagających logowania"""
        private_urls = [
            ('transaction', {}),
            ('category', {}),
            ('statistic', {}),
            ('transaction-add', {}),
            ('transaction-update', {'pk': self.transaction.pk}),
            ('transaction-delete', {'pk': self.transaction.pk}),
            ('category-add', {}),
            ('category_update', {'pk': self.category.pk}),
            ('category_delete', {'pk': self.category.pk}),
        ]
        login_url = reverse(settings.LOGIN_URL)

        for name, kwargs in private_urls:
            url = reverse(name, kwargs=kwargs)
            response = self.client.get(url)
            expected_redirect = f'{login_url}?next={quote(url)}'
            self.assertRedirects(response, expected_redirect, msg_prefix=f"{name} powinien przekierować")

    def test_authenticated_user_access(self):
        """Testowanie dostępu do stron po zalogowaniu"""
        self.client.login(username='user1', password='pass')
        private_urls = [
            ('transaction', {}),
            ('category', {}),
            ('statistic', {}),
            ('transaction-add', {}),
            ('transaction-update', {'pk': self.transaction.pk}),
            ('transaction-delete', {'pk': self.transaction.pk}),
            ('category-add', {}),
            ('category_update', {'pk': self.category.pk}),
            ('category_delete', {'pk': self.category.pk}),
        ]
        for name, kwargs in private_urls:
            url = reverse(name, kwargs=kwargs)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"{name} powinien być dostępny po zalogowaniu")

    def test_url_resolves_to_correct_view(self):
        """Sprawdzanie, czy URL-e kierują do poprawnych widoków"""
        url_view_map = {
            'transaction': transaction_list,
            'about': about,
            'exchange': exchange_rates,
            'category': category,
            'statistic': statistic_view,
            'transaction-add': TransAdd,
            'transaction-update': TransUpdate,
            'transaction-delete': TransDelete,
            'category-add': CategoryAdd,
            'category_update': CategoryUpdate,
            'category_delete': CategoryDelete,
        }

        for name, view in url_view_map.items():
            kwargs = {}
            if ('transaction-update' in name or 'transaction-delete' in name):
                kwargs['pk'] = self.transaction.pk
            elif ('category_update' in name or 'category_delete' in name):
                kwargs['pk'] = self.category.pk

            url = reverse(name, kwargs=kwargs if kwargs else None)
            resolved = resolve(url)
            resolved_func = resolved.func.view_class if hasattr(resolved.func, 'view_class') else resolved.func
            self.assertEqual(resolved_func, view, f"{name} powinien kierować do widoku {view}")
