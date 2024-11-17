from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from .models import Order, Material, Deposit
from .serializers import OrderSerializer, DepositSerializer, MaterialSerializer, UserSerializer, MaterialSerializer

class MaterialListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    #renderer_classes = [TemplateHTMLRenderer]
    #template_name = 'material_list.html'

class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    #renderer_classes = [TemplateHTMLRenderer]
    #template_name = 'order_list.html'

class ReserveOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, reserved=False)
            order.reserved = True
            order.save()
            return Response({"message": "Order reserved"}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error": "Order not found or already reserved"}, status=status.HTTP_400_BAD_REQUEST)

class CreateOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    #renderer_classes = [TemplateHTMLRenderer]
    #template_name = 'create_order.html'

    def post(self, request):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Order created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeliverOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, reserved=True, delivered=False)
        except Order.DoesNotExist:
            return Response({"error": "Order not found or not reserved"}, status=status.HTTP_404_NOT_FOUND)

        # Marcar la orden como entregada y reducir el inventario
        order.delivered = True
        order.save()

        material = order.material
        if order.quantity > material.quantity:
            return Response({"error": "Not enough material in stock"}, status=status.HTTP_400_BAD_REQUEST)

        material.quantity -= order.quantity
        material.save()

        ## Ejecutar el código de la clase RegisterMaterialProviderView
        #register_material_provider(material.name, request)

        return Response({"message": "Order delivered successfully"}, status=status.HTTP_200_OK)

def register_material_provider(material_name, request):
    register_material_provider_view = RegisterMaterialProviderView()
    request.data['material_name'] = material_name
    register_material_provider_view.post(request)

class RegisterMaterialProviderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Obtener el depósito del usuario logueado
        try:
            deposit = Deposit.objects.get(user=request.user)
        except Deposit.DoesNotExist:
            return Response({"error": "No deposit found for the user"}, status=status.HTTP_404_NOT_FOUND)

        # Obtener el nombre del material desde los datos del request
        material_name = request.data.get('material_name', '').strip().lower()

        if not material_name:
            return Response({"error": "Material name is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Buscar o crear el material, ignorando mayúsculas y minúsculas
        material, created = Material.objects.get_or_create(name__iexact=material_name, defaults={'name': material_name})

        # Asociar el material con el depósito del usuario
        deposit.materials.add(material)
        deposit.save()

        message = "Material created and registered as provider" if created else "Registered as provider for material"
        return Response({"message": message}, status=status.HTTP_200_OK)


class RegisterUserAPIView(APIView):
    #renderer_classes = [TemplateHTMLRenderer]
    #template_name = 'register_user.html'

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
