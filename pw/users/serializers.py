from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model
from partecipanti.models import Partecipante

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, data):
        # 1. Controllo coincidenza password
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Le password non coincidono'})
        
        # 2. Controllo Whitelist (Il database deve avere questa email)
        # NOTA: Usiamo email_preautorizzata (nome corretto del campo)
        if not Partecipante.objects.filter(email_preautorizzata=data['email']).exists():
            raise serializers.ValidationError({'email': 'Questa email non risulta tra i partecipanti autorizzati.'})

        return data

    def create(self, validated_data):
        # Togliamo password2 prima di salvare nel DB
        validated_data.pop('password2')
        
        # Recuperiamo la admin_key dalla richiesta
        request = self.context.get('request')
        admin_key_received = request.data.get('admin_key') if request else None
        
        is_admin = False
        if admin_key_received and admin_key_received == settings.ADMIN_SECRET_KEY:
            is_admin = True
        
        # Creiamo l'utente
        user = User.objects.create_user(
            **validated_data, 
            is_admin=is_admin,
            is_participant=not is_admin
        )
        
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