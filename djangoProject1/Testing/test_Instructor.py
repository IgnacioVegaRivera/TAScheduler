import unittest

from django.test import TestCase
from djangoProject1.models import User
from unittest.mock import Mock

# class TestEditContactInfo(unittest.TestCase):
#     def setUp(self):
#         self.temp = User(role="Instructor", phone_number=1011011010, address="356 Kenwood Ave")
#
#     def test_edit_email(self):
#         contactInfo = ["default@example.com", None, None]
#         self.temp.edit_contact_info(contactInfo)
#         self.assertEqual(self.temp.email, "default@example.com")
#
#     def test_edit_phone_number(self):
#         contactInfo = [None, 4144144141, None]
#         self.temp.edit_contact_info(contactInfo)
#         self.assertEqual(self.temp.phone_number, 4144144141)
#
#     def test_edit_address(self):
#         contactInfo = [None, None, "Default 1234 Drive"]
#         self.temp.edit_contact_info(contactInfo)
#         self.assertEqual(self.temp.address, "Default 1234 Drive")
#
#     def test_edit_all(self):
#         contactInfo = ["default@example.com", 4144144141, "Default 1234 Drive"]
#         self.temp.edit_contact_info(contactInfo)
#         self.assertEqual(self.temp.email, "default@example.com")
#         self.assertEqual(self.temp.phone_number, 4144144141)
#         self.assertEqual(self.temp.address, "Default 1234 Drive")
#
#     def test_no_at(self):
#         contactInfo = ["defaultexample.com", None, None]
#         self.temp.edit_contact_info(contactInfo)
#         self.assertEqual(self.temp.email, "default@example.com")
#
#     def test_no_domain(self):
#         contactInfo = ["default@example", None, None]
#         self.temp.edit_contact_info(contactInfo)
#         self.assertEqual(self.temp.email, "default@example.com")
#
#     def test_few_phone_numbers(self):
#         contactInfo = [None, 41414, None]
#         self.temp.edit_contact_info(contactInfo)
#         self.assertEqual(self.temp.phone_number, 1011011010)
#
#     def test_many_phone_numbers(self):
#         contactInfo = [None, 414412425334, None]
#         self.temp.edit_contact_info(contactInfo)
#         self.assertEqual(self.temp.phone_number, 1011011010)
#
#     def test_only_numbers_phone_string(self):
#         contactInfo = [None, "414412425334", None]
#         self.temp.edit_contact_info(contactInfo)
#         self.assertEqual(self.temp.phone_number, 1011011010)
#
#     def test_only_string_address(self):
#         contactInfo = [None, None, 56]
#         self.temp.edit_contact_info(contactInfo)
#         self.assertEqual(self.temp.address, "356 Kenwood Ave")
#
#
#
# class TestViewCourseAssignments(unittest.TestCase):
#
#
#     def test_view_TA_assignments(self):
#         pass
#
#     def test_notify_TAs(self):
#         pass
#
#     def test_assign_TA_Lab(self):
#         pass
#
#     def test_view_public_contact_info(self):
#         pass















