from rest_framework.response import Response
from rest_framework import status, viewsets
from django.core.mail import send_mail
from .models import ContactMessage, NotificationLog
from .serializers import ContactMessageSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = ContactMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        
        # Enviar email simple (por consola en desarrollo)
        print(f"📧 Nuevo mensaje de contacto:")
        print(f"   De: {message.name} ({message.email})")
        print(f"   Mensaje: {message.message}")
        
        return Response({"status": "queued"}, status=status.HTTP_201_CREATED)


class NotifyViewSet(viewsets.ViewSet):
    def create(self, request):
        data = request.data
        
        # Guardar registro en DB
        notification = NotificationLog.objects.create(
            to=data["to"],
            subject=data["subject"],
            body=data["body"]
        )
        
        # Mostrar notificación por consola (simple para aprender)
        print(f"🔔 Nueva notificación:")
        print(f"   Para: {notification.to}")
        print(f"   Asunto: {notification.subject}")
        print(f"   Mensaje: {notification.body}")
        
        return Response({"status": "queued"})