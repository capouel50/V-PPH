<template>
  <q-page >
    <div class="row justify-center">
      <div class="col-md-12">
        <div class="row q-mx-sm q-mt-sm">
          <div class="col-3">
            <div class="row">
              <q-fab glossy class="glossy btn-cyan-pph" icon="add_box" direction="right">
                <router-link :to="{ name: 'CreateAppareilsSupplier' }">
                  <q-fab-action flat color="cyan-4" icon="forklift" class="hover-effect">
                    <q-tooltip>Fournisseur</q-tooltip>
                  </q-fab-action>
                </router-link>
                <router-link :to="{ name: 'CreateAppareils' }">
                  <q-fab-action flat color="cyan-4" icon="appareil" class="hover-effect">
                    <q-tooltip>appareil</q-tooltip>
                  </q-fab-action>
                </router-link>
              </q-fab>
            </div>
          </div>
          <div class="col-6 q-mt-md text-cyan-4 text-h6">
            <div class="row justify-center">
            {{ countAppareils }} appareils référencées
            </div>
          </div>
          <div class="col-2 offset-1">
            <q-input
                ref="searchInput"
                v-model="searchQuery"
                label="Recherche..."
                @input="filterAppareils"
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
          <div class="col-12 justify-center">
            <div class="row justify-start">
              <div class="col-2 q-pa-sm" v-for="appareil in filteredAppareils" :key="appareil.id">
                <q-card bordered
                        class="card-maxi justify-center items-center text-center relative"
                        :class="{ 'bd-red-4': !appareil.is_activate}"
                        @click.stop="redirectToLink(appareil.id)"
                >
                  <div class="card-content">
                    <q-img class="logo-card-mini"
                           src="../../assets/img/blanc.jpg"
                           loading="lazy"
                           spinner-color="red-4"
                           :alt="appareil.nom">
                      <div class="absolute-top hover-effect q-my-none" :class="{ 'text-cyan-1': appareil.is_activate, 'text-red-4': !appareil.is_activate }">
                        <div>{{ appareil.nom }}</div>
                        <div>{{ appareil.modele }}</div>
                        <div>
                          <font-awesome-icon v-if="(new Date(appareil.prochaine) - new Date(appareil.calibration)) < 30 * 24 * 60 * 60 * 1000"
                                             icon="fa-solid fa-triangle-exclamation"
                                             beat-fade
                                             size="fa-xs"
                                             style="color: #e57373;"
                          />
                          Prochaine calibration :
                        </div>
                        <div>
                          {{ appareil.prochaineFormatted }}
                        </div>
                      </div>
                      <template v-slot:loading>
                        <q-spinner-rings color="red-4" />
                      </template>
                    </q-img>
                    <q-btn flat color="white" class="absolute-top-right hover-effect q-pa-none q-ma-none"
                           icon="more_vert" @click.stop="toggleMenu(appareil.id)"
                    />
                    <q-menu fit anchor="top right" self="bottom middle" v-model="showMenu[appareil.id]">
                      <q-list style="min-width: 100px">
                        <q-item clickable v-close-popup @click.stop="toggleActivation({ appareilId: appareil.id, isActive: appareil.is_activate, appareilName: appareil.nom })">
                          <q-item-section :class="{ 'hover-effect-warning': appareil.is_activate, 'hover-effect-success': !appareil.is_activate }">
                            {{ appareil.is_activate ? 'Désactiver' : 'Activer' }}
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </q-menu>
                  </div>

                  <q-btn-group class="absolute-bottom-right q-pa-none q-ma-none">
                    <q-btn
                      class="hover-effect"
                      :color="expanded[appareil.id] ? 'orange-4' : 'cyan-4'"
                      round
                      flat
                      dense
                      icon="info"
                      size="sm"
                      @click.stop="toggleInfo(appareil.id)"
                    />
                  </q-btn-group>

                  <q-menu fit anchor="bottom right" self="top middle" v-model="expanded[appareil.id]">
                    <q-list style="min-width: 100px">
                      <q-item class="justify-center">
                        <q-item-section avatar class="text-cyan-4">
                          Détails
                        </q-item-section>
                      </q-item>
                      <q-item>
                        <q-item-section avatar class="text-orange-4">
                          Fournisseur :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ appareil.fabricant.name }}
                        </q-item-section>
                      </q-item>
                      <q-item>
                        <q-item-section avatar class="text-orange-4">
                          Calibration :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ appareil.calibration }}
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
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {formatDate} from '@/utils/helpers'


export default {
  name: "MatieresCards",
  components: {
    FontAwesomeIcon,
  },

  data() {
    return {
      searchQuery: '',
      appareilId: '',
    };
  },

  computed: {
    ...mapGetters('appareils', ['allAppareils', 'showMenu', 'expanded']),

    countAppareils() {
      return Array.isArray(this.filteredAppareils) ? this.filteredAppareils.length : 0;
    },

    filteredAppareils() {
      if (!Array.isArray(this.allAppareils)) {
        return [];
      }

      if (this.searchQuery) {
        return this.allAppareils.filter(appareil =>
            appareil.nom.toLowerCase().includes(this.searchQuery.toLowerCase()) &&
            appareil.fabricant.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      }

      return this.allAppareils.map(appareil => {
        appareil.prochaineFormatted = formatDate(new Date(appareil.prochaine));
        return appareil;  // Return modified appareil object
      });
    },
  },

  async created() {
    await this.loadAppareils();
    console.log('allappareil', this.allAppareils);
  },

  methods: {
    ...mapActions('appareils', ['loadAppareils', 'toggleMenu', 'toggleInfo', 'toggleActivation']),

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
      this.$router.push(`/modifier-appareils/${id}`);
    }

  }
};
</script>



