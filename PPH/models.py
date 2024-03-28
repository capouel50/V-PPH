from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.urls import reverse
from datetime import date
from .utils import convert_quantity
from django.db import transaction
from datetime import timedelta
from django.db.models import JSONField
class Etablissement(models.Model):

    nom_long = models.CharField(max_length=100, unique=True)
    nom_court = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=100, blank=True)
    postal = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=254, blank=True)
    site = models.URLField(max_length=200, blank=True)
    logo = models.ImageField(upload_to='hopitaux/', default='hopitaux/defaut.jpg')

    class Meta:
        ordering = ['nom_long']

    def get_absolute_url(self):
        return reverse('fiche', args=[str(self.id)])

    def __str__(self):
        return self.nom_long

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('L\'email est obligatoire')

        email = self.normalize_email(email)

        # Capitaliser les prénoms et les noms
        first_name = first_name.title()
        last_name = last_name.title()

        # Générer le username à partir de la première lettre du first_name et du last_name
        username = f'{first_name[0]}{last_name}'.lower().replace(' ', '_')

        user = self.model(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, password=None):
        user = self.create_user(email, first_name, last_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class UserFunction(models.Model):
    title = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='users/', default='users/user.png')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    function = models.ForeignKey(UserFunction, on_delete=models.SET_NULL, default=9, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        ordering = ['last_name']

    def __str__(self):
        return self.username

class FabricantsAppareils(models.Model):

    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=100, blank=True)
    postal = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    site = models.URLField(max_length=200, blank=True)
    user_code = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=True)
    is_activate = models.BooleanField(default=True)


    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class TypeAppareil(models.Model):
    nom = models.CharField(max_length=200)
    def __str__(self):
        return self.nom

class TypeCommunication(models.Model):
    nom = models.CharField(max_length=200)
    def __str__(self):
        return self.nom
class Appareils(models.Model):
    type = models.ForeignKey(TypeAppareil, on_delete=models.CASCADE)
    com = models.ForeignKey(TypeCommunication, on_delete=models.CASCADE, null=True)
    nom = models.CharField(max_length=100, unique=True, null=True)
    modele = models.CharField(max_length=100, unique=True)
    fabricant = models.ForeignKey(FabricantsAppareils, on_delete=models.CASCADE)
    calibration = models.DateField(default=date.today, blank=True)
    duree_calibration = models.IntegerField(null=True)
    prochaine = models.DateField(blank=True, null=True)
    bloque_calibration = models.BooleanField(default=True)
    is_activate = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Calculate `prochaine` by adding `duree_calibration` to `calibration`
        if self.calibration and self.duree_calibration:
            # Multiply duree_calibration by 30 to get an approximate number of days in these months
            self.prochaine = self.calibration + timedelta(days=self.duree_calibration * 30)

        super().save(*args, **kwargs)
    class Meta:
        ordering = ['modele']

    def __str__(self):
        return self.modele

class InstructionsAppareils(models.Model):
    action = models.CharField(max_length=100,null=True, blank=True)
    modele_appareil = models.ForeignKey(Appareils, on_delete=models.CASCADE, null=True)
    nom = models.CharField(max_length=100, unique=True)
    instruction = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100,null=True, blank=True)
    button = models.BooleanField(default=False)
    format_reponse = models.CharField(max_length=100, null=True)
    class Meta:
        ordering = ['nom']

    def __str__(self):
        return self.nom

class ReponseInstructions(models.Model):
    num_instruction = models.ForeignKey(InstructionsAppareils, on_delete=models.CASCADE, null=True)
    nom = models.CharField(max_length=200)
    format = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    erreur = models.BooleanField(default=False)

    def __str__(self):
        return self.nom

class Supplier(models.Model):

    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=100, blank=True)
    postal = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    site = models.URLField(max_length=200, blank=True)
    user_code = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=True)
    logo = models.ImageField(upload_to='suppliers/', default='suppliers/usine.png')
    is_activate = models.BooleanField(default=True)
    download_catalogue = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('fiche', args=[str(self.id)])

    def __str__(self):
        return self.name

class CategorieMatiere(models.Model):
    nom = models.CharField(max_length=200)
    fournisseur = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    class Meta:
        ordering = ['nom']
    def __str__(self):
        return self.nom

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    nom = models.CharField(max_length=200, null=True)
    resettable = models.BooleanField(default=True)
    def __str__(self):
        return str(self.nom)

class TypeMatiere(models.Model):
    nom = models.CharField(max_length=200)

    def __str__(self):
        return self.nom

class UniteMesure(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Conditionnement(models.Model):
    nom = models.CharField(max_length=100)

class Forme(models.Model):
    nom = models.CharField(max_length=200)
    unite_mesure = models.ForeignKey(UniteMesure, on_delete=models.CASCADE, related_name='formes_mesure')
    unite_stock = models.ForeignKey(UniteMesure, on_delete=models.CASCADE, related_name='formes_stock')

    def __str__(self):
        return self.nom

class Liste(models.Model):
    nom = models.CharField(max_length=200)

    def __str__(self):
        return self.nom

class Voie(models.Model):
    nom = models.CharField(max_length=200)

    def __str__(self):
        return self.nom

class TypePrep(models.Model):
    nom = models.CharField(max_length=200)

    def __str__(self):
        return self.nom

class ParametresPrep(models.Model):
    nom = models.CharField(max_length=200)
    unite = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.nom} - {self.unite}"

class ParametresDemandes(models.Model):
    num_demande = models.IntegerField()
    parametre = models.ForeignKey(ParametresPrep, on_delete=models.CASCADE)
    valeur_parametre = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    resettable = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.num_demande} - {self.valeur_parametre}"

class ParametresFiches(models.Model):
    num_fiche = models.IntegerField()
    parametre = models.ForeignKey(ParametresPrep, on_delete=models.CASCADE)
    valeur_parametre = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    resettable = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.num_fiche} - {self.valeur_parametre}"

class ParametresFormules(models.Model):
    num_formule = models.IntegerField()
    parametre = models.ForeignKey(ParametresPrep, on_delete=models.CASCADE)
    unite = models.CharField(max_length=200, null=True)
    resettable = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.num_formule} - {self.parametre}"

    def __str__(self):
        return f"{self.num_formule} - {self.parametre}"

class Epi(models.Model):
    nom = models.CharField(max_length=200, null=True)
    def __str__(self):
        return f"{self.nom}"

class EpiFormules(models.Model):
    num_formule = models.IntegerField()
    epi = models.ForeignKey(Epi, on_delete=models.CASCADE)
    resettable = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.num_formule} - {self.epi}"

class MatierePremiere(models.Model):
    nom = models.CharField(max_length=200, null=True)
    categorie = models.ForeignKey(CategorieMatiere, on_delete=models.CASCADE, default=1, null=False)
    type = models.ForeignKey(TypeMatiere, on_delete=models.CASCADE, default=1, null=False)
    forme = models.ForeignKey(Forme, on_delete=models.CASCADE, null=True)
    cdt = models.ForeignKey(Conditionnement, on_delete=models.CASCADE, null=True)
    qté_cdt = models.DecimalField(max_digits=10, decimal_places=2)
    unite_cdt = models.CharField(max_length=200, null=True)
    fournisseur = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    code_fournisseur = models.CharField(max_length=200, null=True)
    ean = models.CharField(max_length=200, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    prix_unit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    qté_stock = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    stock_mini = models.PositiveIntegerField()
    liste = models.ForeignKey(Liste, on_delete=models.CASCADE, null=True)
    stockee = models.BooleanField(default=False)
    cde_auto = models.BooleanField(default=False)
    cde = models.BooleanField(default=False)
    attente_livraison = models.BooleanField(default=False)
    cmr = models.BooleanField(default=False)
    froid = models.BooleanField(default=False)
    unite_mesure = models.ForeignKey(UniteMesure, on_delete=models.CASCADE, null=True)
    tva = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    prix_ttc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    prix_unit_ttc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    densite = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    resettable = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.prix and self.qté_cdt and self.unite_cdt and self.unite_mesure and self.tva:
            try:
                # Convertissez la quantité du conditionnement à l'unité de mesure
                qté_unite_mesure = convert_quantity(
                    self.qté_cdt, self.unite_cdt.lower(), self.unite_mesure.nom
                )
                # Calculez le prix unitaire
                self.prix_unit = self.prix / qté_unite_mesure
                # Calculez le prix TTC
                self.prix_ttc = self.prix * (1 + self.tva / 100)
            except ValueError:
                # Gérez le cas où la conversion n'est pas possible
                self.prix_unit = None
                self.prix_ttc = None
        else:
            self.prix_unit = None
            self.prix_ttc = None

        if self.prix_unit and self.tva:
            try:
                # Calculez le prix unitaire TTC
                self.prix_unit_ttc = self.prix_unit * (1 + self.tva / 100)
            except ValueError:
                self.prix_unit_ttc = None
        else:
            self.prix_unit_ttc = None

        super(MatierePremiere, self).save(*args, **kwargs)
    class Meta:
        ordering = ['nom']

    def __str__(self):
        return self.nom

class ArticlesFormules(models.Model):
    num_formule = models.IntegerField()
    article = models.ForeignKey(MatierePremiere, on_delete=models.CASCADE)
    resettable = models.BooleanField(default=True)
    def __str__(self):
        return self.article.nom

class Etapes(models.Model):
    num = models.CharField(max_length=200, null=True)
    nom = models.CharField(max_length=200, null=False)
    description = models.TextField(max_length=500, null=False)
    resettable = models.BooleanField(default=True)

class TypeControle(models.Model):
    nom = models.CharField(max_length=100)
    type_appareil = models.ForeignKey(TypeAppareil, on_delete=models.CASCADE, null=True, blank=True)
    structure_formulaire = JSONField()
    def __str__(self):
        return self.nom

class Controles(models.Model):
    num_fiche = models.IntegerField(null=True)
    appareil = models.ForeignKey(Appareils, related_name='controles', on_delete=models.CASCADE, null=True)
    date_heure = models.DateTimeField(auto_now_add=True, null=True)
    controleur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    details = JSONField(null=True)
    remarques = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.type_controle.nom} sur {self.appareil.nom}"

class Formule(models.Model):
    nom = models.CharField(max_length=200, null=False)
    type = models.ForeignKey(TypePrep, on_delete=models.CASCADE, default=1, null=False)
    liste = models.ForeignKey(Liste, on_delete=models.CASCADE, default=1, null=False)
    voie = models.ForeignKey(Voie, on_delete=models.CASCADE, default=1, null=False)
    duree = models.CharField(max_length=200, null=False)
    froid = models.BooleanField(default=False)
    lumiere = models.BooleanField(default=False)
    agiter = models.BooleanField(default=False)
    mode_operatoire = models.CharField(max_length=1000, null=False)
    contre_indications = models.CharField(max_length=1000, null=False)
    publications = models.CharField(max_length=1000, null=True)
    is_activate = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=False)
    temps_preparation = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    temps_controle = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    prix_ht = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    prix_ttc = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    créateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='formules_createur')
    controleur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='formules_controleur')
    cloud = models.BooleanField(default=False)
    pediatric = models.BooleanField(default=False)
    hospitaliere = models.BooleanField(default=False)
    controles = JSONField(null=True, blank=True)
    resettable = models.BooleanField(default=True)

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return self.nom

class Composition(models.Model):
    num_formule = models.IntegerField(null=True)
    matiere = models.ForeignKey(MatierePremiere, on_delete=models.CASCADE, null=True)
    qté = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    calcul = models.CharField(max_length=200, null=True)
    type_appareil = models.ForeignKey(TypeAppareil, on_delete=models.CASCADE, null=True)
    resettable = models.BooleanField(default=True)

    def __str__(self):
        return str(self.num_formule)

class CompositionFiche(models.Model):
    num_fiche = models.IntegerField(null=True)
    matiere = models.ForeignKey(MatierePremiere, on_delete=models.CASCADE, null=True)
    qté = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ecart = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    resettable = models.BooleanField(default=True)

    def __str__(self):
        return str(self.num_formule)

class ParametresTarifs(models.Model):
    tarif_horaire_preparateur = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    tarif_horaire_pharmacien = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    tarif_controle = models.DecimalField(max_digits=10, decimal_places=2, null=True)

class CatalogueImport(models.Model):
    fournisseur = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    categorie = models.ForeignKey(CategorieMatiere, on_delete=models.CASCADE)
    page_debut = models.IntegerField()
    page_fin = models.IntegerField()
    code_debut = models.CharField(max_length=200)
    code_fin = models.CharField(max_length=200)
    date_import = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to='imports/')
    data_source = models.CharField(max_length=200, null=True)
    resettable = models.BooleanField(default=True)
    class Meta:
        ordering = ['date_import']
    def __str__(self):
        return str(self.date_import)

class Catalogue(models.Model):
    designation = models.CharField(max_length=200)
    code_fournisseur = models.CharField(max_length=200)
    cip = models.CharField(max_length=200)
    fournisseur = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    qté = models.DecimalField(max_digits=10, decimal_places=2)
    unite = models.CharField(max_length=200)
    prix = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    type = models.ForeignKey(TypeMatiere, on_delete=models.CASCADE, null=True)
    cmr = models.BooleanField(default=False)
    froid = models.BooleanField(default=False)
    categorie = models.ForeignKey(CategorieMatiere, on_delete=models.CASCADE, null=True)
    resettable = models.BooleanField(default=True)

    class Meta:
        ordering = ['designation']

    def __str__(self):
        return self.designation

class Demandes(models.Model):
    date_demande = models.DateField(default=date.today, blank=True)
    typePrep = models.ForeignKey(TypePrep, on_delete=models.CASCADE, null=True)
    prep = models.ForeignKey(Formule, on_delete=models.CASCADE, null=True)
    patient = models.CharField(max_length=200, null=True)
    age = models.IntegerField(null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    date_prevu = models.DateField(default=date.today, blank=True)
    prescripteur = models.CharField(max_length=200, null=True)
    commentaire = models.CharField(max_length=200, null=True)
    production = models.BooleanField(default=False)
    recurence = models.IntegerField(null=True, blank=True)
    delai = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.prep} - {self.date_prevu}"

class Fiches(models.Model):
    patient = models.CharField(max_length=200, null=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    typePrep = models.ForeignKey(TypePrep, on_delete=models.CASCADE, null=True)
    prep = models.ForeignKey(Formule, on_delete=models.CASCADE, null=True)
    prescripteur = models.CharField(max_length=200, null=True)
    attente_controle = models.BooleanField(default=True)
    controle_valide = models.BooleanField(default=False)
    destruction = models.BooleanField(default=False)
    date_fab = models.DateField(default=date.today, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    qté = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    preparateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='fiches_preparateur')
    controleur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='fiches_controleur')
    resettable = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        parametre_fiche = ParametresFiches.objects.filter(
            num_fiche=self.id,
            parametre__nom__startswith="Nb"
        ).first()

        if parametre_fiche:
            self.qté = parametre_fiche.valeur_parametre

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.prep)

class Reception(models.Model):
    date_reception = models.DateField(default=date.today, blank=True)
    matiere = models.ForeignKey(MatierePremiere, on_delete=models.CASCADE, null=True)
    lot = models.CharField(max_length=200, null=True)
    peremption = models.DateField(blank=True)
    certificat = models.FileField(upload_to='certificats/', null=True)
    qte = models.PositiveIntegerField(null=True, blank=True)
    stock_reception = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    echantillon = models.BooleanField(default=False)
    qte_echantillon = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    resettable = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        created = not self.pk
        old = Reception.objects.get(pk=self.pk) if self.pk else None

        if created:
            self.stock_reception = self.get_default_stock()
            if self.qte_echantillon:
                self.stock_reception -= self.qte_echantillon

        super().save(*args, **kwargs)

        if created:
            self.update_matiere_stock(created=True)

        elif old and old.qte_echantillon != self.qte_echantillon:
            with transaction.atomic():
                self.stock_reception -= self.qte_echantillon
                self.save()
                self.update_matiere_stock(created=False)

    def get_default_stock(self):
        if self.qte and self.matiere:
            converted_quantity = convert_quantity(self.qte, self.matiere.unite_cdt, self.matiere.unite_mesure.nom)
            return converted_quantity*self.matiere.qté_cdt
        return 0

    def update_matiere_stock(self, created):
        if self.matiere:
            with transaction.atomic():
                matiere = MatierePremiere.objects.select_for_update().get(pk=self.matiere.pk)
                if created:
                    matiere.qté_stock += self.stock_reception
                else:
                    matiere.qté_stock -= self.qte_echantillon
                matiere.attente_livraison = False
                matiere.save()

