from django.test import TestCase, Client
from django.shortcuts import reverse
from trades.models import Trade, Trader, Bank
import json

class HomePageTests(TestCase):

    def test_status_code(self):
        response = self.client.get(reverse('home-page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_page.html')

class LandingPageTests(TestCase):

    def test_status_code(self):
        response = self.client.get(reverse('landing-page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing_page.html')

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.trade_list_url = reverse('trade-list')
        self.trade_detail_url = reverse('trade-detail')

    def test_trade_detail_GET(self):
        response = self.client.get(self.trade_detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'trades/trade_detail.html')

    def test_trade_list_GET(self):
        response = self.client.get(self.trade_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'trades/trade_list.html')
