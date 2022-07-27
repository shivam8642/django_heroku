
from django.test import TestCase
from requests import request
from .forms import Signupform
from django.urls import reverse
# Create your tests here.


class BaseTest(TestCase):
    def test_UserForm_invalid(self):
        url=reverse('ajax_load_cities')
        response=self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_index(self):
        url=reverse('index')
        response=self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_user(self):
        url=reverse('createuser')
        form={
            'username':'shivam',
            'first_name':'shivam',
            'last_name':'verma',
            'email':'shivam@mail.com',
            'password1':'sss11sss',
            'password2':'sss11sss'
        }
        form=Signupform(data=form)
        form.save()
        self.assertTrue(form.is_valid())
        response=self.client.post(url,form)
        self.assertEqual(response.status_code,200)
        response=self.client.get(url,form)
        self.assertEqual(response.status_code,200)

















# class User_Form_Test(TestCase):

#     # Valid Form Data
#     def test_UserForm_valid(self):
#         form = Signupform(data={'email': "user@mp.com", 'password': "user", 'first_name': "user",'last_name':"vema" })
#         self.assertFalse(form.is_valid())

#     # Invalid Form Data
#     def test_UserForm_invalid(self):
#         form = Signupform(data={'email': "", 'password': "mp", 'first_name': "mp",})
#         self.assertFalse(form.is_valid())


# class EntryModelTest(TestCase):
#     def test_string_representation(self):
#         entry = Product.objects.create(name="shivam",price=399)
#         self.assertEqual(str(entry),entry.name)

# class Testviews(TestCase):
#     def setUp(self):
#         self.register_url=(reverse('index'))
#         self.cart=(reverse('cartdata'))
#         self.user=(reverse('createuser'))
      

# class Testindex(Testviews):
#     def test_views(self):
#         response=self.client.get(self.register_url)
#         self.assertEqual(response.status_code,200)
#         self.assertTemplateUsed(response,"index.html")


#     def insert(self):
#         form=Signupform(username="shivam",password="sss11sss").save()
#         response=self.client.post(form,self.user)
#         self.assertEqual(response.status_code,200)



#     def test_cart(self):
#         response=self.client.get(self.cart)
#         self.assertEqual(response.status_code,302)
  


# class Test_login(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.login_url = reverse('login')
#         self.logout_url = reverse('logout')
#         self.register_url = reverse('createuser')

#     def test_register_post(self):
#         response = self.client.get(reverse('createuser'), {
#             'username': 'testuser',
#             'email': 'testuser@gmail.com',
#             'password': 'testpassword',
#             'password2': 'testpassword',
#         })
#         self.assertEquals(response.status_code, 200)
        

#     def test_login_post(self):
#         response = self.client.post(reverse('login'), {
#             'username': 'testuser',
#             'password': 'testpassword',
#         })
#         self.assertEquals(response.status_code, 200)

#     def test_logout_redirect_succeeds(self):
#         self.client.login(username='testuser', password='testpassword')
#         response = self.client.post(reverse('logout'), follow=True)
#         self.assertEquals(response.status_code, 200)


    
         
         
    

    
    

