from rest_framework import serializers
from .models import Order, Material, Deposit
from django.contrib.auth.models import User


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['name', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(write_only=True)  # Campo para entrada del nombre del material
    material_display_name = serializers.CharField(source='material.name', read_only=True)  # Campo de solo lectura para mostrar el nombre del material
    deposit_name = serializers.CharField(source='deposit.user.username', read_only=True)  # Mostrar el nombre del usuario asociado al depósito

    class Meta:
        model = Order
        fields = ['id','material_name', 'material_display_name', 'deposit_name', 'quantity', 'reserved', 'delivered']
        extra_kwargs = {
            'material_name': {'write_only': True}  # El campo material_name solo se usa al crear la orden
        }

    def create(self, validated_data):
        # Extraer el nombre del material y normalizarlo
        material_name = validated_data.pop('material_name').strip().lower()

        # Buscar o crear el material ignorando mayúsculas y minúsculas
        material, created = Material.objects.get_or_create(name__iexact=material_name, defaults={'name': material_name})

        # Obtener el usuario logueado
        user = self.context['request'].user

        try:
            # Buscar el depósito que provee ese material
            deposit = Deposit.objects.get(user=user, materials=material)
        except Deposit.DoesNotExist:
            # Si el depósito del usuario no proporciona el material, lo agregamos
            deposit, _ = Deposit.objects.get_or_create(user=user)
            deposit.materials.add(material)
            deposit.save()

        # Crear la orden y asociar el depósito y material
        order = Order.objects.create(material=material, deposit=deposit, **validated_data)

        # Incrementar la cantidad de material disponible
        material.quantity += order.quantity
        material.save()

        return order
    
class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ['id', 'user', 'materials']



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
