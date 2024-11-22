from djangoProject1.models import User, Course, Lab
from django.test import TestCase, Client
import unittest
from unittest.mock import Mock

class UnitTATest(unittest.TestCase):
    def setUp(self):
        self.temp = User(phone_number="4144340987", address= "3028 N 89th St")

    #def test_edit_contact_info(self):


#compares a defined dictionary with the returned one from the method
    #def test_view_TA_assignments(self):


#compares a defined dictionary with the returned one from the method
    #def test_view_public_contact_info(self):

















# class AcceptanceTATest(unittest.TestCase):