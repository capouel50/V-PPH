<template>
  <q-page>
    <div class="row justify-center">
      <div class="col-md-12">
        <div class="row q-mx-sm">
          <div class="col-4 offset-4 q-mt-md text-cyan-4 text-h6">
            <div class="row justify-center">
            {{ controlCount }} fiches en attente de contrôle
            </div>
          </div>
          <div class="col-2 offset-2 q-mt-sm">
            <q-input
                ref="searchInput"
                v-model="searchQuery"
                label="Recherche..."
                @input="filteredFiches"
                color="cyan-4"
                @mouseover="changeLabelColor('searchInput', '#ffb74d')"
                @mouseleave="changeLabelColor('searchInput', '')"
                @focus="onFocus('searchQuery', '#4dd0e1')"
                @blur="onBlur('searchQuery')"
            >
              <template v-slot:append>
                <q-icon name="search" color="cyan-4"/>
              </template>
            </q-input>
          </div>
        </div>
        <div class="row q-mt-sm">
          <div class="col col-12 justify-center">
            <div class="row justify-start">
              <div class="col-2 q-pa-sm" v-for="fiche in filteredFiches" :key="fiche.id">
                <q-card v-if="!fiche.destruction"
                    bordered
                    class="card-maxi justify-center items-center text-center relative"
                    @click.stop="redirectToLink(fiche.id)"
                >
                  <div class="card-content">
                    <q-img
                        class="logo-card-mini"
                        src="../../assets/img/blanc.jpg"
                        :alt="fiche.prep.nom"
                        loading="lazy"
                        spinner-color="red-4"
                    >
                      <div class="absolute-top hover-effect q-my-none text-cyan-1">
                        <div>{{ fiche.date_fab }}</div>
                        <div v-if="fiche.patient">{{ fiche.patient }}</div>
                        <div>{{ fiche.prep.nom }}</div>
                      </div>
                      <template v-slot:loading>
                        <q-spinner-rings color="red-4" />
                      </template>
                    </q-img>
                    <q-btn flat color="white" class="absolute-top-right hover-effect q-pa-none q-ma-none" icon="more_vert" @click.stop="toggleMenu(fiche.id)" />
                    <q-menu fit anchor="top right" self="bottom middle" v-model="showMenu[fiche.id]">
                      <q-list style="min-width: 100px">
                        <q-item clickable v-close-popup @click.stop="toggleControle({ ficheId: fiche.id, isControl: fiche.controle_valide })">
                          <q-item-section class="hover-effect-success">
                            Valider contrôle
                          </q-item-section>
                        </q-item>
                        <q-item clickable v-close-popup @click.stop="toggleDestruction({ ficheId: fiche.id, isDestroy: fiche.destruction })">
                          <q-item-section class="hover-effect-warning">Destruction</q-item-section>
                        </q-item>
                      </q-list>
                    </q-menu>
                  </div>
                  <div class="absolute-top-left hover-effect q-ml-xs q-my-none text-red-4">
                    <div>n°{{ fiche.id }}</div>
                  </div>
                  <div class="absolute-bottom-left">
                    <div class="row q-mb-xs">
                      <font-awesome-icon v-if="fiche.prep.pediatric" icon="fa-solid fa-child" class="q-ml-xs fa-lg" style="color: #4dd0e1;"/>
                      <font-awesome-icon v-if="fiche.prep.froid" fade icon="fa-solid fa-snowflake" class="q-ml-xs fa-lg" style="color: #4dd0e1;" />
                      <q-icon v-if="fiche.prep.agiter" name="waving_hand" class="q-ml-xs" color="cyan-4" size="xs"/>
                      <q-icon v-if="fiche.prep.lumiere" name="light_mode" class="q-ml-xs" color="red-4" size="xs"/>
                    </div>
                  </div>
                  <q-btn-group class="absolute-bottom-right q-pa-none q-ma-none">
                    <q-btn
                       class="q-pa-none hover-effect"
                       flat
                       :color="compo[fiche.id] ? 'orange-4' : 'cyan-4'"
                       icon="science"
                       size="sm"
                       @click.stop="toggleCompo(fiche.id)"
                    />
                    <q-btn
                       class="q-pa-none hover-effect"
                       flat
                       :color="settings[fiche.id] ? 'orange-4' : 'cyan-4'"
                       icon="settings"
                       size="sm"
                       @click.stop="toggleSettings(fiche.id)"
                    />
                    <q-btn
                      class="hover-effect"
                      :color="info[fiche.id] ? 'orange-4' : 'cyan-4'"
                      round
                      flat
                      dense
                      icon="info"
                      size="sm"
                      @click.stop="toggleInfo(fiche.id)"
                    />
                  </q-btn-group>
                  <q-menu class="row" fit anchor="bottom right" self="top middle" v-model="compo[fiche.id]">
                    <q-list class="col-12">
                      <q-item>
                        <q-item-section class="text-cyan-4 text-center">
                          Composition de la formule
                        </q-item-section>
                      </q-item>
                      <q-item class="row" v-for="compo in filteredCompositions(fiche.prep.id)" :key="compo.id">
                        <q-item-section class="col-auto text-orange-4 text-no-wrap">
                          {{ compo.matiere.nom }} :
                        </q-item-section>
                        <q-item-section class="col-auto text-grey-7">
                          <q-item-label>{{ getCalculatedQty(compo.calcul,filteredParametres(fiche.id), compo.qté, compo.matiere.unite_mesure.nom) }} {{ compo.matiere.unite_mesure.nom }}</q-item-label>
                        </q-item-section>
                        <q-item-section v-if="compo.matiere.cmr" class="col-auto q-ml-none text-grey-7">
                          <q-img class="fade-blink" src="@/assets/img/health_hazard.png"
                                 :style="{ width: '20px', height: '20px' }"/>
                        </q-item-section>
                      </q-item>
                    </q-list>
                  </q-menu>
                  <q-menu fit anchor="bottom right" self="top middle" v-model="settings[fiche.id]">
                    <q-list style="min-width: 100px">
                      <q-item>
                        <q-item-section class="text-cyan-4 text-center">
                          Paramètres de la formule
                        </q-item-section>
                      </q-item>
                      <q-item class="row" v-for="parametre in filteredParametres(fiche.id)" :key="parametre.id">
                        <q-item-section class="col-auto text-orange-4 text-no-wrap">
                          {{ parametre.parametre.nom }} :
                        </q-item-section>
                        <q-item-section class="col-auto text-grey-7">
                          {{ parametre.valeur_parametre }}{{ parametre.parametre.unite }}
                        </q-item-section>
                      </q-item>
                    </q-list>
                  </q-menu>
                  <q-menu fit anchor="bottom right" self="top middle" v-model="info[fiche.id]">
                    <q-list style="min-width: 100px">
                      <q-item>
                        <q-item-section class="text-cyan-4 text-center">
                          Détails de la fiche n° {{ fiche.id }}
                        </q-item-section>
                      </q-item>
                      <q-item v-if="fiche.date_fab">
                        <q-item-section avatar class="text-orange-4">
                          Date d'émission :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ fiche.date_fab }}
                        </q-item-section>
                      </q-item>
                      <q-item v-if="fiche.patient">
                        <q-item-section avatar class="text-orange-4">
                          Patient :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ fiche.patient }} - {{ fiche.age }} ans
                        </q-item-section>
                      </q-item>
                      <q-item v-if="fiche.service.nom">
                        <q-item-section avatar class="text-orange-4">
                          Service :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ fiche.service.nom }}
                        </q-item-section>
                      </q-item>
                      <q-item v-if="fiche.prescripteur">
                        <q-item-section avatar class="text-orange-4">
                          Prescripteur :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ fiche.prescripteur }}
                        </q-item-section>
                      </q-item>
                    </q-list>
                  </q-menu>
                </q-card>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  name: "ControlesCards",

  data() {
    return {
      searchQuery: '',
    };
  },

  computed: {
    ...mapGetters('fiches', ['allFiches', 'allParametresFiches', 'fichesControlCount', 'showMenu', 'settings', 'info', 'compo']),
    ...mapGetters('formules', ['allCompositions']),

    controlCount() {
      return this.fichesControlCount;
    },

    filteredFichesControle() {
      return this.allFiches.filter(fiche => fiche.attente_controle === true);
    },

    filteredFiches() {
      if (this.searchQuery) {
        return this.filteredFichesControle.filter(fiche =>
            fiche.prep.nom.toLowerCase().startsWith(this.searchQuery.toLowerCase()) ||
            fiche.id.toString().startsWith(this.searchQuery.toLowerCase()) ||
            fiche.patient.toLowerCase().startsWith(this.searchQuery.toLowerCase())
        );
      }
      return this.filteredFichesControle;
    },
  },

  created() {
    this.loadFiches();
    this.loadFormules();
    this.loadCompositions();
    this.loadParametresFiches();
  },

  methods: {
    ...mapActions('fiches', ['loadFiches', 'loadParametresFiches', 'toggleInfo', 'toggleSettings', 'toggleCompo',
                             'toggleControle', 'toggleMenu', 'toggleDestruction']),
    ...mapActions('formules', ['loadCompositions', 'loadFormules']),

    getCalculatedQty(formula, params, qte, unitMeasureString) {
      for(let param of params){
        let searchTerm = param.parametre.nom + " - " + param.parametre.unite;
        formula = formula.replace(new RegExp(searchTerm, 'g'), param.valeur_parametre);

        let qteSearchTerm = "Quantité - " + unitMeasureString;
        formula = formula.replace(new RegExp(qteSearchTerm, 'g'), qte);
      }

      try {
        let result = eval(formula);
        // Si le résultat est un nombre, le formater avec 3 chiffres après la virgule
        if(!isNaN(result)) {
          return Number(result).toFixed(2);
        } else {
          return result;
        }
      } catch(e) {
        return "Erreur";
      }
    },

    filteredParametres(ficheId) {
      return this.allParametresFiches.filter(parametre => parametre.num_fiche === ficheId);
    },

    filteredCompositions(ficheFormule) {
      return this.allCompositions.filter(compo => compo.num_formule === ficheFormule);
    },

    changeLabelColor(inputRef, color) {
      if (!this[inputRef.replace('Input', '')]) {
        this.$refs[inputRef].$el.querySelector('.q-field__label').style.color = color;
      }
    },

    onFocus(field, color) {
      this[`${field}Focused`] = true;
      this.changeLabelColor(`${field}Input`, color);
    },

    onBlur(field) {
      this[`${field}Focused`] = false;
    },

    redirectToLink(id) {
      this.$router.push(`/fiche/${id}`);
    }
  }
};
</script>



