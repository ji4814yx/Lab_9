from django.test import TestCase
from django.urls import reverse

from .models import Place

# Create your tests here.

class TestHomePage(TestCase):
    def test_home_page_shows_empty_list_message_for_empty_database(self):  # use a method
        home_page_url = reverse('place_list')



