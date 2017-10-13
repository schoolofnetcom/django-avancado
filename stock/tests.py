from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.test.testcases import SimpleTestCase
from django.urls.base import reverse

from stock.models import Product, TimestampableMixin, StockEntry


class ProductTest(SimpleTestCase):
    def test_value_initial_stock_field(self):
        product = Product()
        self.assertEquals(0, product.stock)
        # self.assertEquals(1, product.stock)

    def test_product_has_timestampable(self):
        product = Product()
        self.assertIsInstance(product, TimestampableMixin)

    def test_exception_when_stock_less_zero(self):
        product = Product()
        with self.assertRaises(ValueError) as exception:
            product.stock = 10
            product.decrement(11)
        self.assertEquals('Sem estoque disponível', str(exception.exception))


class ProductDatabaseTest(TestCase):
    fixtures = ['data.json']

    def setUp(self):
        self.product = Product.objects.create(
            name="Produto YY", stock_max=200, price_sale=50.50, price_purchase=25.25,
        )

    def test_product_save(self):
        self.assertEquals('Produto YY', self.product.name)
        self.assertEquals(0, self.product.stock)

    def test_if_user_exists(self):
        user = User.objects.all().first()
        self.assertIsNotNone(user)


class StockEntryHttpTest(TestCase):
    fixtures = ['data.json']

    def test_list(self):
        response = self.client.get('/stock_entries/')
        self.assertEquals(200, response.status_code)
        self.assertIn('Produto A', str(response.content))

    def test_create(self):
        url = reverse('entries_create')
        self.client.post(url, {'product': 1, 'amount': 20})
        entry = StockEntry.objects.filter(amount=20, product_id=1).first()
        self.assertIsNotNone(entry)
        self.assertEquals(31, entry.product.stock)
