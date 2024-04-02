from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    CurrentUserView, ContactView, SupplierViewSet, UserFunctionListCreateView, CustomUserListCreateView,
    CustomUserRetrieveUpdateDestroyView, TypeMatiereViewSet, UniteMesureViewSet, FormeViewSet,
    CompositionViewSet, FormuleViewSet, MatierePremiereViewSet, CatalogueViewSet, ListeViewSet, ServiceViewSet,
    VoieViewSet, TypePrepViewSet, ParametresPrepViewSet, ParametresFormulesViewSet, CompositionFilterView,
    DemandesViewSet, FichesViewSet, FichesSemaine, FichesMois, ConditionnementViewSet, CategorieMatiereViewSet,
    CatalogueImportViewSet, ReceptionViewSet, EtablissementViewSet, ParametresDemandesViewSet, ParametresFichesViewSet,
    EpiViewSet, EpiFormulesViewSet, AppareilsViewSet, InstructionsAppareilsViewSet, ArticlesFormulesViewSet, TypeCommunicationViewSet,
    TypeAppareilViewSet, ReponseInstructionsViewSet, EtapesViewSet, ControlesViewSet, TypeControleViewSet, ChatGPTView, PersonnaAPIView
)
from PPH import views
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'etablissement', EtablissementViewSet)
router.register(r'formules', FormuleViewSet)
router.register(r'suppliers', SupplierViewSet, basename='suppliers')
router.register(r'appareils-suppliers', SupplierViewSet, basename='appareils-supplier')
router.register(r'types-matieres', TypeMatiereViewSet)
router.register(r'unites-mesure', UniteMesureViewSet)
router.register(r'formes', FormeViewSet)
router.register(r'conditionnement', ConditionnementViewSet)
router.register(r'matieres-premieres', MatierePremiereViewSet)
router.register(r'creation-matiere-premiere', MatierePremiereViewSet)
router.register(r'nouvelle-formule', FormuleViewSet)
router.register(r'composition', CompositionViewSet, basename='composition')
router.register(r'demandes', DemandesViewSet)
router.register(r'fiches', FichesViewSet)
router.register(r'reception', ReceptionViewSet)
router.register(r'catalogue', CatalogueViewSet)
router.register(r'catalogue-import', CatalogueImportViewSet)
router.register(r'categories', CategorieMatiereViewSet)
router.register(r'voie', VoieViewSet)
router.register(r'service', ServiceViewSet)
router.register(r'liste', ListeViewSet)
router.register(r'type-prep', TypePrepViewSet)
router.register(r'parametres-prep', ParametresPrepViewSet)
router.register(r'parametres-formules', ParametresFormulesViewSet)
router.register(r'parametres-demandes', ParametresDemandesViewSet)
router.register(r'parametres-fiches', ParametresFichesViewSet)
router.register(r'epi', EpiViewSet)
router.register(r'epi-formules', EpiFormulesViewSet)
router.register(r'appareils', AppareilsViewSet)
router.register(r'type-com', TypeCommunicationViewSet)
router.register(r'types-appareils', TypeAppareilViewSet)
router.register(r'instructions-appareils', InstructionsAppareilsViewSet)
router.register(r'reponses-appareils', ReponseInstructionsViewSet)
router.register(r'articles-formules', ArticlesFormulesViewSet)
router.register(r'etapes', EtapesViewSet)
router.register(r'controles', ControlesViewSet)
router.register(r'type-controle', TypeControleViewSet)
router.register(r'articles-formules/update/<int:num_formule>/', ArticlesFormulesViewSet)

urlpatterns = [
    path('personnas/', PersonnaAPIView.as_view(), name='personnas'),
    path('personnas/<int:pk>/', PersonnaAPIView.as_view(), name='personna-detail'),
    path('chatgpt/', ChatGPTView.as_view(), name='chatgpt'),
    path('reset-data/', views.reset_data, name='reset_data'),
    path('fiches-mois/', FichesMois.as_view(), name='fiches-mois'),
    path('fiches-semaine/', FichesSemaine.as_view(), name='fiches-semaine'),
    path('composition/filter/<int:num_formule>/', CompositionFilterView.as_view(), name='composition-filter'),
    path('current_user/', CurrentUserView.as_view(), name='current-user'),
    path('contact/', ContactView.as_view(), name='contact-create'),
    path('user/update/', CustomUserRetrieveUpdateDestroyView.as_view(), name='user-update'),
    path('users/<int:pk>/', CustomUserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    path('users/', CustomUserListCreateView.as_view(), name='custom-user-list'),
    path('user-functions/', UserFunctionListCreateView.as_view(), name='user-function-list'),
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


