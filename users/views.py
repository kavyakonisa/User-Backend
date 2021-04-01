from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import *
from .serializers import *
import jwt, datetime
from django.http import Http404
from rest_framework import status



class RegisterView(APIView):
    def post(self,request):
        serializer = userSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self,request):
        email= request.data['email']
        password = request.data['password']
        
        user= User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not Found')

        if not (user.password == password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()

        }    

        token = jwt.encode(payload,'secret',algorithm= 'HS256')

        response= Response()
        response.set_cookie(key='jwt', value = token, httponly = True)
        response.data= {
            'jwt': token
 
        }

        return response 


class UserView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("unauthenticated")
        try:
            payload = jwt.decode(token, 'secret' , algorithms = ['HS256'])
        except jwt.ExpiredSignatureError: 
            raise AuthenticationFailed("unauthenticated")

        user = User.objects.filter(id = payload['id']).filter()  
        serializer = userSerializer(user, many=True)

  
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self,request):
        response= Response()
        response.delete_cookie('jwt')
        response.data = {
            'message' : 'SUCCESS'
        }                 
        return response 


class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = userSerializer(users, many=True)
        return Response(serializer.data)   

class UserDetail(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = userSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("unauthenticated")
        try:
            payload = jwt.decode(token, 'secret' , algorithms = ['HS256'])
        except jwt.ExpiredSignatureError: 
            raise AuthenticationFailed("unauthenticated")
        
        user = self.get_object(pk)
        serializer = userSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("unauthenticated")
        try:
            payload = jwt.decode(token, 'secret' , algorithms = ['HS256'])
        except jwt.ExpiredSignatureError: 
            raise AuthenticationFailed("unauthenticated")
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  
class StudentList(APIView):
   
    def get(self, request, format=None):
        students = Student.objects.all()
        serializer = studentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = studentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentDetail(APIView):

    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        student = self.get_object(pk)
        serializer = studentSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk):
        student = self.get_object(pk)
        serializer = studentSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        student = self.get_object(pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)   


class TeacherList(APIView):
   
    def get(self, request, format=None):
        teachers = Teacher.objects.all()
        serializer = teacherSerializer(teachers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = teacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeacherDetail(APIView):

    def get_object(self, pk):
        try:
            return Teacher.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        teacher = self.get_object(pk)
        serializer = teacherSerializer(teacher)
        return Response(serializer.data)

    def put(self, request, pk):
        teacher = self.get_object(pk)
        serializer = teacherSerializer(teacher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        teacher = self.get_object(pk)
        teacher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)                             