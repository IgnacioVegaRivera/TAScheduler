from django.test import TestCase, Client

from djangoProject1.MethodFiles.Administrator import CreateUser
from djangoProject1.models import User
### IGNACIO TESTS
class Unit_Admin_CreateAccountTest(TestCase):
    def setUp(self):
        pass

    #tests for valid creations
    #first name tests
    def test_Create_Account_firstName(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            "Bob", "Smith", "4141234567", "UWM 123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount.first_name,"Bob","The first name is not correct")

    def test_blank_firstName(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            "", "Smith", "4141234567", "UWM 123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount, None, "The first name is not correct")

    def test_firstName_with_number(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            "Bob1", "Smith", "4141234567", "UWM 123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount, None, "The first name is not correct")

    def test_firstName_with_special_char(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            "[Bob]", "Smith", "4141234567", "UWM 123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount, None, "The first name is not correct")

    def test_firstName_invalid_type(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            12345, "Smith", "4141234567", "UWM 123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount, None, "The first name is not correct")

    # last name tests
    def test_Create_Account_lastName(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            "Bob", "Smith", "4141234567", "UWM 123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount.last_name,"Smith","The last name is not correct")

    def test_blank_lastName(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            "Bob", "", "4141234567", "UWM 123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount, None, "The last name is not correct")

    def test_lastName_with_number(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            "Bob", "Smith2", "4141234567", "UWM 123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount, None, "The last name is not correct")

    def test_lastName_with_special_char(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            "Bob", "_Smith_", "4141234567", "UWM 123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount, None, "The first name is not correct")

    def test_lastName_invalid_type(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            "Bob", 123, "4141234567", "UWM 123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount, None, "The first name is not correct")

    #username tests
    def test_Create_Account_Username(self):
        newAccount = CreateUser.create_user("login1", "email@gmail.com", "password1",
                                            "Bob", "Smith", "4141234567", "UWM 123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount.username,"login1","The username is not correct")

    def test_blank_username(self):
        newAccount = CreateUser.create_user("", "email@gmail.com", "password1",
            "Bob", "Smith", "4141234567", "UWM 123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount, None, "The username is not correct")

    def test_wrong_type_username(self):
        newAccount = CreateUser.create_user(123, "email@gmail.com", "password1",
                                            "Bob", "Smith", "4141234567", "UWM 123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount, None, "The username is not correct")

    #password tests
    def test_Create_Account_Password(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            "Bob", "Smith", "4141234567", "UWM 123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount.password,"password1","The password is not correct")

    def test_blank_password(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "",
            "Bob", "Smith", "4141234567", "UWM 123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount, None, "The password is not correct")

    def test_wrong_type_password(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", 123,
                                            "Bob", "Smith", "4141234567", "UWM 123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount, None, "The password is not correct")

    #email tests
    def test_Create_Account_Email(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            "Bob", "Smith", "4141234567", "UWM 123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount.email,"email@gmail.com","The email is not correct")

    def test_blank_email(self):
        newAccount = CreateUser.create_user("login", "", "password1",
                                        "Bob", "Smith", "4141234567", "UWM 123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount, None, "The email is not correct")

    def test_wrong_type_email(self):
        newAccount = CreateUser.create_user("login", 456, "password1",
                                            "Bob", "Smith", "4141234567", "UWM 123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount, None, "The email is not correct")

    #phone number tests
    def test_Create_Account_Phone(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            "Bob", "Smith", "4141234567", "UWM 123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount.phone_number,"4141234567","The phone number is not correct")

    def test_small_Phone(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            "Bob", "Smith", "4141234", "UWM 123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount,None,"The phone number is not correct")

    def test_large_phone(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            "Bob", "Smith", "414123456789", "UWM 123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount, None, "The phone number is not correct")

    def test_wrong_type_phone(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            "Bob", "Smith", 4141234567, "UWM 123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount, None, "The phone number is not correct")

    #phone number should be an optional field
    def test_blank_phone(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            "Bob", "Smith", "", "UWM 123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount.phone_number, "", "The phone number is not correct")

    #address tests
    def test_Create_Account_Address(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            "Bob", "Smith", "4141234567", "UWM 123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount.address,"UWM 123","The address is not correct")

    #address is an optional field
    def test_blank_Address(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            "Bob", "Smith", "4141234567", "", "Admin"
                                            , "skills")
        self.assertEqual(newAccount.address, "", "The address is not correct")

    def test_wrong_type_Address(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            "Bob", "Smith", "4141234567", 789, "Admin"
                                            , "skills")
        self.assertEqual(newAccount, None, "The address is not correct")

    def test_no_house_number(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            "Bob", "Smith", "4141234567", "UWM", "Admin"
                                            , "skills")
        self.assertEqual(newAccount, None, "The address is not correct")

    def test_no_street_name(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            "Bob", "Smith", "4141234567", "123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount, None, "The address is not correct")

    #role tests
    def test_Create_Account_Role(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            "Bob", "Smith", "4141234567", "UWM 123", "Admin"
                                            , "skills")
        self.assertEqual(newAccount.role,"Admin","The role is not correct")

    def test_invalid_Role(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            "Bob", "Smith", "4141234567", "UWM 123", "Administrate"
                                            , "skills")
        self.assertEqual(newAccount,None,"The role is not correct")

    #skills tests
    def test_Create_Account_Skills(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            "Bob", "Smith", "4141234567",
                                            "UWM 123", "Admin", "skills")
        self.assertEqual(newAccount.skills,"skills","The skills is not correct")

    def test_invalid_type_Skills(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            "Bob", "Smith", "4141234567",
                                            "UWM 123", "Admin", 4)
        self.assertEqual(newAccount,None,"The skills is not correct")

    #skills is an optional field
    def test_blank_skills(self):
        newAccount = CreateUser.create_user("login", "email@gmail.com", "password1",
                                            "Bob", "Smith", "4141234567",
                                            "UWM 123", "Admin", "")
        self.assertEqual(newAccount.skills, "", "The skills is not correct")

    #unit tests testing created account with default values

    # def test_Create_Account_defaultFirstNames(self):
    #     self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
    #     newAccount = CreateUser.create_user()
    #     self.assertEqual(newAccount.first_name,"DefaultFirst","The default first name is not correct")
    #
    # def test_Create_Account_defaultLastNames(self):
    #     self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
    #     newAccount = CreateUser.create_user()
    #     self.assertEqual(newAccount.last_name,"DefaultLast","The default last name is not correct")
    #
    # def test_Create_Account_defaultUsername(self):
    #     self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
    #     newAccount = CreateUser.create_user()
    #     self.assertEqual(newAccount.username,"Default_Username","The default username is not correct")
    #
    # def test_Create_Account_defaultPassword(self):
    #     self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
    #     newAccount = CreateUser.create_user()
    #     self.assertEqual(newAccount.password,"Default_Password","The default password is not correct")
    #
    # def test_Create_Account_defaultEmail(self):
    #     self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
    #     newAccount = CreateUser.create_user()
    #     self.assertEqual(newAccount.email,"<default@example.com>","The default email is not correct")
    #
    # def test_Create_Account_defaultRole(self):
    #     self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
    #     newAccount = CreateUser.create_user()
    #     self.assertEqual(newAccount.role,"TA","The default role is not correct")

# class Acceptance_Admin_CreateAccountTest(TestCase):
#     def setUp(self):
#         self.donkey = Client()
#
#
#
#     def test_valid_User(self):
#         response = self.donkey.post("/configure_user.html", {"first_name" : "Administrator",
#                 "last_name":"Smith", "username":"login1", "password":"password1", "email":"<EMAIL1>@email.com",
#                 "phone_number":"1141234567", "address":"UWM1", "role":"Admin", "form_name":"create_user"}, follow=True)
#         self.assertEqual(User.objects.count(), 1, "The amount of users do not match")
#         self.assertIn('message', response.context)
#         self.assertEqual(response.context['message'],
#                          "The user \"Administrator Smith\" has been created")
#
#     def test_invalid_User_firstName(self):
#         response = self.donkey.post("/configure_user.html", {"first_name" : "",
#                 "last_name":"Smith", "username":"login1", "password":"password1", "email":"<EMAIL1>@email.com",
#                 "phone_number":"1141234567", "address":"UWM1", "role":"Admin", "form_name":"create_user"}, follow=True)
#         self.assertEqual(User.objects.count(), 0, "The amount of users do not match")
#         self.assertIn('message', response.context)
#         self.assertEqual(response.context['message'],
#                          "Something went wrong when creating the user \" Smith\"")
#
#     def test_invalid_User_lastName(self):
#         response = self.donkey.post("/configure_user.html", {"first_name" : "Administrator",
#                 "last_name":"", "username":"login1", "password":"password1", "email":"<EMAIL1>@email.com",
#                 "phone_number":"1141234567", "address":"UWM1", "role":"Admin", "form_name":"create_user"}, follow=True)
#         self.assertEqual(User.objects.count(), 0, "The amount of users do not match")
#         self.assertIn('message', response.context)
#         self.assertEqual(response.context['message'],
#                          "Something went wrong when creating the user \"Administrator \"")
#
#     def test_invalid_User_Username(self):
#         response = self.donkey.post("/configure_user.html", {"first_name" : "Administrator",
#                 "last_name":"Smith", "username":"", "password":"password1", "email":"<EMAIL1>@email.com",
#                 "phone_number":"1141234567", "address":"UWM1", "role":"Admin", "form_name":"create_user"}, follow=True)
#         self.assertEqual(User.objects.count(), 0, "The amount of users do not match")
#         self.assertIn('message', response.context)
#         self.assertEqual(response.context['message'],
#                          "Something went wrong when creating the user \"Administrator Smith\"")
#
#
#     def test_invalid_User_Password(self):
#         response = self.donkey.post("/configure_user.html", {"first_name" : "Administrator",
#                 "last_name":"Smith", "username":"login1", "password":"", "email":"<EMAIL1>@email.com",
#                 "phone_number":"1141234567", "address":"UWM1", "role":"Admin", "form_name":"create_user"}, follow=True)
#         self.assertEqual(User.objects.count(), 0, "The amount of users do not match")
#         self.assertIn('message', response.context)
#         self.assertEqual(response.context['message'],
#                          "Something went wrong when creating the user \"Administrator Smith\"")
#
#
#     def test_invalid_User_Email(self):
#         response = self.donkey.post("/configure_user.html", {"first_name" : "Administrator",
#                 "last_name":"Smith", "username":"login1", "password":"password1", "email":"",
#                 "phone_number":"1141234567", "address":"UWM1", "role":"Admin", "form_name":"create_user"}, follow=True)
#         self.assertEqual(User.objects.count(), 0, "The amount of users do not match")
#         self.assertIn('message', response.context)
#         self.assertEqual(response.context['message'],
#                          "Something went wrong when creating the user \"Administrator Smith\"")
#
#
#     def test_invalid_User_PhoneNumber(self):
#         response = self.donkey.post("/configure_user.html", {"first_name" : "Administrator",
#                 "last_name":"Smith", "username":"login1", "password":"password1", "email":"<EMAIL1>@email.com",
#                 "phone_number":"", "address":"UWM1", "role":"Admin", "form_name":"create_user"}, follow=True)
#         self.assertEqual(User.objects.count(), 0, "The amount of users do not match")
#         self.assertIn('message', response.context)
#         self.assertEqual(response.context['message'],
#                          "Something went wrong when creating the user \"Administrator Smith\"")
#
#
#     def test_invalid_User_Address(self):
#         response = self.donkey.post("/configure_user.html", {"first_name" : "Administrator",
#                 "last_name":"Smith", "username":"login1", "password":"password1", "email":"<EMAIL1>@email.com",
#                 "phone_number":"1141234567", "address":"", "role":"Admin", "form_name":"create_user"}, follow=True)
#         self.assertEqual(User.objects.count(), 0, "The amount of users do not match")
#         self.assertIn('message', response.context)
#         self.assertEqual(response.context['message'],
#                          "Something went wrong when creating the user \"Administrator Smith\"")
#
#
#     def test_invalid_User_Role(self):
#         response = self.donkey.post("/configure_user.html", {"first_name" : "Administrator",
#                 "last_name":"Smith", "username":"login1", "password":"password1", "email":"<EMAIL1>@email.com",
#                 "phone_number":"1141234567", "address":"UWM1", "role":"", "form_name":"create_user"}, follow=True)
#         self.assertEqual(User.objects.count(), 0, "The amount of users do not match")
#         self.assertIn('message', response.context)
#         self.assertEqual(response.context['message'],
#                          "Something went wrong when creating the user \"Administrator Smith\"")
#
#
#     def test_invalid_User_FormName(self):
#         response = self.donkey.post("/configure_user.html", {"first_name" : "Administrator",
#                 "last_name":"Smith", "username":"login1", "password":"password1", "email":"<EMAIL1>@email.com",
#                 "phone_number":"1141234567", "address":"UWM1", "role":"Admin", "form_name":""}, follow=True)
#         self.assertEqual(User.objects.count(), 0, "The amount of users do not match")
#         self.assertIn('message', response.context)
#         self.assertEqual(response.context['message'],
#                          "Something went wrong when fetching the form, please try again")



###
###
###AADI TESTS

