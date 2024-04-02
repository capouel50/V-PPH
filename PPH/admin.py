from django.contrib import admin
from .models import (CustomUser, UserFunction, Supplier, TypeMatiere, \
    UniteMesure, Forme, MatierePremiere, Liste, TypePrep, Formule, Composition, \
    Catalogue, Voie, ParametresPrep, ParametresFormules, Demandes, Fiches, Service, \
    Conditionnement, CategorieMatiere, CatalogueImport, Reception, Etablissement, \
    ParametresDemandes, ParametresFiches, Appareils, FabricantsAppareils, InstructionsAppareils, ReponseInstructions, \
    TypeAppareil, TypeCommunication, Epi, EpiFormules, ArticlesFormules, Etapes, Controles, TypeControle, Personna)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'function', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff', 'function')

class UserFunctionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserFunction, UserFunctionAdmin)
admin.site.register(Supplier)
admin.site.register(Etapes)
admin.site.register(Controles)
admin.site.register(TypeControle)
admin.site.register(Personna)

@admin.register(Etablissement)
class EtablissementAdmin(admin.ModelAdmin):
    list_display = ['nom_long','nom_court', 'address', 'postal', 'city', 'phone', 'email', 'site', 'logo']

@admin.register(TypeMatiere)
class TypeMatiereAdmin(admin.ModelAdmin):
    list_display = ['id','nom']

@admin.register(UniteMesure)
class UniteMesureAdmin(admin.ModelAdmin):
    list_display = ['nom']

@admin.register(Forme)
class FormeAdmin(admin.ModelAdmin):
    list_display = ['nom', 'unite_mesure', 'unite_stock']

@admin.register(Epi)
class EpiAdmin(admin.ModelAdmin):
    list_display = ['nom']

@admin.register(EpiFormules)
class EpiFormulesAdmin(admin.ModelAdmin):
    list_display = ['num_formule', 'epi', 'resettable']

@admin.register(TypeCommunication)
class TypeCommunicationAdmin(admin.ModelAdmin):
    list_display = ['nom']
@admin.register(TypeAppareil)
class TypeAppareilAdmin(admin.ModelAdmin):
    list_display = ['nom']
@admin.register(Appareils)
class AppareilsAdmin(admin.ModelAdmin):
    list_display = ['nom', 'modele', 'fabricant']

@admin.register(ReponseInstructions)
class ReponseInstructionsAdmin(admin.ModelAdmin):
    list_display = ['nom', 'format', 'message']
@admin.register(InstructionsAppareils)
class InstructionsAppareilsAdmin(admin.ModelAdmin):
    list_display = ['nom', 'modele_appareil', 'instruction', 'description']

@admin.register(FabricantsAppareils)
class FabricantsAppareilsAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'postal', 'city', 'country', 'email', 'phone', 'site', 'is_activate', 'user_code', 'password']
@admin.register(Liste)
class ListeAdmin(admin.ModelAdmin):
    list_display = ['nom']

@admin.register(Conditionnement)
class ConditionnementAdmin(admin.ModelAdmin):
    list_display = ['nom']
@admin.register(Voie)
class VoieAdmin(admin.ModelAdmin):
    list_display = ['nom']

@admin.register(TypePrep)
class TypePrepAdmin(admin.ModelAdmin):
    list_display = ['nom']

@admin.register(ParametresPrep)
class ParametresPrepAdmin(admin.ModelAdmin):
    list_display = ['nom', 'unite']

@admin.register(ParametresFormules)
class ParametresFormulesAdmin(admin.ModelAdmin):
    list_display = ['num_formule', 'parametre']

@admin.register(ArticlesFormules)
class ArticlesFormulesAdmin(admin.ModelAdmin):
    list_display = ['num_formule', 'article']

@admin.register(ParametresDemandes)
class ParametresDemandesAdmin(admin.ModelAdmin):
    list_display = ['num_demande', 'parametre', 'valeur_parametre']

@admin.register(ParametresFiches)
class ParametresFichesAdmin(admin.ModelAdmin):
    list_display = ['num_fiche', 'parametre', 'valeur_parametre']

@admin.register(CategorieMatiere)
class CategorieMatiereAdmin(admin.ModelAdmin):
    list_display = ['nom', 'fournisseur']
@admin.register(Demandes)
class DemandesAdmin(admin.ModelAdmin):
    list_display = ['date_demande', 'prep', 'typePrep', 'date_prevu', 'patient', 'age', 'service', 'prescripteur', 'commentaire', 'production']

@admin.register(Fiches)
class FichesAdmin(admin.ModelAdmin):
    list_display = ['prep']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['nom']

@admin.register(MatierePremiere)
class MatierePremiereAdmin(admin.ModelAdmin):
    list_display = ['nom', 'type', 'forme', 'qté_cdt', 'fournisseur', 'prix', 'prix_unit',
                    'qté_stock', 'stock_mini', 'stockee', 'cde', 'cde_auto', 'attente_livraison',]

@admin.register(Formule)
class TypePrepAdmin(admin.ModelAdmin):
    list_display = ['nom', 'type']

@admin.register(Composition)
class Composition(admin.ModelAdmin):
    list_display = ['num_formule', 'matiere', 'qté', 'calcul']

@admin.register(CatalogueImport)
class CatalogueImportAdmin(admin.ModelAdmin):
    list_display = ['pdf', 'fournisseur', 'categorie', 'page_debut', 'page_fin', 'code_debut', 'code_fin', 'date_import']

@admin.register(Catalogue)
class CatalogueAdmin(admin.ModelAdmin):
    list_display = ['designation', 'code_fournisseur', 'cip', 'fournisseur', 'qté', 'unite']

@admin.register(Reception)
class ReceptionAdmin(admin.ModelAdmin):
    list_display = ['date_reception', 'matiere', 'lot', 'peremption', 'qte', 'certificat']