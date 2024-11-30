import os
from django.conf import settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'SEA_Module.settings'

from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import datetime
from trades.models import Trade, Trader, Bank
from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

# Test the CREATE, READ, UPDATE functionalities using Bank model, reproducible for Trade and Trader models
class BankModelTest(TestCase):
    def test_create_bank(self):
        bank = Bank.objects.create(bank_name="Test")
        self.assertEqual(Bank.objects.count(), 1)
        self.assertEqual(bank.bank_name, "Test")

    def test_read_bank(self):
        item = Bank.objects.create(bank_name="HSBC")
        retrieved_item = Bank.objects.get(id=item.id)
        self.assertEqual(retrieved_item.bank_name, "HSBC")

    def test_update_bank(self):
        item = Bank.objects.create(bank_name="Chase")
        item.bank_name = "Chase Bank"
        item.save()
        updated_item = Bank.objects.get(id=item.id)
        self.assertEqual(updated_item.bank_name, "Chase Bank")

# Test data inputs for Trade model - testing for various data types
class TradeModelTest(TestCase):
    def setUp(self):
        self.trader = Trader.objects.create(
            first_name="Dummy",
            last_name="Data",
            email="dummy.data@testing.com",
        )
        self.bank = Bank.objects.create(bank_name="Test Bank")

    # Test for successful trade creation
    def test_trade_creation(self):
        trade = Trade.objects.create(
            trade_name="Bond Asset Swap",
            status="Accepted",
            status_comments="Trade executed successfully.",
            quantity=100,
            price=Decimal("1500.00"),
            trader=self.trader,
            bank=self.bank,
        )
        self.assertEqual(trade.trade_name, "Bond Asset Swap")
        self.assertEqual(trade.status, "Accepted")
        self.assertEqual(trade.quantity, 100)
        self.assertEqual(trade.price, Decimal("1500.00"))
        self.assertEqual(trade.trader, self.trader)
        self.assertEqual(trade.bank, self.bank)
        self.assertIsNotNone(trade.datetime)

    # trade_name is from a drop-down selection - testing an invalid string if it raises a ValidationError
    def test_invalid_trade_name_choice(self):
        trade = Trade(
            trade_name="Cryptocurrency",  # <--- This is not in the selection
            status="Accepted",
            quantity=100,
            price=Decimal("1500.00"),
            trader=self.trader,
            bank=self.bank,
        )
        with self.assertRaises(ValidationError):
            trade.full_clean()

    # Likewise, status can only be "Accepted", "Pending", or "Rejected"
    def test_invalid_status_choice(self):
        trade = Trade(
            trade_name="Bond Asset Swap",
            status="Expired",  # Invalid choice
            quantity=100,
            price=Decimal("1500.00"),
            trader=self.trader,
            bank=self.bank,
        )
        with self.assertRaises(ValidationError):
            trade.full_clean()

    # Testing for quantity validations
    def test_quantity_validation(self):
        trade = Trade(
            trade_name="Bond Asset Swap",
            status="Pending",
            quantity=500,  # Valid value
            price=Decimal("2000.00"),
            trader=self.trader,
            bank=self.bank,
        )
        trade.full_clean()  # Should pass

        # Invalid quantity - minimum is 1
        trade.quantity = 0
        with self.assertRaises(ValidationError):
            trade.full_clean()

        # Invalid quantity - exceeded threshold
        trade.quantity = 1500
        with self.assertRaises(ValidationError):
            trade.full_clean()

    # Testing for price validations
    def test_price_validation(self):
        # Valid price
        trade = Trade(
            trade_name="Bond Asset Swap",
            status="Pending",
            quantity=100,
            price=Decimal("500.00"),  # Minimum is GBP £500.00
            trader=self.trader,
            bank=self.bank,
        )
        trade.full_clean()

        # Invalid price - price is lower than Markets standard
        trade.price = Decimal("499.99")
        with self.assertRaises(ValidationError):
            trade.full_clean()

        # Invalid price - greater than what can be traded at a given time
        trade.price = Decimal("1000001.00")
        with self.assertRaises(ValidationError):
            trade.full_clean()

    # Testing if trader and bank fields accept null values since this is not always necessary
    def test_foreign_key_null_values(self):
        trade = Trade.objects.create(
            trade_name="Bond Outright",
            status="Rejected",
            status_comments="Not approved by risk.",
            quantity=50,
            price=Decimal("7500.00"),
            trader=None,  # No trader
            bank=None,  # No bank
        )
        self.assertIsNone(trade.trader)
        self.assertIsNone(trade.bank)

    # Testing that datetime is auto-populated as this is necessary for timestamps
    def test_datetime_auto_now_add(self):
        trade = Trade.objects.create(
            trade_name="Bond Butterfly",
            status="Accepted",
            status_comments="Successful trade.",
            quantity=75,
            price=Decimal("1200.00"),
            trader=self.trader,
            bank=self.bank,
        )
        self.assertIsNotNone(trade.datetime)
        self.assertTrue(isinstance(trade.datetime, datetime))

# Test delete functionality is reserved only for admin users
class DeleteTradeViewTests(TestCase):
    def setUp(self):
        # Create admin and regular users
        self.staff_user = User.objects.create_user(username="admin", password="password123", is_staff=True)
        self.non_staff_user = User.objects.create_user(username="regular", password="password123", is_staff=False)

        # Create trader and bank instances
        self.trader = Trader.objects.create(first_name="John", last_name="Doe", email="john.doe@example.com")
        self.bank = Bank.objects.create(bank_name="Test Bank")

        # Create a trade
        self.trade = Trade.objects.create(
            trade_name="Bond Asset Swap",
            status="Pending",
            quantity=10,
            price=1000.00,
            trader=self.trader,
            bank=self.bank
        )

    # SECURITY TEST
    # Unauthenticated user are redirected to login page
    def test_redirect_for_unauthenticated_users(self):
        url = reverse('trades:trade-delete', kwargs={'pk': self.trade.id})
        response = self.client.get(url)
        self.assertRedirects(response, f"{reverse('login')}?next={url}")

    # SECURITY TEST
    # Test if regular users are unable to delete but instead, they are redirected to the unauthorised-action page from template unauthorised_message.html
    def test_delete_for_regular_users(self):
        self.client.login(username="regular", password="password123")
        url = reverse('trades:trade-delete', kwargs={'pk': self.trade.id})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('unauthorised-action'))

        response_after = self.client.get(reverse('unauthorised-action'))
        self.assertTemplateUsed(response_after, 'unauthorised_message.html')

        # Check if the unauthorised message is rendered on the page
        self.assertContains(response_after, "You are not authorised to delete records.")

    # Test if admin users are able to delete records
    def test_delete_trade_for_staff_users(self):
        self.client.login(username="admin", password="password123")
        url = reverse('trades:trade-delete', kwargs={'pk': self.trade.id})

        # Checking if GET request renders delete confirmation page
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trades/trade_delete.html")
        self.assertContains(response, self.trade.trade_name)

        # Checking if POST request deletes the trade
        response = self.client.post(url)
        self.assertRedirects(response, reverse('trades:trade-list'))
        self.assertEqual(Trade.objects.count(), 0)

    # Admin users should see a message confirming the trade is deleted
    def test_success_message_after_deletion(self):
        self.client.login(username="admin", password="password123")
        url = reverse('trades:trade-delete', kwargs={'pk': self.trade.id})
        response = self.client.post(url, follow=True)  # Follow redirects to check messages

        self.assertContains(response, "Trade successfully deleted.")

# Test login functionality
class UserSignupAndLoginTests(TestCase):
    def setUp(self):
        self.admin_signup_url = reverse('admin-signup')
        self.regular_user_signup_url = reverse('regular-user-signup')
        self.login_url = reverse('login')
        self.home_page_url = reverse('home-page')
        self.landing_page_url = reverse('landing-page')

        self.admin_group, created = Group.objects.get_or_create(name='Admin')
        self.regular_user_group, created = Group.objects.get_or_create(name='Regular User')

    def test_signup(self):
        data = {
            'username': 'adminuser',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'email': 'adminuser@example.com'
        }

        response = self.client.post(self.admin_signup_url, data)
        self.assertRedirects(response, reverse('login'))
        user = User.objects.get(username='adminuser')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(self.admin_group in user.groups.all())

    def test_login(self):
        admin_user = User.objects.create_user(username='adminuser', password='adminpassword123')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        admin_user.groups.add(self.admin_group)

        response = self.client.post(self.login_url, {'username': 'adminuser', 'password': 'adminpassword123'})

        self.assertRedirects(response, self.home_page_url)

    def test_redirect_to_landing_page_after_logout(self):
        User.objects.create_user(username='testuser', password='testpassword123')
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, self.landing_page_url)

    # SECURITY TEST
    def test_redirect_to_landing_page_if_not_logged_in(self):
        # Attempt to access the home page without being logged in
        response = self.client.get(self.home_page_url)

        # Expect user to be redirected to the login page
        self.assertRedirects(response, f'{self.login_url}?next={self.home_page_url}')
