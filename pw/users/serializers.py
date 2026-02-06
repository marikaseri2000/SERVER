from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model
from partecipanti.models import Partecipante

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True)
    admin_key = serializers.CharField(write_only=True, required=False, help_text="Chiave segreta per registrare un admin")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'admin_key']

    def validate(self, data):
        # 1. Controllo coincidenza password
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Le password non coincidono'})
        
        # 2. Controllo se si sta registrando un admin
        admin_key = data.get('admin_key')
        is_admin_registration = admin_key is not None
        
        if is_admin_registration:
            # Verifica admin_key
            if admin_key != settings.ADMIN_SECRET_KEY:
                raise serializers.ValidationError({'admin_key': 'Chiave admin non valida'})
        else:
            # 3. Controllo Whitelist per partecipanti (Il database deve avere questa email)
            if not Partecipante.objects.filter(email_preautorizzata=data['email']).exists():
                raise serializers.ValidationError({'email': 'Questa email non risulta tra i partecipanti autorizzati.'})

        return data

    def create(self, validated_data):
        # Togliamo password2 e admin_key prima di salvare nel DB
        validated_data.pop('password2')
        admin_key = validated_data.pop('admin_key', None)
        
        # Determiniamo il tipo di utente
        is_admin_registration = admin_key is not None
        
        if is_admin_registration:
            # Creiamo un admin
            user = User.objects.create_user(**validated_data, is_admin=True)
        else:
            # Creiamo un partecipante
            user = User.objects.create_user(**validated_data, is_participant=True)
            
            # Colleghiamo l'utente al profilo partecipante esistente
            try:
                partecipante = Partecipante.objects.get(email_preautorizzata=user.email)
                partecipante.user = user
                partecipante.save()
            except Partecipante.DoesNotExist:
                # Protezione nel caso l'email sparisca tra validate e create
                user.delete()
                raise serializers.ValidationError({'email': 'Errore durante il collegamento al partecipante.'})

        return user