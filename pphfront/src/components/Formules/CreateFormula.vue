<template>
  <q-page v-if="loading">
  <div class="q-pa-md">
    <q-stepper
      v-model="step"
      class="bg-op-8"
      vertical
      done-color="cyan-4"
      active-color="orange-4"
      header-nav
      animated
    >
      <div v-if="formuleId" class="text-h5 text-center text-cyan-4">{{ formule.nom }}</div>
      <div v-else class="text-h5 text-center text-cyan-4">Nouvelle Formule</div>
       <q-step
        :name="1"
        title="Identification"
        icon="info"
        :done="step > 1"
      >
        <div class="row">
          <q-input
            ref="nomInput"
            class="q-mr-lg col-3"
            v-model="name"
            label="Nom de la formule"
            color ='cyan-4'
            @mouseover="changeLabelColor('nameInput','#ffb74d')"
            @mouseleave="changeLabelColor('nameInput','')"
            @focus="onFocus('name','#4dd0e1')"
            @blur="onBlur('name')"
        >
          <template v-slot:prepend>
            <q-icon name="local_pharmacy" color="cyan-4"/>
          </template>
        </q-input>

          <q-select
            v-model="typePrep"
            color="cyan-4"
            class="col-3 hover-effect"
            label="Type de préparation"
            :options="typesPrep"
            option-label="nom"
            option-value="id"
          >
            <template v-slot:prepend>
              <q-icon name="local_pharmacy" color="cyan-4"/>
            </template>
          </q-select>
        </div>
        <div class="row">
          <q-select
            v-model="liste"
            color="cyan-4"
            class="col-2 hover-effect"
            label="Liste"
            :options="listes"
            option-label="nom"
            option-value="id"
          >
            <template v-slot:prepend>
              <q-icon name="gavel" color="cyan-4"/>
            </template>
          </q-select>
        </div>
         <div class="row">
            <q-toggle
                class="col-2 q-mt-sm"
                v-model="hospital"
                label="Préparation hospitalière"
                size="md"
                color="purple-4"
                icon="account_child"
            />
            <q-toggle
                class="col-2 offset-1 q-mt-sm"
                v-model="pediatric"
                label="Formule pédiatrique"
                size="md"
                color="red-4"
                icon="account_child"
            />
          </div>
        <q-stepper-navigation>
          <q-btn flat @click="step = 2" color="cyan-4" label="Suivant" class="hover-effect" />
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="2"
        title="Voie d'administration"
        icon="vaccines"
        :done="step > 2"
      >
      <div class="row">
        <q-select
        v-model="voie"
        color="cyan-4"
        class="col-3 hover-effect"
        label="Sélectionnez la voie"
        :options="voies"
        option-label="nom"
        option-value="id"
      >
        <template v-slot:prepend>
          <q-icon name="vaccines" color="cyan-4"/>
        </template>
        </q-select>
      </div>

      <q-stepper-navigation>
          <q-btn flat @click="step = 1" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
        <q-btn flat @click="step = 3" color="cyan-4" label="Suivant" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="3"
        title="Conservation"
        icon="ac_unit"
        :done="step > 3"
      >

      <div class="row">
      <q-input
        ref="dureeInput"
        class="my-0 col-1"
        v-model="duree"
        label="Durée (j)"
        color ='cyan-4'
        @mouseover="changeLabelColor('nameInput','#ffb74d')"
        @mouseleave="changeLabelColor('nameInput','')"
        @focus="onFocus('name','#4dd0e1')"
        @blur="onBlur('name')"
      >
        <template v-slot:before>
          <q-icon name="alarm" color="cyan-4"/>
        </template>
      </q-input>
      </div>
      <div class="q-pa-md q-gutter-sm">
        <div>
          <q-toggle
            v-model="froid"
            color="cyan-4"
            icon="ac_unit"
            label="4°C - 8°C"
            size="md"
          />
          <q-toggle
             v-model="lumiere"
             color="yellow-4"
             icon="light_mode"
             label="Abris de la lumiere"
             size="md"
          />
          <q-toggle
             v-model="agiter"
             color="red-4"
             icon="waving_hand"
             label="Agiter avant emploi"
             size="md"
          />
         </div>
      </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 2" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          <q-btn flat @click="step = 4" color="cyan-4" label="Suivant" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="4"
        title="Matériel"
        icon="biotech"
        :done="step > 4"
      >
        <ArticlesForm v-if="step === 4" :newId="newId" :formuleId="formuleId" @articlesRows="rowsArticles" :articlesRows="articlesRows"/>

        <q-stepper-navigation>
          <q-btn flat @click="step = 3" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          <q-btn flat @click="step = 5" color="cyan-4" label="Suivant" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="5"
        title="Paramètres"
        icon="settings"
        :done="step > 5"
      >

        <ParametresForm v-if="step === 5" :newId="newId" :formuleId="formuleId" @parametresRows="rowsParametres" :parametresRows="parametresRows"/>

        <q-stepper-navigation>
          <q-btn flat @click="step = 4" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          <q-btn flat @click="step = 6" color="cyan-4" label="Suivant" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="6"
        title="Composition"
        icon="science"
        :done="step > 6"
      >
        <div class="row">
          <div class="col-12">
            <CompositionForm
                :newId="newId"
                :formuleId="formuleId"
                :typesAppareils="typesAppareils"
                :parametresRows="parametresRows"
                :name="name"
                :prep="typePrep"
                :compoRows="compoRows"
                @compoRows="rowsCompo"
            />
          </div>
        </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 5" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          <q-btn flat @click="step = 7" color="cyan-4" label="Suivant" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="7"
        title="EPI"
        icon="masks"
        :done="step > 7"
      >
        <div class="row">
          <div class="col-8">
            <EpiForm v-if="step === 7" :newId="newId" :formuleId="formuleId" :episRows="episRows" @episRows="rowsEpis"/>
          </div>
        </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 6" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          <q-btn flat @click="step = 8" color="cyan-4" label="Suivant" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="8"
        title="Mode opératoire"
        icon="list_alt"
        :done="step > 8"
      >

        <div class="row">
          <div class="col-12">
            <EtapesForm
                v-if="step === 8"
                :newId="newId"
                :formuleId="formuleId"
                :name="name"
                :prep="typePrep"
                :compoRows="compoRows"
                @etapesRows="rowsEtapes"
                :etapesRows="etapesRows"/>
          </div>
        </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 7" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          <q-btn flat @click="step = 9" color="cyan-4" label="Suivant" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="9"
        title="Contrôles"
        icon="biotech"
        :done="step > 9"
      >
            <ControlesForm v-if="step === 9" :controlesRows="controleRows" @controleRows="rows"/>

        <q-stepper-navigation>
          <q-btn flat @click="step = 8" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          <q-btn flat @click="step = 10" color="cyan-4" label="Suivant" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="10"
        title="Contre-indications et précautions d'emploi"
        icon="warning"
        :done="step > 10"
      >
      <div class="row">
      <q-input
        ref="emploiInput"
        class="my-0 col-3"
        v-model="emploi"
        label="Entrez les informations"
        color ='cyan-4'
        autogrow
        @mouseover="changeLabelColor('nameInput','#ffb74d')"
        @mouseleave="changeLabelColor('nameInput','')"
        @focus="onFocus('name','#4dd0e1')"
        @blur="onBlur('name')"
      >
        <template v-slot:prepend>
          <q-icon name="info" color="cyan-4"/>
        </template>
      </q-input>
      </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 9"  color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          <q-btn flat @click="step = 11" color="cyan-4" label="Suivant" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="10"
        title="Publications"
        icon="article"
        :done="step > 11"
      >
      <div class="row">
        <q-input
        ref="publicationsInput"
        class="my-0 col-3"
        v-model="publications"
        label="Publications, données de stabilité..."
        color ='cyan-4'
        autogrow
        @mouseover="changeLabelColor('nameInput','#ffb74d')"
        @mouseleave="changeLabelColor('nameInput','')"
        @focus="onFocus('name','#4dd0e1')"
        @blur="onBlur('name')"
      >
        <template v-slot:prepend>
          <q-icon name="article" color="cyan-4"/>
        </template>
      </q-input>
      </div>
        <q-stepper-navigation>
          <q-btn flat @click="step = 10" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          <q-btn flat @click="step = 12" color="cyan-4" label="Suivant" class="hover-effect q-ml-sm" />
        </q-stepper-navigation>
      </q-step>

      <q-step
          :name="12"
          title="PPH cloud"
          icon="cloud"
          :done="step > 12"
        >
        <div class="row">
          <div class="col-2">
            <q-toggle
                v-model="cloud"
                :label="cloud ? 'Publique' : 'Privée'"
                size="md"
                color="green-4"
                icon="publish"
            />
          </div>
        </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 11" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          <q-btn flat @click="step = 13" color="cyan-4" label="Terminer" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>

      <div class="row justify-center">
        <q-btn-group>
          <q-btn flat @click="submitForm" color="green-4" label="Enregistrer" class="btn-flat-success-pph"/>
          <q-btn flat color="red-4" label="Supprimer" class="btn-flat-danger-pph"/>
        </q-btn-group>
      </div>
    </q-stepper>
  </div>
  </q-page>
  <q-page v-else class="row items-center justify-center">
  <div class=" row justify-center">
      <atom-spinner
        class="bg-op-8"
        :animation-duration="1000"
        :size="100"
        :color="'#ff1d5e'"
      />
      </div>
  </q-page>
</template>

<script>
import CompositionForm from './CompositionForm.vue';
import ParametresForm from './ParametresForm.vue';
import EpiForm from './EpiForm.vue';
import ArticlesForm from './ArticlesForm.vue';
import EtapesForm from './EtapesForm.vue';
import ControlesForm from './ControlesForm.vue';
import {mapActions, mapGetters} from "vuex";
import {AtomSpinner} from 'epic-spinners'

export default {
  components: {
    CompositionForm,
    ParametresForm,
    EpiForm,
    ArticlesForm,
    EtapesForm,
    ControlesForm,
    AtomSpinner,
  },
  data() {
    return {
      loading: false,
      step: 1,
      name: '',                // Pour le Nom de la formule
      typePrep: null,
      prep: '',// Pour le Type de préparation
      liste: null,             // Pour la Liste
      voie: null,              // Pour la Voie d'administration
      duree: '',               // Pour la Durée
      froid: false,            // Toggle pour Conservation au froid
      lumiere: false,          // Toggle pour Abris de la lumiere
      agiter: false,           // Toggle pour Agiter avant emploi
      modeOperatoire: '',      // Pour le Mode opératoire
      emploi: '',              // Pour les Contre-indications et précautions d'emploi
      publications: '',
      cloud: false,
      pediatric: false,
      hospital: false,
      specialite: false,
      newId: null,
      formuleId: null,
      formule:[],
      episRows: [],
      typesAppareils: [],
      controleRows: [],
      articlesRows: [],
      parametresRows: [],
      compoRows: [],
      etapesRows: [],
      typesPrep: [],
      listes: [],
      voies: [],
    };
  },

  computed: {
    ...mapGetters('formules', ['allFormules', 'allTypesPrep', 'allListes', 'allArticlesFormules',
                               "allParametresFormules", 'allParametres', 'allCompositions']),
    ...mapGetters('voiesAdministration', ['allVoies']),
    ...mapGetters('epi', ['allEpis', 'allEpisFormules']),
    ...mapGetters('appareils', ['allTypes']),
    ...mapGetters('etapes', ['allEtapes']),
    ...mapGetters('matieresPremieres', ['allMatieres']),

  },

  async created() {
    if(this.$route.params.id) {
      this.formuleId = Number(this.$route.params.id);
    }else{
      this.newId = this.allFormules.length + 1;
    }

    await Promise.all([
      this.loadFormules(),
      this.loadUnites(),
      this.loadVoies(),
      this.loadTypes(),
      this.loadListes(),
      this.loadTypesAppareils(),
      this.loadParametres(),
      this.loadMatieresPremieres(),
      this.loadEpis(),
      this.loadEtapes(),
    ]);
    this.typesAppareils = this.allTypes;
    this.typesPrep = this.allTypesPrep;
    this.listes = this.allListes;
    this.voies = this.allVoies;
    if(!this.formuleId){
      this.loading = true;
    }

    if(this.formuleId) {
      await Promise.all([
        this.loadArticlesFormules(),
        this.loadParametresFormules(),
        this.loadEpisFormules(),
        this.loadCompositions(),
      ]);
      this.formule = this.allFormules.find(formule => formule.id === this.formuleId);
      this.name = this.formule.nom;
      this.typePrep = this.formule.type.nom;
      this.liste = this.formule.liste.nom;
      this.voie = this.formule.voie.nom;
      this.duree = this.formule.duree;
      this.froid = this.formule.froid;
      this.lumiere = this.formule.lumiere;
      this.agiter = this.formule.agiter;
      this.modeOperatoire = this.formule.mode_operatoire;
      this.emploi = this.formule.contre_indications;
      this.publications = this.formule.publications;
      this.cloud = this.formule.cloud;
      this.pediatric = this.formule.pediatric;
      this.hospital = this.formule.hospitaliere;
      this.specialite = this.formule.specialite;
      this.episRows = this.allEpisFormules.filter(epi => epi.num_formule === this.formuleId);
      if(this.formule.controles) {
        this.controleRows = this.formule.controles;
      }else{
        this.controleRows = [];
      }
      this.articlesRows = this.allArticlesFormules.filter(article => article.num_formule === this.formuleId);
      this.parametresRows = this.allParametresFormules.filter(parametre => parametre.num_formule === this.formuleId);
      this.etapesRows = this.allEtapes.filter(etape => etape.num === 'f' + this.formuleId);
      this.compoRows = this.allCompositions.filter(compo => compo.num_formule === this.formuleId);
      this.loading = true;
    }
  },

  methods: {
    ...mapActions('formules', ['loadTypes','loadListes', 'addFormule', 'loadArticlesFormules', 'loadFormules', 'loadParametres', 'loadCompositions',
                               'addArticles', 'loadParametresFormules', 'addParametres', 'updateParametres', 'updateArticles', 'updateFormule']),
    ...mapActions('voiesAdministration', ['loadVoies']),
    ...mapActions('epi', ['loadEpis', 'loadEpisFormules', 'updateEpis', 'addEpis']),
    ...mapActions('appareils', ['loadTypesAppareils']),
    ...mapActions('etapes', ['loadEtapes']),
    ...mapActions('matieresPremieres', ['loadMatieresPremieres', 'loadUnites']),

    rowsArticles(articlesRows) {
      this.articlesRows = articlesRows;
    },
    rowsParametres(parametresRows) {
      this.parametresRows = parametresRows;
    },
    rowsEtapes(etapesRows) {
      this.etapesRows = etapesRows;
    },
    rowsEpis(episRows) {
      this.episRows = episRows;
    },
    rowsCompo(compoRows) {
      this.compoRows = compoRows;
    },
    rows(rows) {
      this.controleRows = rows;
    },

    async submitForm(){
      this.articlesRows.forEach(row => {
        row.article = row.article.id;
      });
      const formData = this.articlesRows;
      await this.updateArticles({formData, formuleId: Number(this.formuleId)});
      this.articlesRows.forEach(row => {
      const matchingArticle = this.allMatieres
          .filter(article => article.categorie.nom === "Matériel & Articles de conditionnement")
          .find(article => article.id === row.article);
      if (matchingArticle) {
        row.article = matchingArticle;
      }
    });

    },

    async submitForms() {
      const formData = {
        nom: this.name,
        type: this.typePrep,
        liste: this.liste,
        voie: this.voie,
        duree: this.duree,
        froid: this.froid,
        lumiere: this.lumiere,
        agiter: this.agiter,
        mode_operatoire: this.modeOperatoire,
        contre_indications: this.emploi,
        publications: this.publications,
        cloud: this.cloud,
        pediatric: this.pediatric,
        hospitaliere: this.hospital,
        specialite: this.specialite,
      };
      if(!this.formuleId){
        this.articlesRows.forEach((row) => {
        this.addArticles(row);
      });
        this.parametresRows.forEach((row) => {
        this.addParametres(row);
      });
        this.episRows
          .map(row => ({
            id: row.id,
            num_formule: row.num_formule,
            epi: row.epi.id
          }))
          .forEach((row) => {
            if(this.allEpisFormules) {
              const rowExists = this.allEpisFormules.some((epiFormule) => epiFormule.num_formule === row.num_formule && epiFormule.id === row.id);

              if (rowExists) {
                console.log('row', row);
                this.updateEpis({formData: row, id: row.id});
              } else {
                console.log('add');
                this.addEpis(row);
              }
            }else{
              this.addEpis(row);
            }
        });
        this.etapesRows.forEach((row) => {
        this.addEtapes(row);
      });

        await this.addFormule(formData);
      }else{
          this.articlesRows.forEach((row) => {
          this.updateArticles(row);
        });
          this.parametresRows.forEach((row) => {
          this.updateParametres(row);
        });
          this.episRows.forEach((row) => {
          this.updateEpis(row);
        });
          this.etapesRows.forEach((row) => {
          this.updateEtapes(row);
        });
          const formuleId = this.formuleId;
        await this.updateFormule({formData, formuleId});
      }
      this.name= '';
      this.typePrep= null;
      this.liste= null;
      this.voie= null;
      this.duree= '';
      this.froid= false;
      this.lumiere= false;
      this.agiter= false;
      this.modeOperatoire= '';
      this.emploi= '';
      this.publications= '';
      this.cloud= false;
      this.pediatric= false;
      this.specialite= false;
      this.controlesRows= [];
      this.step= 1;

    },
  },
};
</script>






