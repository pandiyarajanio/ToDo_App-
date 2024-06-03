from django.shortcuts import render
import pyrebase
from rest_framework import generics
from rest_framework.response import Response
from .serializers import ToDoSerializer
from .models import Todo
from rest_framework import serializers
from rest_framework.views import APIView

config = {
    "apiKey": "AIzaSyNdHr3hyG8VzaPfu-UadV1_hWwpalKHo",
    "authDomain": "todoapp-c9012.firebaseapp.com",
    "databaseURL": "https://todoapp-c9012-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "todoapp-c9012",
    "storageBucket": "todoapp-c9012.appspot.com",
    "messagingSenderId": "798375133589",
    "appId": "1:798375133589:web:e338db000300d21b5af69c",
    "measurementId": "G-MBDQYF975C"
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()

def my_view(request):
    try:
        message = "Database Connection Successful"
    except Exception as e:
        message = "Error: " + str(e) + ". Something is issue!"

    return render(request, 'index.html', {'message': message})




class ListTodo(APIView):
    def get(self, request):
        todos = database.child("todos").get()
        todo_list = [{"id": todo.key(), "name": todo.val()['name'], "status": todo.val()['status']} for todo in todos.each()]
        return Response(todo_list)

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo  # Assuming you have a Todo model
        fields = ['id', 'name', 'status']


class DetailTodo(generics.RetrieveUpdateAPIView):
    serializer_class = TodoSerializer

    def get(self, request, pk):
        todo = database.child("todos").child(pk).get()
        serializer = self.serializer_class(todo.val())
        return Response(serializer.data)

    def put(self, request, pk):
        data = request.data
        database.child("todos").child(pk).update({"name": data['name'], "status": data['status']})
        return Response({'id': pk, 'name': data['name'], 'status': data['status']})




class TodoSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    status = serializers.CharField()

class CreateTodo(generics.CreateAPIView):
    serializer_class = ToDoSerializer 

    def post(self, request):
        data = request.data
        todo_data = {"name": data['name'], "status": data['status']}
        database.child("todos").push(todo_data)
        return Response(todo_data)

class DeleteTodo(generics.DestroyAPIView):
    def delete(self, request, pk):
        todo = database.child("todos").child(pk).get()
        if todo.val() is None:
            return Response({'error': 'Todo not found'}, status=404)
        try:
            database.child("todos").child(pk).remove()
        except Exception as e:
            return Response({'error': 'Failed to delete todo'}, status=500)
        return Response({'message': 'Todo deleted successfully'})