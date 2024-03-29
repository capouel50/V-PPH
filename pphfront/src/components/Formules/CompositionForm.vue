<template>
  <div class="row">
        <q-list bordered class="col-11" v-if="rows.length > 0">
          <q-item v-for="(row, index) in rows" :key="index" class="row">
            <q-item-section>
              <q-select
                :label="row.matiere ? 'Matiere premiere n°' + (index + 1) : 'Ajouter une matière première'"
                v-model="row.matiere"
                color="cyan-4"
                class="hover-effect"
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
            </q-item-section>
            <q-item-section class="col-1">
              <q-input
                v-model="row.qté"
                color="cyan-4"
                class="hover-effect text-center"
                label="Quantité"
              >
                <template v-slot:append>
                  <div class="text-cyan-4 text-subtitle2 q-pt-md" v-if=" typeof row.matiere ==='string'">{{ row.unite_mesure }}</div>
                  <div class="text-cyan-4 text-subtitle2 q-pt-md" v-else>{{ row.matiere.unite }}</div>
                </template>
              </q-input>
            </q-item-section>
            <q-item-section class="col-4">
              <q-input
                  readonly
                  v-model="row.calcul"
                  :label="row.calcul ? 'Calcul appliqué' : 'Ajouter un calcul'"
                  color="cyan-4"
                  class="hover-effect text-center"
              >
                <template v-slot:prepend>
                  <q-avatar>
                    <q-btn flat size="md" @click="openCalculDialog(index)" icon="calculate" color="purple-4" class="hover-effect"
                    >
                      <q-tooltip>Ajouter ou modifier le calcul</q-tooltip>
                    </q-btn>
                  </q-avatar>
                </template>
              </q-input>
              <q-dialog v-model="calculDialog">
      <q-card>
        <q-card-section>
          <div v-if="typeof currentRow.matiere === 'string'" class="row text-subtitle1 text-cyan-4 justify-center">
            Calcul pour {{ currentRow.matiere }}
          </div>
          <div  v-else class="row text-subtitle1 text-cyan-4 justify-center">
            Calcul pour {{ currentRow.matiere.nom }} {{currentRow.matiere.qté_cdt}}{{currentRow.matiere.unite_cdt}} - {{currentRow.matiere.forme.nom}} - {{currentRow.matiere.fournisseur.name}}
          </div>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row text-orange-4 text-subtitle2 justify-center">Paramètres de calcul</div>
          <q-card-actions>
            <div class="row justify-center">
            <div v-for="(parametre, index) in parametresRows" :key="index">
              <q-btn
                flat
                color="cyan-4"
                class="hover-effect"
                :label="`${parametre.parametre.nom} - ${parametre.parametre.unite}`"
                @Click="inputParametre(`${parametre.parametre.nom} - ${parametre.parametre.unite}`, indexRow)"
              />
            </div>
              <q-btn v-if="!formuleId"
                flat
                color="cyan-4"
                class="hover-effect"
                :label="'Quantité - ' + (currentRow?.matiere?.unite_mesure?.nom || 'Unité inconnue')"
                @click="inputParametre('Quantité - ' + (currentRow?.matiere?.unite_mesure?.nom || ''), indexRow)"
              />
              <q-btn v-else
                flat
                color="cyan-4"
                class="hover-effect"
                :label="'Quantité - ' + (currentRow?.unite_mesure || 'Unité inconnue')"
                @click="inputParametre('Quantité - ' + (currentRow?.unite_mesure || ''), indexRow)"
              />
            </div>
          </q-card-actions>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row">
            <div class="col-12">
              <q-input
              v-model="currentRow.calcul"
              color="cyan-4"
              :label="response && currentRow.calcul ? 'Calcul généré par V-PPH' : 'Entrez le calcul a appliquer'"
          >
            <template v-slot:prepend>
              <q-btn  v-if="!ask" flat class="q-ma-none hover-effect fade-blink" color="purple-4" label="V-PPH" size="sm" @click.stop="gptCalculate(indexRow)"/>
              <div v-if="ask && !response" class="q-pr-sm q-pl-md">
                <atom-spinner
                class="bg-op-8"
                :animation-duration="1000"
                :size="25"
                :color="'#ff1d5e'"
              />
              </div>
            </template>
          </q-input>
            </div>
          </div>
          <div class="row justify-center">
            <div class="col-8">
              <q-input
              v-if="response"
              v-model="question"
              label="Effectuer une demande"
              @keyup.enter="gptCalculate(indexRow)"
            >
            <template v-slot:append>
              <q-btn
              flat
              color="purple-4"
              class="hover-effect-success"
              size="md"
              icon="send"
              @click="gptCalculate(indexRow)"
            />
            </template>
          </q-input>
            </div>
          </div>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row justify-center">
          <q-btn-group>
          <q-btn
            flat
            color="green-4"
            label="Valider"
            @click="validerCalcul(indexRow)"
          />
          <q-btn
            flat
            class="hover-effect"
            color="cyan-4"
            label="Effacer"
            @click="effacerCalcul(indexRow)"
          />
          <q-btn
            flat
            color="red-4"
            label="Annuler"
            @click="annulerCalcul"
          />
          </q-btn-group>
          </div>
        </q-card-section>
      </q-card>
      </q-dialog>
            </q-item-section>
            <q-item-section class="col-2">
              <q-select
                label="Appareil de mesure"
                v-model="row.type_appareil"
                color="cyan-4"
                class="hover-effect"
                :options="typesAppareils"
                option-label="nom"
                option-value="id"
              />
            </q-item-section>
            <q-item-section side>
              <q-btn flat size="md" @click="removeLine(index)" icon="delete_forever" color="red-4"/>
            </q-item-section>
          </q-item>
        </q-list>
          <q-btn flat size="md" @click="addLine" icon="add_box" color="cyan-4" class="hover-effect q-px-xs" :label="rows.length > 0 ? '' : 'Ajouter'"/>
          <q-btn v-if="rows.length > 0" flat size="md" @click="validRows" icon="check_circle" color="green-4" class="q-px-xs"/>
      </div>

</template>

<script>
import { mapActions, mapGetters, mapState, mapMutations } from 'vuex';
import {AtomSpinner} from 'epic-spinners'
export default {
  components: {
    AtomSpinner
  },
  props: ['newId', 'formuleId', 'typesAppareils', 'compoRows', 'parametresRows', 'name', 'prep'],
  data() {
    return {
      calculDialog: false,
      selectedRowIndex: null,
      calculDetails: [],
      matieres: [],
      rows: [],
      currentRow: [],
      indexRow: '',
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
      question: '',
      context: '',
      ask: false,
    };
  },
  computed: {
    ...mapGetters('matieresPremieres', ['allMatieres', 'allUnites']),
    ...mapGetters('formules', ['allParametres', 'allParametresFormules']),
    ...mapGetters('appareils', ['allTypes']),
    ...mapState('chatGPT', ['response']),

  },

  async created() {
    this.newChat();
    this.question = '';
    console.log('compoRows', this.compoRows);
      this.matieres = this.allMatieres.map(matiere => ({
        ...matiere,
        label: `${matiere.nom} ${matiere.qté_cdt}${matiere.unite_cdt} - ${matiere.forme.nom} - ${matiere.fournisseur.name}`,
        id: matiere.id,
        unite: matiere.unite_mesure.nom,
        cmr: matiere.cmr,
      }));
      if(this.formuleId) {
        this.rows = this.compoRows.map(compo => ({
          num_formule: this.formuleId,
          matiere: `${compo.matiere.nom} ${compo.matiere.qté_cdt}${compo.matiere.unite_cdt} - ${compo.matiere.forme.nom} - ${compo.matiere.fournisseur.name}`,
          qté: compo.qté,
          calcul: compo.calcul,
          calculInput: '',
          type_appareil: compo.type_appareil.nom,
          unite_mesure: compo.matiere.unite_mesure.nom,
          matiereId: compo.matiere.id
        }));
      }
    },

  methods: {
    ...mapActions('matieresPremieres', ['loadMatieresPremieres', 'loadUnites']),
    ...mapActions('formules', ['addComposition']),
    ...mapActions('formules', ['loadParametres', 'loadParametresFormules']),
    ...mapActions('notifications', ['showNotification']),
    ...mapActions('chatGPT', ['askQuestion', 'newChat']),
    ...mapMutations('chatGPT', ['deleteResponse']),

    async gptCalculate(indexRow) {
      this.currentRow.calcul = 'Analyse de la demande en cours...';
      const params = this.parametresRows.map(row => `${row.parametre.nom} - ${row.parametre.unite}`);
      const verification = 'Avant de traiter cette demande, vérifie bien les données que tu possèdes ou que tu trouves sur internet. '
      const matieresString = this.compoRows.map(compoRow => `${compoRow.matiere.nom} ${compoRow.matiere.forme.nom}`).join(', ');
      const message =
          'Pour une ' + this.prep + ' de ' + this.name + ' dont les composants sont ' + matieresString +
          ' donne moi le calcul qui sera utilisé pour mesurer la quantité de ' + this.rows[indexRow].matiere +
          ' sachant que les parametres de calcul disponibles sont '
      let restriction = '. Ces paramètres sont fournis sous le format: paramètre - unité. ' +
          'Ta réponse doit uniquement comporter le calcul litéral effectué à l\'aide des paramètres (et leur unité), en respectant le format des paramètres fournis.' +
          'Tu as le droit d\'utiliser des nombres et de faire autant d\'opérations que tu veux. ' +
          'Fait bien attention aux unités des paramètres pour générer ton calcul.' +
          'Exemple: (parametre1 + parametre2)/parametre1. ' +
          'La valeur de chaque paramètre sera fourni par l\'utilisateur plus tard, lors de la préparation, elle remplacera les paramètres pour calculer les quantités, c\'est pourquoi tu dois fournir uniquement le calcul littéral et ne mettre aucune égalité.' +
          'Je tiens absolument a ce que ta réponse ne contienne que le calcul littéral, tu n\'as pas le droit de faire de phrases, c\'est très important, sauf si tu as un doute, que tu constate une incohérence, ta réponse sera: '
      let error = 'Erreur: (explique ici en 10 mots maximum d\'où vient l\'erreur)'
      this.context = verification + message + params + restriction + error;
      if (this.question.trim()) {
        this.question = this.question + restriction + error;
        await this.askQuestion(this.question);
        this.question='';
      }else{
        this.ask = true;
        await this.askQuestion(this.context);
        this.ask = false;
      }
      this.currentRow.calcul = this.response;
    },

    updateControlesRows() {
      this.$emit('compoRows', this.rows);
      console.log('rows', this.rows);
      console.log('comporows', this.compoRows);
    },

    validRows(){
      this.updateControlesRows();
      this.showNotification({message: 'Composition ajoutée', type: 'success'});
    },

    addLine() {
      this.updateControlesRows();
      this.rows.push({
        num_formule: this.formuleId ? this.formuleId : this.newId,
        matiere: '',
        qté: '',
        calcul: '',
        type_appareil: '',
      });
      console.log('rows', this.rows);
    },
    removeLine(index) {
      this.rows.splice(index, 1);
      this.updateControlesRows();
    },

    openCalculDialog(index) {
      this.currentRow = this.rows[index];
      this.calculDialog = true;
      this.indexRow = index;
    },

    validerCalcul(indexRow) {
      this.rows[indexRow].calcul = this.currentRow.calcul;
      this.newChat();
      this.deleteResponse();
      this.calculDialog = false;
    },

    annulerCalcul() {
      this.newChat();
      this.deleteResponse();
      this.calculDialog = false;
    },

    inputParametre(parametre, indexRow) {
      this.currentRow.calcul += parametre;
      this.rows[indexRow].calcul = this.currentRow.calcul;
    },

    effacerCalcul(indexRow) {
      this.currentRow.calcul = " ";
      this.deleteResponse();
      this.rows[indexRow].calcul = this.currentRow.calcul;
    },

    async submitForm() {
      // Récupérez les données de toutes les lignes
      const formData = {
        compositions: this.rows.map(row => ({
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


