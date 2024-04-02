import logging
import time
from datetime import date

import jwt
import requests
import serial
from dj_rest_auth.registration.views import RegisterView
from django.apps import apps
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Count, Sum
from django.db.models.functions import ExtractMonth, ExtractYear, ExtractWeek
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.views import TokenObtainPairView

from PPH.serializers import (
    CustomRegisterSerializer, UserFunctionSerializer, SupplierSerializer, CustomUserSerializer,
    ContactSerializer, TypeMatiereSerializer, TypePrepSerializer, UniteMesureSerializer,
    FormeReadSerializer, FormeWriteSerializer, MatierePremiereReadSerializer, MatierePremiereWriteSerializer,
    FormuleSerializer, CompositionReadSerializer, CompositionWriteSerializer,
    CatalogueSerializer, VoieSerializer, ListeSerializer, ParametresPrepSerializer, ParametresFormulesListSerializer,
    DemandesReadSerializer, DemandesWriteSerializer, FichesReadSerializer, FichesWriteSerializer, ServiceSerializer,
    ParametresFormulesReadSerializer,
    ConditionnementSerializer, CategorieMatiereSerializer, CatalogueImportSerializer, ReceptionReadSerializer,
    ReceptionWriteSerializer, EtablissementSerializer, ParametresDemandesReadSerializer,
    ParametresDemandesWriteSerializer,
    ParametresFichesReadSerializer, ParametresFichesWriteSerializer, EpiSerializer, EpiFormulesReadSerializer,
    EpiFormulesWriteSerializer,
    AppareilsSerializer, FabricantsAppareilsSerializer, InstructionsAppareilsSerializer, TypeAppareilSerializer,
    TypeCommunicationSerializer,
    ArticlesFormulesListSerializer, ArticlesFormulesReadSerializer, ReponseInstructionsSerializer, EtapesSerializer,
    ControlesSerializer, TypeControleReadSerializer, TypeControleWriteSerializer, PersonnaSerializer
)
from .models import CustomUser, Supplier, UserFunction, Contact, \
    TypeMatiere, UniteMesure, Forme, MatierePremiere, TypePrep, \
    Formule, Composition, Catalogue, Liste, Voie, ParametresPrep, \
    ParametresFormules, Demandes, Fiches, Service, Conditionnement, \
    CategorieMatiere, CatalogueImport, Reception, Etablissement, \
    ParametresDemandes, ParametresFiches, Epi, EpiFormules, Appareils, \
    InstructionsAppareils, FabricantsAppareils, ArticlesFormules, TypeAppareil, \
    TypeCommunication, ReponseInstructions, Etapes, Controles, TypeControle, Personna
from .utils import extract_data_from_pdf
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI

logger = logging.getLogger(__name__)

class PersonnaAPIView(APIView):
    def get(self, request):
        personnas = Personna.objects.all()
        serializer = PersonnaSerializer(personnas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PersonnaSerializer(data=request.data)
        if serializer.is_valid():
            personna = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        personna = self.get_object(pk)
        serializer = PersonnaSerializer(personna, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        personna = self.get_object(pk)
        serializer = PersonnaSerializer(personna, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return Personna.objects.get(pk=pk)
        except Personna.DoesNotExist:
            raise Http404

class ChatGPTView(APIView):
    conversation_history = []  # Stocke l'historique de la conversation

    def post(self, request, *args, **kwargs):
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        user_message = request.data.get("message")
        if not user_message:
            return Response({"error": "Le message ne peut pas être vide."}, status=status.HTTP_400_BAD_REQUEST)

        # Ajouter l'instruction au prompt et l'historique de la conversation
        prompt_message = (
            "Je suis pharmacien hospitalier et tu es un excellent pharmacien, expert en pharmacologie, en chimie, en mathématiques. "
            "Tu excelles dans les méthodes de préparation et de contrôle des formules de préparations magistrales et hospitalières en tout genre."
            "Tu es rigoureux, méthodique et tu respectes la réglementation française en vigueur."
            "Tu t'appuies notamment sur les Bonnes pratiques de Fabrication, les Bonnes Pratiques de Préparations Hospitalières, la pharmacopée française et européenne, les études réalisées par les laboratoires pharmaceutiques et tous les textes règlementaires dans le domaine de la santé. ")

        # Construction des messages pour l'API en incluant l'historique
        messages = [
            {"role": "system", "content": prompt_message}
        ]
        messages.extend(self.conversation_history)  # Ajoute l'historique de la conversation
        messages.append({"role": "user", "content": user_message})  # Ajoute le message actuel de l'utilisateur

        try:
            response = client.chat.completions.create(
                model="gpt-4",  # Assurez-vous d'utiliser le bon modèle
                messages=messages,
                temperature=0.7,
                max_tokens=1500,
            )

            gpt_response = response.choices[0].message.content
            # Ajoute la dernière interaction à l'historique
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": gpt_response})

            return Response({"message": gpt_response}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)  # Pour le débogage
            return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        # Retourne l'historique de la conversation
        return Response({"conversation_history": self.conversation_history}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        self.conversation_history.clear()  # Efface l'historique de la conversation
        return Response({"message": "L'historique de la conversation a été effacé."}, status=status.HTTP_200_OK)



def reset_data(request):
    try:
        # Obtenez tous les modèles de votre application Django
        models = apps.get_models()

        # Parcourez tous les modèles
        for model in models:
            # Vérifiez si le modèle a un champ "reinitialisable"
            if hasattr(model, 'resettable'):
                # Supprimer toutes les instances du modèle réinitialisable
                model.objects.filter(resettable=True).delete()

        return JsonResponse({'success': True, 'message': 'Données réinitialisées.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

class EtablissementViewSet(viewsets.ModelViewSet):
    queryset = Etablissement.objects.all()
    serializer_class = EtablissementSerializer
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data['access']
            refresh_token = response.data['refresh']

            max_age_access = 60 * 60  # 1 heure en secondes
            max_age_refresh = 24 * 60 * 60  # 1 jour en secondes

            new_response = JsonResponse({'detail': 'Authentification réussie'})
            if settings.DEBUG:
                # En mode développement
                new_response.set_cookie('access_token', access_token, max_age=max_age_access, httponly=True,
                                        samesite='None', secure=True)
                new_response.set_cookie('refresh_token', refresh_token, max_age=max_age_refresh, httponly=True,
                                        samesite='None', secure=True)
            else:
                # En production
                new_response.set_cookie('access_token', access_token, max_age=max_age_access, httponly=True,
                                        samesite='None', secure=True)
                new_response.set_cookie('refresh_token', refresh_token, max_age=max_age_refresh, httponly=True,
                                        samesite='None', secure=True)

            return new_response

        return response


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Prepare data for the 'create' endpoint
        response_data = serializer.validated_data
        response_data["user"] = {
            "pk": user.pk,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }

        token = Token.objects.create(user=user)

        # Générer un token pour le nouvel utilisateur
        email_token = default_token_generator.make_token(user)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(request).domain
        domain = domain.replace('http://', '').replace('https://', '')
        protocol = 'https' if request.is_secure() else 'http'
        activate_url = f'{protocol}://{domain}{reverse("validate_account", args=[uid, email_token])}'

        # Créer le contenu du mail de confirmation
        mail_subject = 'Confirmation de votre inscription.'
        message = render_to_string('account/email/email_confirmation_signup.html', {
            'user': user,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': email_token,
            'activate_url': activate_url,
            'username' : user.username,
        })

        # Créer un message en texte brut pour les clients de messagerie qui ne supportent pas HTML
        plain_message = strip_tags(message)

        # Envoyer le mail de bienvenue
        send_mail(mail_subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email], html_message=message)

        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

@api_view(['GET'])
def confirm_email(request, token):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

    try:
        email = serializer.loads(token, salt='email-confirmation', max_age=3600)
    except (SignatureExpired, BadTimeSignature):
        return Response({'message': 'Le lien de confirmation est invalide ou est expiré.'}, status=400)

    user = CustomUser.objects.get(email=email)
    user.is_confirmed = True
    user.save()

    return Response({'message': 'Votre inscription est confirmée'})


class ValidateAccountView(APIView):
    def get(self, request, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()

                login_url = f"{settings.FRONTEND_DOMAIN}/login?accountActivated=true"
                return HttpResponseRedirect(login_url)

            else:
                return Response({"message": "Clé de validation invalide."}, status=400)

        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response({"message": "Id utilisateur invalide."}, status=400)


@api_view(['POST'])
def logout(request):
    try:
        # Utilisez la demande pour identifier l'utilisateur
        user = request.user

        # Supprimez le token d'actualisation pour cet utilisateur
        # (cette logique peut varier en fonction de la façon dont vous stockez et gérez les tokens)
        OutstandingToken.objects.filter(user=user).delete()

        # Supprimez le cookie côté serveur (si vous l'utilisez)
        response = Response({"message": "Vous êtes déconnecté"}, status=status.HTTP_200_OK)
        response.delete_cookie("refreshToken")
        return response

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CustomUserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CustomUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        jwt_token = request.COOKIES.get('access_token')

        try:
            # Valider le token et obtenir sa date d'expiration
            UntypedToken(jwt_token)  # Valide le token
            token_data = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
            expiry = token_data.get('exp')  # Date d'expiration du token en timestamp

            # Calculez le temps restant jusqu'à l'expiration (en secondes)
            time_remaining = expiry - int(time.time())

        except (InvalidToken, TokenError):
            time_remaining = 0  # ou toute autre valeur pour indiquer un token invalide

        data = {
            'id': user.id,
            'email': user.email,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'userName': user.username,
            'function': user.function.title if user.function else None,
            'tokenExpiry': time_remaining
        }

        return Response(data)


class SupplierViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.basename == 'suppliers':
            return Supplier.objects.all()
        elif self.basename == 'appareils-supplier':
            return FabricantsAppareils.objects.all()
        else:
            return Supplier.objects.none()

    def get_serializer_class(self):
        if self.basename == 'suppliers':
            return SupplierSerializer
        elif self.basename == 'appareils-supplier':
            return FabricantsAppareilsSerializer
        else:
            return SupplierSerializer

    def create(self, request, *args, **kwargs):
        # Créez une instance de serializer en utilisant les données soumises par le formulaire
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data.get('name')
        if name:
            serializer.validated_data['name'] = name.capitalize()

        # Sauvegarder l'objet Supplier en base de données
        serializer.save()

        # Répondre avec les données du fournisseur créé et le code de statut 201 (Created)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserFunctionListCreateView(APIView):
    def get(self, request, *args, **kwargs):
        user_functions = UserFunction.objects.all()
        serializer = UserFunctionSerializer(user_functions, many=True)
        return Response(serializer.data)


class ContactView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        name = request.data.get("name")
        email = request.data.get("email")
        message = request.data.get("message")

        # Envoi du courrier
        subject = f"Message de {name}"
        send_mail(subject, message, email, [settings.DEFAULT_TO_EMAIL])

        return Response({"success": "Message envoyé avec succès"}, status=status.HTTP_201_CREATED)

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class DemandesViewSet(viewsets.ModelViewSet):
    queryset = Demandes.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return DemandesReadSerializer
        return DemandesWriteSerializer

class TypeMatiereViewSet(viewsets.ModelViewSet):
    queryset = TypeMatiere.objects.all()
    serializer_class = TypeMatiereSerializer

class TypePrepViewSet(viewsets.ModelViewSet):
    queryset = TypePrep.objects.all()
    serializer_class = TypePrepSerializer

class ParametresPrepViewSet(viewsets.ModelViewSet):
    queryset = ParametresPrep.objects.all()
    serializer_class = ParametresPrepSerializer

class ParametresDemandesViewSet(viewsets.ModelViewSet):
    queryset = ParametresDemandes.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return ParametresDemandesWriteSerializer
        return ParametresDemandesReadSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        # Vérifier si les données sont une liste
        if not isinstance(data, list):
            return Response({"detail": "Invalid data. Expected a list of dictionaries."},
                            status=status.HTTP_400_BAD_REQUEST)

        created_instances = []
        for item in data:
            serializer = self.get_serializer(data=item)
            if serializer.is_valid():
                # Associer le numéro de demande à chaque paramètre
                item['num_demande'] = item.get('num_demande',
                                               None)  # Assurez-vous que num_demande est présent dans vos données JSON
                serializer.save()
                created_instances.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(created_instances, status=status.HTTP_201_CREATED)

class ParametresFichesViewSet(viewsets.ModelViewSet):
    queryset = ParametresFiches.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return ParametresFichesWriteSerializer
        return ParametresFichesReadSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        # Vérifier si les données sont une liste
        if not isinstance(data, list):
            return Response({"detail": "Invalid data. Expected a list of dictionaries."},
                            status=status.HTTP_400_BAD_REQUEST)

        created_instances = []
        for item in data:
            serializer = self.get_serializer(data=item)
            if serializer.is_valid():
                # Associer le numéro de demande à chaque paramètre
                item['num_fiche'] = item.get('num_fiche',
                                               None)  # Assurez-vous que num_demande est présent dans vos données JSON
                serializer.save()
                created_instances.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(created_instances, status=status.HTTP_201_CREATED)

class ParametresFormulesViewSet(viewsets.ModelViewSet):
    queryset = ParametresFormules.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return ParametresFormulesListSerializer
        return ParametresFormulesReadSerializer


class ArticlesFormulesViewSet(viewsets.ModelViewSet):
    queryset = ArticlesFormules.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ArticlesFormulesListSerializer  # Sérialiseur pour les opérations standard
        return ArticlesFormulesReadSerializer  # Sérialiseur pour la lecture

    @action(detail=False, methods=['put'], url_path=r'update/(?P<num_formule>\d+)')
    def update_articles_formules_bulk(self, request, num_formule=None):
        with transaction.atomic():
            received_article_ids = [item.get('article') for item in request.data if item.get('article')]

            # Suppression des articles non présents dans la liste reçue
            ArticlesFormules.objects.filter(num_formule=num_formule).exclude(article__id__in=received_article_ids).delete()

            updated_instances_data = []
            for item in request.data:
                if "id" in item:
                    # Mise à jour d'un objet existant
                    instance = ArticlesFormules.objects.filter(id=item["id"]).first()
                    if not instance:
                        return Response({"error": f"Instance avec id={item['id']} non trouvée."}, status=status.HTTP_404_NOT_FOUND)
                    serializer = self.get_serializer(instance, data=item, partial=True)
                else:
                    # Ajout d'un nouvel objet
                    serializer = self.get_serializer(data=item)

                if serializer.is_valid():
                    serializer.save()
                    updated_instances_data.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(updated_instances_data, status=status.HTTP_200_OK)

class UniteMesureViewSet(viewsets.ModelViewSet):
    queryset = UniteMesure.objects.all()
    serializer_class = UniteMesureSerializer

class ListeViewSet(viewsets.ModelViewSet):
    queryset = Liste.objects.all()
    serializer_class = ListeSerializer

class VoieViewSet(viewsets.ModelViewSet):
    queryset = Voie.objects.all()
    serializer_class = VoieSerializer

class ConditionnementViewSet(viewsets.ModelViewSet):
    queryset = Conditionnement.objects.all()
    serializer_class = ConditionnementSerializer

class CategorieMatiereViewSet(viewsets.ModelViewSet):
    queryset = CategorieMatiere.objects.all()
    serializer_class = CategorieMatiereSerializer

class TypeAppareilViewSet(viewsets.ModelViewSet):
    queryset = TypeAppareil.objects.all()
    serializer_class = TypeAppareilSerializer

class TypeCommunicationViewSet(viewsets.ModelViewSet):
    queryset = TypeCommunication.objects.all()
    serializer_class = TypeCommunicationSerializer
class AppareilsViewSet(viewsets.ModelViewSet):
    queryset = Appareils.objects.all()
    serializer_class = AppareilsSerializer


class ReponseInstructionsViewSet(viewsets.ModelViewSet):
    queryset = ReponseInstructions.objects.all()
    serializer_class = ReponseInstructionsSerializer

class InstructionsAppareilsViewSet(viewsets.ModelViewSet):
   
    queryset = InstructionsAppareils.objects.all()
    serializer_class = InstructionsAppareilsSerializer

    def recuperer_liste_commandes(self, request):
       
        ser = serial.Serial('COM1', 9600)  # Remplacez 'COM1' par le port série approprié
        ser.timeout = 2  # Temps d'attente pour la réponse de la balance

        ser.write(b'I0\r\n')  # Envoyer la commande "I0"

        reponse = ser.read_until(b'\r\n')  # Lire la réponse jusqu'à la fin de ligne
        ser.close()  # Fermer la connexion série

        liste_commandes = reponse.decode().splitlines()  # Séparer la réponse en lignes

        return Response(liste_commandes)

    def envoyer_et_recevoir(self, instruction):
        
        ser = serial.Serial('COM1', 9600)  # Remplacez 'COM1' par le port série approprié
        ser.write(instruction.encode())
        reponse = ser.readline().decode().strip()

        # Obtenir le format de réponse à partir de l'objet d'instruction
        format_reponse = instruction.format_reponse.strip('"')  # Supprime les guillemets

        # Vérifier si la réponse correspond au format attendu
        if reponse.startswith(format_reponse):
            # Extraire le poids et l'unité de la réponse en fonction de la séparation par un espace
            poids, unite = reponse[len(format_reponse):].split(' ', 1)  # Séparation en deux parties au premier espace
        else:
            poids = None
            unite = None

        return poids, unite

    def envoyer_instruction(self, request, pk=None):
        
        instruction = get_object_or_404(InstructionsAppareils, pk=pk)
        reponse = self.envoyer_et_recevoir(instruction.nom_instruction)
        return Response({'reponse': reponse})

    def list(self, request):
        
        queryset = InstructionsAppareils.objects.all()
        serializer = InstructionsAppareilsSerializer(queryset, many=True)
        return Response(serializer.data)

class FormeViewSet(viewsets.ModelViewSet):
    queryset = Forme.objects.all()
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return FormeReadSerializer
        return FormeWriteSerializer

class EtapesViewSet(viewsets.ModelViewSet):
    queryset = Etapes.objects.all()
    serializer_class = EtapesSerializer

class TypeControleViewSet(viewsets.ModelViewSet):
    queryset = TypeControle.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TypeControleReadSerializer
        return TypeControleWriteSerializer


class ControlesViewSet(viewsets.ModelViewSet):
    queryset = Controles.objects.all()
    serializer_class = ControlesSerializer

class EpiViewSet(viewsets.ModelViewSet):
    queryset = Epi.objects.all()
    serializer_class = EpiSerializer

class EpiFormulesViewSet(viewsets.ModelViewSet):
    queryset = EpiFormules.objects.all()
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return EpiFormulesReadSerializer
        return EpiFormulesWriteSerializer

class FichesViewSet(viewsets.ModelViewSet):
    queryset = Fiches.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return FichesReadSerializer
        return FichesWriteSerializer

    @action(detail=False, methods=['get'])
    def count_per_service(self, request):
        # Regroupement des fiches par service et comptage
        count = Fiches.objects.filter(attente_controle=False).values('service__nom').annotate(count=Count('id')).order_by('service__nom')
        return Response(count)

    @action(detail=False, methods=['get'])
    def top_fiches_annuelles(self, request):
        current_year = timezone.now().year
        previous_year = current_year - 1

        # Récupération des 5 fiches les plus utilisées cette année
        top_current_year = (Fiches.objects.filter(date_fab__year=current_year)
                            .select_related('prep')  # Joindre la table Formule
                            .values('prep', 'prep__nom')  # Inclure le champ 'nom' de Formule
                            .annotate(count=Count('prep'))
                            .order_by('-count')[:5])

        # Récupération des données correspondantes pour l'année précédente
        top_previous_year = (
            Fiches.objects.filter(date_fab__year=previous_year, prep__in=[fiche['prep'] for fiche in top_current_year])
            .select_related('prep')  # Joindre la table Formule
            .values('prep', 'prep__nom')  # Inclure le champ 'nom' de Formule
            .annotate(count=Count('prep')))

        # Mise en forme des données pour la réponse
        response_data = {
            'current_year': list(top_current_year),
            'previous_year': {fiche['prep__nom']: fiche for fiche in top_previous_year}
        }

        return Response(response_data)

class FichesSemaine(APIView):
    def get(self, request, format=None):
        current_year = date.today().year
        # Générer une liste de toutes les semaines pour l'année courante
        all_weeks = list(range(1, 53))  # 52 semaines, ajustez si nécessaire
        # Récupérer les données existantes
        fiches = Fiches.objects.annotate(
            week=ExtractWeek('date_fab'),
            year=ExtractYear('date_fab')
        ).filter(year=current_year, controle_valide=True).values(
            'week'
        ).annotate(count=Count('id'), qte=Sum('qté')).order_by('week')

        fiches_dict = {fiche['week']: fiche for fiche in fiches}
        # Compléter les semaines manquantes
        complete_data = [
            fiches_dict.get(week, {'week': week, 'count': 0, 'qte': 0}) for week in all_weeks
        ]

        return Response(complete_data)

class FichesMois(APIView):
    def get(self, request, format=None):
        current_year = date.today().year
        # Générer une liste de tous les mois pour l'année courante
        all_months = list(range(1, 13))
        # Récupérer les données existantes
        fiches = Fiches.objects.annotate(
            month=ExtractMonth('date_fab'),
            year=ExtractYear('date_fab')
        ).filter(year=current_year, controle_valide=True).values(
            'month'
        ).annotate(count=Count('id'), qte=Sum('qté')).order_by('month')

        fiches_dict = {fiche['month']: fiche for fiche in fiches}
        # Compléter les mois manquants
        complete_data = [
            fiches_dict.get(month, {'month': month, 'count': 0, 'qte': 0}) for month in all_months
        ]

        return Response(complete_data)


class MatierePremiereViewSet(viewsets.ModelViewSet):
    queryset = MatierePremiere.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return MatierePremiereReadSerializer
        return MatierePremiereWriteSerializer

    def retrieve_details(self, request, pk=None):
        matiere = self.get_object()
        serializer = self.get_serializer(matiere)
        return Response(serializer.data)

class FormuleViewSet(viewsets.ModelViewSet):
    queryset = Formule.objects.all()
    serializer_class = FormuleSerializer

    @action(detail=False, methods=['get'])
    def dernier_id(self, request):
        dernier_id = Formule.objects.latest('id').id
        return Response({'dernierId': dernier_id})

class CompositionViewSet(viewsets.ModelViewSet):
    queryset = Composition.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CompositionReadSerializer
        return CompositionWriteSerializer

    def create(self, request, *args, **kwargs):
        try:
            compositions_data = request.data.get('compositions', [])
            # Log the received data for debugging purposes
            logger.info(f'Received data: {compositions_data}')

            # Assume you are using a serializer for Composition
            serializer = CompositionWriteSerializer(data=compositions_data, many=True)
            if serializer.is_valid():
                serializer.save()
                # Log the saved data for debugging purposes
                logger.info(f'Saved data: {serializer.data}')
                return Response(serializer.data, status=201)
            else:
                return Response(serializer.errors, status=400)
        except Exception as e:
            logger.error(f'Error processing composition creation: {str(e)}')
            return Response({'error': str(e)}, status=500)

class CompositionFilterView(APIView):
    def get(self, request, num_formule):
        compositions = Composition.objects.filter(num_formule=num_formule)
        serializer = CompositionReadSerializer(compositions, many=True)
        return Response(serializer.data)

class CatalogueImportViewSet(viewsets.ModelViewSet):
    queryset = CatalogueImport.objects.all()
    serializer_class = CatalogueImportSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Call extract_data_from_pdf to process the new record
        notifs = extract_data_from_pdf(serializer.instance)

        # Create a list to store JsonResponse objects for notifications
        notifications_response = []

        # Add each notification to the list
        for notification in notifs:
            notifications_response.append({'notification': notification})

        # Return the serializer data and the list of notifications
        response_data = {
            'serializer.data': serializer.data,
            'notifications': notifications_response
        }

        headers = self.get_success_headers(serializer.data)
        return JsonResponse(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Call extract_data_from_pdf to process the updated record
        notifs = extract_data_from_pdf(serializer.instance)

        # Create a list to store JsonResponse objects for notifications
        notifications_response = []

        # Add each notification to the list
        for notification in notifs:
            notifications_response.append({'notification': notification})

        # Return the serializer data and the list of notifications
        response_data = {
            'serializer.data': serializer.data,
            'notifications': notifications_response
        }

        return JsonResponse(response_data)



class CatalogueViewSet(viewsets.ModelViewSet):
    queryset = Catalogue.objects.all()
    serializer_class = CatalogueSerializer

class ReceptionViewSet(viewsets.ModelViewSet):
    queryset = Reception.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReceptionReadSerializer
        return ReceptionWriteSerializer
