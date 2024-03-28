<template>
  <q-form @submit.prevent="submitForm">
    <div
      v-for="(row, index) in formRows"
      :key="index"
      class="row"
    >
      <q-select
        label="Matière première"
        v-model="row.matiere"
        color="cyan-4"
        class="col-4 hover-effect q-mr-md"
        :options="matieres"
        option-label="label"
        option-value="id"
      >
        <template v-slot:option="scope">
          <q-item
            v-bind="scope.itemProps"
            v-on="scope.itemEvents"
          >
            <q-item-section>{{ scope.opt.label }}</q-item-section>
            <q-item-section side>
              <q-img v-if="scope.opt.cmr" class="q-ml-xs fade-blink" src="@/assets/img/health_hazard.png" :style="{ width: '20px', height: '20px' }"/>
            </q-item-section>
          </q-item>
        </template>
      </q-select>
      <q-input
        v-model="row.qté"
        color="cyan-4"
        class="col-1 hover-effect text-center q-mr-md"
        label="Quantité"
      >
        <template v-slot:append>
          <div class="text-cyan-4 text-subtitle2" v-if="row.matiere">{{ row.matiere.unite }}</div>
        </template>
      </q-input>
      <q-input
          readonly
          label="Calcul appliqué"
          v-model="row.calculInput"
          color="cyan-4"
          class="col-3 hover-effect text-center q-mr-md"
      >
        <template v-slot:prepend>
          <q-avatar>
            <q-btn flat size="md" @click="openCalculDialog(index)" icon="calculate" color="cyan-4" class="hover-effect"/>
          </q-avatar>
        </template>
      </q-input>
      <q-select
        label="Appareil de mesure"
        v-model="row.type_appareil"
        color="cyan-4"
        class="col-2 hover-effect q-mr-md"
        :options="TypesAppareils"
        option-label="nom"
        option-value="id"
      />
      <q-btn-group flat class="q-ml-lg">
        <q-btn flat size="sm" @click="addRow" icon="add_box" color="green-4" class="hover-effect-success"/>
        <q-btn flat size="sm" @click="removeRow" icon="delete_forever" color="red-4" class="hover-effect-warning"/>
      </q-btn-group>
      <q-dialog v-model="calculDialog">
      <q-card>
        <q-card-section>
          <div class="row text-subtitle1 text-cyan-4 justify-center">
            Calcul pour {{ formRows[selectedRowIndex].matiere.nom }}
          </div>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row text-orange-4 text-subtitle2 justify-center">Paramètres de calcul</div>
          <q-card-actions>
            <div class="row justify-center">
            <div v-for="(parametre, index) in filteredParametresFormules" :key="index">
              <q-btn
                flat
                color="cyan-4"
                class="hover-effect"
                :label="parametre.label"
                @Click="inputParametre(parametre)"
              />
            </div>
              <q-btn
                flat
                color="cyan-4"
                class="hover-effect"
                :label="'Quantité - ' + (formRows[selectedRowIndex]?.matiere?.unite_mesure?.nom || 'Unité inconnue')"
                @click="inputParametre('Quantité - ' + (formRows[selectedRowIndex]?.matiere?.unite_mesure?.nom || ''))"
              >
              </q-btn>
            </div>
          </q-card-actions>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <q-input
              v-model="row.calcul"
              color="cyan-4"
              label="Entrez le calcul a appliquer"
          />
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row justify-center">
          <q-btn-group>
          <q-btn
            flat
            color="green-4"
            label="Valider"
            @click="validerCalcul"
          />
          <q-btn
            flat
            class="hover-effect"
            color="cyan-4"
            label="Effacer"
            @click="effacerCalcul"
          />
          <q-btn
            flat
            color="red-4"
            label="Annuler"
            @click="calculDialog = false"
          />
          </q-btn-group>
          </div>
        </q-card-section>
      </q-card>
      </q-dialog>
    </div>

    <div class="row">
      <div class="col-4">
        <q-btn flat @click="submitForm" color="green-4" class="q-mt-xs btn-flat-success-pph">
          Valider
        </q-btn>
      </div>
    </div>
  </q-form>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import api from '../../../api';

export default {
  props: ['newId', 'formuleId', 'typesAppareils', 'compoRows', 'parametresRows'],
  data() {
    return {
      calculDialog: false,
      enregistrements: [],
      selectedRowIndex: null,
      calculDetails: [],
      matieres: [],
      formRows: [
        {
          num_formule: null,
          matiere: null,
          qté: null,
          calcul: '',
          calculInput: '',
          type_appareil: null,
        }
      ],
    };
  },
  computed: {
    ...mapGetters('matieresPremieres', ['allMatieres', 'allUnites']),
    ...mapGetters('formules', ['allParametres', 'allParametresFormules']),

    paramestreFormules

    filteredParametresFormules() {
      if (this.selectedRowIndex !== null) {
        const numFormule = this.formRows[this.selectedRowIndex].num_formule;
        const allParametresDetails = this.allParametres; // Assurez-vous que ceci contient les détails complets des paramètres
        console.log('allparametres', this.allParametres);
        return this.allParametresFormules
          .filter(pf => pf.num_formule.toString() === numFormule.toString())
          .map(pf => {
            const parametreDetail = allParametresDetails.find(p => p.id === pf.parametre.id);
            return {
              ...pf,
              label: parametreDetail ? `${parametreDetail.nom} - ${parametreDetail.unite}` : 'Inconnu',
              id: pf.parametre.id
            };
          });
      }
      return [];
    },
  },

  async created() {
      await this.createNewNumCompo();
      this.matieres = this.allMatieres.map(matiere => ({
        ...matiere,
        label: `${matiere.nom} ${matiere.qté_cdt}${matiere.unite_cdt} - ${matiere.forme.nom} - ${matiere.fournisseur.name}`,
        id: `${matiere.id}`,
        unite: `${matiere.unite_mesure.nom}`,
        cmr: matiere.cmr,
      }));
    },

  methods: {
    ...mapActions('matieresPremieres', ['loadMatieresPremieres', 'loadUnites']),
    ...mapActions('formules', ['addComposition']),
    ...mapActions('formules', ['loadParametres', 'loadParametresFormules']),

    validerCalcul() {
      if (this.selectedRowIndex !== null) {
        this.formRows[this.selectedRowIndex].calculInput = this.formRows[this.selectedRowIndex].calcul;
        let calculTransforme = this.formRows[this.selectedRowIndex].calcul;

        // Remplacer chaque label par son ID correspondant, sauf pour les cas spéciaux
        //this.calculDetails.forEach(detail => {
          //if (detail.id !== null) {
            //const regex = new RegExp(detail.label, 'g');
            //calculTransforme = calculTransforme.replace(regex, detail.id);
          //} else {
            // Pour les cas spéciaux comme "Quantité - Unité", vous pouvez choisir de les laisser tels quels,
            // les remplacer par une valeur spécifique, ou effectuer une autre transformation.
            // Exemple : Remplacer par une chaîne spéciale ou laisser tel quel
            //const specialValue = "Qte"; // Définir une valeur spéciale si nécessaire
            //calculTransforme = calculTransforme.replace(new RegExp(detail.label, 'g'), specialValue);
          //}
        //});

        // Mettre à jour le calcul dans formRows
        this.formRows[this.selectedRowIndex].calcul = calculTransforme;


        // Réinitialiser les détails du calcul et fermer le dialogue
        this.calculDetails = [];
        this.calculDialog = false;
      }
    },


    openCalculDialog(rowIndex) {
      this.selectedRowIndex = rowIndex;
      this.calculDialog = true;
      if (this.formRows[this.selectedRowIndex].calculInput){
        this.formRows[this.selectedRowIndex].calcul = this.formRows[this.selectedRowIndex].calculInput
      }
    },

    inputParametre(parametre) {
      console.log("Paramètre reçu :", parametre);

      if (this.selectedRowIndex !== null && this.formRows[this.selectedRowIndex]) {
        let label, id;

        if (typeof parametre === 'string') {
          // Cas où parametre est une chaîne de caractères (par exemple, "Quantité - Unité")
          label = parametre;
          id = null;  // Il n'y a pas d'ID spécifique pour "Quantité - Unité"
        } else {
          // Cas où parametre est un objet (paramètres habituels)
          label = parametre.label;
          id = parametre.id;
        }

        // Ajouter le label au calcul
        this.formRows[this.selectedRowIndex].calcul += label;

        // Ajouter les détails du paramètre ou de la chaîne pour le remplacement ultérieur
        this.calculDetails.push({
          label: label,
          id: id
        });
      }
    },


    effacerCalcul() {
      this.formRows[this.selectedRowIndex].calcul = " ";
    },

    removeRow(row) {
      // Supprime la ligne qui contient le bouton
      const index = this.formRows.indexOf(row);
      this.formRows.splice(index, 1);
    },

    async createNewNumCompo() {
      try {
        if (this.formRows.length === 0 || this.formRows[0].num_formule === null) {
          this.formRows[0].num_formule = this.newId;
        }
      } catch (error) {
        console.error('Erreur lors de la récupération du dernier ID de la formule', error);
      }
    },

    async loadRecords() {
      try {
        // Assurez-vous que le dernier numéro de formule est chargé
        const dernierNumFormule = await this.createNewNumCompo();

        // Faites l'appel API en passant le dernier numéro de formule
        const response = await api.get(`/PPH/composition/filter/${dernierNumFormule}`);
        this.enregistrements = response.data;
        console.log('Enregistrements chargés:', this.enregistrements);
      } catch (error) {
        console.error('Erreur lors du chargement des enregistrements:', error);
        // Gérer l'erreur comme il convient
      }
    },

    async updateFilteredRecords() {
      const NumFormule = await this.createNewNumCompo(); // Assurez-vous que cette méthode renvoie le dernier numéro

      const enregistrementsFiltres = this.enregistrements.filter(enregistrement => {
        return enregistrement.num_formule === NumFormule;
      });

      if (enregistrementsFiltres.length === 0) {
        // S'il n'y a pas d'enregistrements correspondants, exécutez addRow()
        this.addRow();
      } else {
        // Sinon, mettez à jour formRows avec les enregistrements filtrés
        this.formRows = enregistrementsFiltres.map(enregistrement => {
          return {
            num_formule: enregistrement.num_formule,
            matiere: enregistrement.matiere,
            qté: enregistrement.qté,
            calcul: enregistrement.calcul,
            type_appareil: enregistrement.type_appareil
            // ... autres propriétés nécessaires
          };
        });
      }
    },

    async addRow() {
      try {
        this.formRows.push({
          num_formule: this.newId,
          matiere: null,
          qté: '',
          calcul: '',
          type_appareil: '',
        });
      } catch (error) {
        console.error('Erreur lors de la récupération du dernier ID du modèle Formule', error);
      }
    },

    async submitForm() {
      // Récupérez les données de toutes les lignes
      const formData = {
        compositions: this.formRows.map(row => ({
          num_formule: row.num_formule,
          matiere: row.matiere.id,
          qté: row.qté,
          calcul: row.calcul,
          type_apparel: row.type_appareil.id
        })),
      };

      // Appelez votre action Vuex pour ajouter les compositions
      this.addComposition(formData);
    },
  },
};
</script>


