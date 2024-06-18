from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from bulletin.serializers import SignUpSerializer
from users.models import CustomUser, OneTimeCode, Profile


class AuthApi(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(email="andreymazo3@mail.ru")
        # self.token = Token.objects.create(user=self.user)

 

    def test_sign_in_email(self):
           
        """
        Ensure we can create a new account object.
        """
        number1 = CustomUser.objects.count()
        print(number1)
        url = reverse('bulletin:sign_in_email')
        data = {'email': 'DabApps@mail.ru'}
        response = self.client.post(url, data, format='json')
        number2 = CustomUser.objects.count()
        print(number2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CustomUser.objects.count(), 2) # Одного создали в сетапе второго здесь
        self.assertEqual(CustomUser.objects.last().email, 'DabApps@mail.ru')
        
        
        
    def test_sign_up_profile(self):
        # self.client.force_login(user=self.user)
        self.client.logout()
        url = reverse('bulletin:sign_up_profile')
        self.client.post(url)
        session = self.client.session
        session['email'] = "andreyma3@mail.ru"
        session.save()
        
        number1 = Profile.objects.count()
        print(number1)
        user=CustomUser.objects.create(email="andreyma3@mail.ru")
        data = {
        "email":"andreymazo3@mail.ru",
        "name":"Giraff",
        "phone_number":"+79213455676"}
        serializer = SignUpSerializer(
            data=data,
            context={"user": user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        number2 = Profile.objects.count()
        print(number2)

        print('self.client', self.client.__dict__)
        print('self.client', self.client.session['email'])
        self.assertEqual(session.get("email"), "andreyma3@mail.ru")
        response = self.client.post(url, data, format='json')#, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)# Уже авторизирован
    
        self.assertEqual(number1, number2-1)
    
  