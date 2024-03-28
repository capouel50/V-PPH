<template>
  <q-page v-if="loading">
    <div class="row">
      <div class="col-3 q-mt-md q-pl-lg">
        <q-fab glossy class="glossy btn-cyan-pph" icon="print" direction="right">
          <q-fab-action flat external-label label-position="bottom" label="Fiche" color="cyan-4" icon="description"/>
          <q-fab-action flat external-label label-position="bottom" label="Etiquettes" color="cyan-4" icon="note_stack"/>
        </q-fab>
      </div>
      <div class="col-6 text-h6 text-cyan-4 q-mt-lg text-center">
        Fiche n°{{ fiche.id }} - {{ fiche.prep.nom }}
      </div>
    </div>

    <div class="row justify-evenly q-mt-md">

      <div class="col-2">
        <div v-if="this.articles.length">
          <q-card class="q-mb-md bg-op-8">
          <q-card-section>

            <q-item clickable class="row">
              <q-item-section class="text-subtitle1 text-center"
                              :class="materiel ? 'text-orange-4' : 'text-cyan-4'"
                              @click="materiel = !materiel"
              >
                Matériel
              </q-item-section>
            </q-item>

          </q-card-section>

          <q-slide-transition>
            <div v-show="materiel">
              <q-separator />
              <q-card-section class="text-subtitle2">
                <q-list v-for="article in articles" :key="article.id">
                  <q-item class="row">
                    <q-item-section>
                      {{ article.article.nom}}
                    </q-item-section>
                  </q-item>
                </q-list>
              </q-card-section>
            </div>
          </q-slide-transition>

        </q-card>
        </div>

        <div v-if="this.epis.length">
          <q-card class="q-mb-md bg-op-8">
          <q-card-section>
            <q-item clickable class="row">
              <q-icon  class="fade-blink" name="warning" color="red-4" size="sm"/>
              <q-item-section class="text-subtitle1 text-center q-mr-md"
                              :class="expanded ? 'text-orange-4' : 'text-cyan-4'"
                              @click="expanded = !expanded"
              >
                {{ this.epis.length }} EPI
              </q-item-section>
            </q-item>

          </q-card-section>

          <q-slide-transition>
            <div v-show="expanded">
              <q-separator />
              <q-card-section>
                <q-list v-for="epi in epis" :key="epi.id">
                  <q-item class="row">
                    <q-item-section>
                      {{ epi.epi.nom}}
                    </q-item-section>
                  </q-item>
                </q-list>
              </q-card-section>
            </div>
          </q-slide-transition>

        </q-card>
        </div>

        <div>
          <q-card class="bg-op-8">
          <q-card-section>

            <q-item clickable class="row">
              <q-item-section class="text-subtitle1 text-center"
                              :class="modeOp ? 'text-orange-4' : 'text-cyan-4'"
                              @click="modeOp = !modeOp"
              >
                Mode opératoire
              </q-item-section>
            </q-item>

          </q-card-section>

          <q-slide-transition>
            <div v-show="modeOp">
              <q-separator />
              <q-card-section class="text-subtitle2">
                <div>
                  {{ fiche.prep.mode_operatoire}}
                </div>
              </q-card-section>
            </div>
          </q-slide-transition>

          </q-card>
        </div>
      </div>
      <div class="col-7">
        <q-card class="bg-op-8">
          <q-card-section>

            <q-item>
              <q-item-section class="text-subtitle1 text-cyan-4 text-center">
                Composition de la formule
              </q-item-section>
            </q-item>

          </q-card-section>

          <q-separator/>

          <q-card-section>
            <q-list v-for="compo in composition" :key="compo.id">
              <q-item clickable class="row justify-evenly" :class="activeCompo === compo ? 'bg-cyan-1' : ''"
                      @click="activeCompo = compo; appareils(); updateQteTheory(compo)"
              >
                <q-item-section class="col-4 q-pl-sm text-cyan-4">
                  {{ compo.matiere.nom}}
                </q-item-section>
                <q-item-section class="col-1 text-orange-4">
                  {{ compo.result }}{{ compo.matiere.unite_mesure.nom}}
                </q-item-section>
                <q-item-section class="col-1 text-orange-4">
                  <q-img v-if="compo.matiere.cmr" class="q-ml-xs fade-blink" src="@/assets/img/health_hazard.png" :style="{ width: '20px', height: '20px' }"/>
                </q-item-section>
                <q-item-section class="col-2">
                  <q-input
                      v-model="compo.num_reception"
                      label="N° réception"
                      color="cyan-4"
                      @change="updateReception(compo)"
                  />
                </q-item-section>
                <q-item-section class="col-2 text-subtitle2 text-center" :class="!compo.reception.certificat && !compo.reception.echantillon ? 'text-red-4' : 'text-green-4'">
                  <q-item-label>
                    {{ compo.reception.lot }}
                    <q-btn
                        v-if="compo.reception.isValid && !compo.reception.certificat"
                        flat
                        icon="add_box"
                        color="cyan-4"
                        class="q-pa-none hover-effect-success"
                        size="xs"
                        @click="addMatiereCertif(compo)"
                    >
                    <q-tooltip class="bg-blue-grey-4">Ajouter un certificat</q-tooltip>
                    </q-btn>
                  </q-item-label>
                  <q-form>
                    <q-dialog v-model="addMatiereLot">
                    <q-card>

                      <q-card-section>
                        <div class="row justify-center text-h6 text-cyan-4">
                          Ajouter un certificat d'analyse ou un echantillon pour le lot
                        </div><br/>
                        <div class="row justify-center text-subtitle1 text-orange-4">
                        {{ lot }}
                        </div><br/>
                      </q-card-section>

                      <q-separator/>

                      <q-card-section>
                        <div class="row justify-center">
                          <div class="col-12">
                            <q-file
                              label="Sélectionner un certificat(.pdf)"
                              accept=".pdf"
                              v-model="certificatReception"
                            />
                          </div>
                        </div>
                        <div class="row" v-if="!reception.echantillon">
                          <div class="col-2 q-mt-sm">
                            <q-toggle
                              label="Echantillon"
                              color="green-4"
                              v-model="echantillon"
                            />
                          </div>
                          <div class="col-2 offset-2" v-show="echantillon">
                            <q-input
                              label="Quantité"
                              color="cyan-4"
                              v-model="qte"
                            >
                              <template v-slot:append>
                                <div class="text-cyan-4 text-subtitle2 q-pt-md">
                                  {{ unite }}
                                </div>
                              </template>
                            </q-input>
                          </div>
                        </div>

                      </q-card-section>

                      <q-separator/>

                      <q-card-section>
                        <div class="row justify-center">
                        <q-btn-group>
                          <q-btn flat label="Ajouter" @click="addCertif(compo)" color="green-4"/>
                          <q-btn flat label="Annuler" @click="addMatiereLot=false" color="red-4"/>
                        </q-btn-group>
                          </div>
                      </q-card-section>

                    </q-card>
                  </q-dialog>
                  </q-form>
                  <q-item-label class="text-subtitle2">
                    {{ compo.reception.peremption }}
                  </q-item-label>
                </q-item-section>
                <q-item-section class="col-2 q-pr-sm">
                  <q-input v-if="compo.reception.isValid"
                      v-model="compo.pesee"
                      label="Quantité"
                      color="cyan-4"

                  >
                    <template v-slot:append>
                      <div class="text-cyan-4 text-subtitle2 q-pt-md">{{ compo.matiere.unite_mesure.nom}}</div>
                    </template>
                  </q-input>
                </q-item-section>
              </q-item>
            </q-list>
          </q-card-section>

          <q-separator/>

          <q-card-section>
            <q-card-actions class="justify-center">
              <q-btn-group>
                <q-btn
                flat
                color="green-4"
                label="Valider"
                @click="saveData"
              />
              </q-btn-group>
            </q-card-actions>
          </q-card-section>

        </q-card>
      </div>

      <div class="col-2">
        <div v-if="activeCompo">
          <q-card class="bg-op-8">
          <q-card-section class="q-pt-none q-pb-xs">
            <q-item>
              <q-item-section>
                <q-select
                  class="q-mb-xs q-py-none"
                  v-model="appareil"
                  color="cyan-4"
                  :label="activeCompo.type_appareil.nom"
                  :options="typesAppareil"
                  option-label="nom"
                  option-value="id"
                />
              </q-item-section>
            </q-item>

          </q-card-section>

          <q-separator/>

          <q-card-section>
            <div class="text-cyan-4 text-subtitle2 text-center">{{ activeCompo.matiere.nom}}</div>
            <div class="row justify-center" :class="getDeviationPercentageColor()">
              <div class="text-center text-h6 text-cyan-1" >
                {{ this.selectedCompoPesee }}{{ qteTheory.unite }} / {{ qteTheory.value }}{{ qteTheory.unite }}
              </div>
            </div>
            <div class="row justify-center text-cyan-1" :class="getDeviationPercentageColor()">
              <div class="text-subtiltle1">
                Ecart : {{ calculateDeviationPercentage() }}%
              </div>
            </div>
          </q-card-section>
            <q-separator v-if="appareil && btns.length > 0"/>
          <q-card-section v-if="appareil && btns.length > 0">
            <q-item clickable class="row" @click="buttons = !buttons">
                <q-item-section
                  class="text-center text-subtitle1"
                  :class="buttons ? 'text-orange-4' : 'text-cyan-4'"
                >
                  Fonctions
                </q-item-section>
            </q-item>
          </q-card-section>
          <q-slide-transition>
            <div v-show="buttons">
              <q-separator/>
              <q-card-section class="row justify-evenly">
                <div v-for="btn in btns" :key="btn.id">
                  <div class="col-4">
                    <q-btn
                      flat
                      :label="btn.action"
                      class="hover-effect"
                      color="cyan-4"
                  >
                    <q-tooltip>{{ btn.description}}</q-tooltip>
                  </q-btn>
                  </div>
                </div>
              </q-card-section>
            </div>
          </q-slide-transition>

        </q-card>
        </div>

      </div>
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
import { mapActions, mapGetters, mapMutations } from 'vuex';
import {AtomSpinner} from 'epic-spinners'
import { getCalculatedQty, formatDate } from '@/utils/helpers'
export default {
  name: 'InfosFiche',
  components: {
    AtomSpinner
  },

  data() {
    return {
      activeCompo: null,
      loading: false,
      id: null,
      fiche: [],
      composition: [],
      parametres: [],
      epis: [],
      articles: [],
      result: [],
      expanded: false,
      modeOp: false,
      habillage: false,
      materiel: false,
      qteTheory: {
        value: null,
        unite: null,
      },
      selectedCompoPesee: null,
      typesAppareil: [],
      appareil: null,
      lastId: null,
      reception: [],
      num_reception: null,
      addMatiereLot: false,
      lot: null,
      certificatReception: null,
      echantillon: false,
      qte: null,
      btns: [],
      buttons: false,
    };
  },

  computed: {
    ...mapGetters('fiches', ['allFiches', 'allParametresFiches']),
    ...mapGetters('formules', ['allCompositions', 'allParametresFormules', 'allArticlesFormules']),
    ...mapGetters('epi', ['allEpis', 'allEpisFormules']),
    ...mapGetters('appareils', ['allAppareils', 'allInstructionsAppareils']),
    ...mapGetters('demandes', ['allDemandes', 'allParametresDemandes']),
    ...mapGetters('matieresPremieres', ['allReceptions']),
  },

  async created() {
    await Promise.all([
      this.loadReceptions(),
      this.loadCompositions(),
      this.loadParametresFormules(),
      this.loadEpisFormules(),
      this.loadArticlesFormules(),
      this.loadAppareils(),
      this.loadInstructionsAppareils(),
    ]);
    const allFiches = this.allFiches;
    this.lastId = Math.max(...allFiches.map(fiche => fiche.id));

    if(this.$route.params.demandeId) {
      this.loadDemandes(),
      this.loadParametresDemandes(),
      this.id = this.$route.params.demandeId;
      this.fiche = this.allDemandes.find(demande => demande.id === Number(this.id));
      if(this.fiche.commentaire) {
        this.showNotification({message: this.fiche.commentaire, type: 'info', position: 'center'});
      }
      this.parametres = this.allParametresDemandes.filter(param => param.num_demande === this.fiche.id);
      this.parametres.forEach(parametre => {
        this.ADD_PARAMETRES_FICHES ({
            num_fiche: this.lastId + 1,
            parametre: parametre.parametre,
            valeur_parametre: parametre.valeur_parametre
          });
        });

      this.ADD_FICHE ({
        id: this.lastId + 1,
        prep: this.fiche.prep.id,
        typePrep: this.fiche.typePrep.id,
        service: this.fiche.service.id,
        patient: this.fiche.patient,
        age: this.fiche.age,
        prescripteur: this.fiche.prescripteur,
      });
        const allFiches = this.allFiches;
        this.lastId = Math.max(...allFiches.map(fiche => fiche.id));
        this.id = this.lastId;
    }else {
        this.id = this.$route.params.ficheId;
        this.fiche = this.allFiches.find(fiche => fiche.id === Number(this.id));
    }
    this.parametres = this.allParametresFiches.filter(param => param.num_fiche === this.fiche.id);
    this.epis = this.allEpisFormules.filter(epi => epi.num_formule === this.fiche.prep.id);
    this.articles = this.allArticlesFormules.filter(article => article.num_formule === this.fiche.prep.id);
    this.composition = this.allCompositions
    .filter(compo => compo.num_formule === this.fiche.prep.id)
    .map(compo => {
      const updatedCompo = {...compo};
      updatedCompo.num_reception = '';
      updatedCompo.reception = {isValid: false};

      // Initialisez pesee pour chaque compo
      updatedCompo.pesee = 0;

      const formula = compo.calcul;
      const params = this.parametres;
      const qte = compo.qté;
      const unitMeasureString = compo.matiere.unite_mesure.nom;

      updatedCompo.result = getCalculatedQty(formula, params, qte, unitMeasureString);

      if (updatedCompo.matiere.unite_mesure.nom === 'ml' && updatedCompo.matiere.densite) {
        updatedCompo.result = (updatedCompo.result * updatedCompo.matiere.densite).toFixed(2);
        updatedCompo.matiere.unite_mesure.nom = 'g';
      }

      return updatedCompo;
    });
    this.loading= true;
  },

  watch: {
    appareil(newValue) {
        this.handleInput(newValue);
    },
  },

  methods: {
    ...mapActions('fiches', ['loadFiches', 'loadParametresFiches', 'loadLastFicheId', 'addFiche', 'addParametresValues']),
    ...mapActions('formules', ['loadCompositions', 'loadParametresFormules', 'loadArticlesFormules',]),
    ...mapActions('epi', ['loadEpis', 'loadEpisFormules']),
    ...mapActions('demandes', ['loadDemandes', 'loadParametresDemandes', 'loadLastDemandeId']),
    ...mapActions('appareils', ['loadAppareils', 'loadInstructionsAppareils']),
    ...mapActions('notifications', ['showNotification']),
    ...mapActions('matieresPremieres', ['loadReceptions', 'addCertificat']),
    ...mapMutations('fiches', ['ADD_FICHE', 'ADD_PARAMETRES_FICHES']),

    appareils(){
      this.typesAppareil = this.allAppareils.filter(appareil => appareil.type.nom === this.activeCompo.type_appareil.nom);
      this.appareil = null;
      this.btns = [];
      this.buttons = false;
    },


    addMatiereCertif(){
      this.addMatiereLot = true;
      this.lot = this.reception.lot;
      this.unite = this.reception.matiere.unite_mesure.nom
    },

    addCertif(){
      const id = this.reception.id
      const formData = {
        certificat: this.certificatReception,
        echantillon: this.echantillon,
        qte_echantillon: this.qte,
      };
      this.addCertificat({ formData, id });
      this.loadReceptions();
    },

    async addReception(compo, reception, peremption) {
      compo.reception = JSON.parse(JSON.stringify(reception)) || {};
      compo.reception.peremption = formatDate(peremption);
      compo.reception.isValid = true;
      if(!compo.reception.certificat && !compo.reception.echantillon){
        this.showNotification({message: 'Aucun certificat d\'analyse, ni d\'échantillon pour le lot ' + compo.reception.lot, type: 'info'})
        this.showNotification({message: 'Réception ajoutée', type: 'success'})
      }else if(!compo.reception.certificat && compo.reception.echantillon){
        this.showNotification({message: 'Aucun certificat d\'analyse pour le lot ' + compo.reception.lot, type: 'info'})
        this.showNotification({message: 'Réception ajoutée', type: 'success'})
      }else {
        this.showNotification({message: 'Réception ajoutée', type: 'success'})
      }
    },

    async updateReception(compo) {
      const reception = await this.allReceptions.find(reception => reception.id === Number(compo.num_reception)
          && reception.matiere.id === compo.matiere.id);
      const today = new Date();
      this.reception = reception;
      today.setDate(today.getDate() + Number(this.fiche.prep.duree));
      const limitDate = today;
      let peremption;
      if(reception){
        peremption = new Date(reception.peremption);
      }
      if(!reception){
        this.showNotification({message:'Erreur de numéro de réception', type:'error'});
        compo.num_reception = '';
      }else if(reception && peremption > limitDate) {
        this.addReception(compo, reception, peremption);
      }else if(reception && peremption < limitDate){
        this.showNotification({message: 'Date de péremption: ' + formatDate(peremption), type: 'info', position: 'center', time: 200000, options: {actions: [
            { label: 'Ajouter', color: 'green', handler: () => { this.addReception(compo, reception, peremption); } },
            { label: 'Annuler', color: 'red', handler: () => { compo.num_reception = '' } }
          ]}
        })
      }
    },

    handleInput(appareil) {
        if (appareil) {
            this.btns = this.allInstructionsAppareils.filter(btn => btn.modele_appareil === appareil.id && btn.button === true);
        } else {
            console.error('Invalid appareil object or ID');
        }

    },

    updateQteTheory(compo) {
      this.selectedCompoPesee = compo.pesee;
      this.qteTheory.value = compo.result;
      if(compo.matiere.densite) {
        this.qteTheory.unite = 'g';
      }else{
        this.qteTheory.unite = compo.matiere.unite_mesure.nom;
      }
    },

    calculateDeviationPercentage() {
      // Convert values to Number if they aren't
      const liveDataValue = Number(this.selectedCompoPesee);
      const qteTheoryValue = Number(this.qteTheory.value);

      // Calculate the percentage difference
      const percentageDifference = ((Math.abs(liveDataValue - qteTheoryValue)) / qteTheoryValue) * 100;

      // Return the result rounded to to two decimal places
      return percentageDifference.toFixed(2);
    },

    getDeviationPercentageColor() {
      // calculate deviation percentage
      const deviationPercentage = this.calculateDeviationPercentage();

      // return the color class depending on the percetage
      return deviationPercentage < 5 ? 'bg-green-4' : 'bg-red-4';
    },

    saveData(){

      this.parametres.forEach(parametre => {
          const dataObject = {
              num_fiche: this.lastId + 1,
              parametre: parametre.parametre.id,
              valeur_parametre: parametre.valeur_parametre
          };

          const dataJson = JSON.stringify(dataObject);

          this.addParametresValues(dataJson);
      });
      const ficheData = {
        id: this.lastId + 1,
        prep: this.fiche.prep.id,
        typePrep: this.fiche.typePrep.id,
        service: this.fiche.service.id,
        patient: this.fiche.patient,
        age: this.fiche.age,
        prescripteur: this.fiche.prescripteur,
      }
      this.addFiche (ficheData);
    }

  },
}

</script>








