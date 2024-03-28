<template>
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
      <div v-if="appareilId" class="text-h5 text-center text-cyan-4">{{ appareil.nom }}</div>
      <div v-else class="text-h5 text-center text-cyan-4">Nouvelle Appareil</div>
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
            v-model="nom"
            label="Nom de l'appareil"
            color ='cyan-4'
            @mouseover="changeLabelColor('nameInput','#ffb74d')"
            @mouseleave="changeLabelColor('nameInput','')"
            @focus="onFocus('name','#4dd0e1')"
            @blur="onBlur('name')"
        >
          <template v-slot:prepend>
            <q-icon name="branding_watermark" color="cyan-4"/>
          </template>
        </q-input>

          <q-input
            v-model="modele"
            color="cyan-4"
            class="col-3 hover-effect"
            label="Modèle"
          >
            <template v-slot:prepend>
              <q-icon name="computer" color="cyan-4"/>
            </template>
          </q-input>
        </div>
        <div class="row">
          <q-select
            v-model="fabricant"
            color="cyan-4"
            class="col-2 q-mr-lg hover-effect"
            label="Fabricant"
            :options="suppliers"
            option-label="label"
            option-value="id"
          >
            <template v-slot:prepend>
              <q-icon name="forklift" color="cyan-4"/>
            </template>
          </q-select>
          <q-select
            v-model="type"
            color="cyan-4"
            class="col-2 offset-1 hover-effect"
            label="Type"
            :options="types"
            option-label="nom"
            option-value="id"
          >
            <template v-slot:prepend>
              <q-icon name="devices" color="cyan-4"/>
            </template>
          </q-select>
        </div>
        <q-stepper-navigation>
          <q-btn flat @click="step = 2" color="cyan-4" label="Suivant" class="hover-effect" />
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="2"
        title="Calibration"
        icon="calendar_month"
        :done="step > 2"
      >

      <div class="row">
        <q-input
        ref="dureeInput"
        type="date"
        class="my-0 col-2"
        v-model="date_calibration"
        label="Dernière calibration"
        color ='cyan-4'
        @mouseover="changeLabelColor('nameInput','#ffb74d')"
        @mouseleave="changeLabelColor('nameInput','')"
        @focus="onFocus('name','#4dd0e1')"
        @blur="onBlur('name')"
      >
        <template v-slot:prepend>
          <q-icon name="alarm" color="cyan-4"/>
        </template>
      </q-input>
      </div>
      <div class="row">
        <q-input
        ref="dureeInput"
        class="my-0 col-2"
        v-model="duree_calibration"
        label="Validitée"
        color ='cyan-4'
        @mouseover="changeLabelColor('nameInput','#ffb74d')"
        @mouseleave="changeLabelColor('nameInput','')"
        @focus="onFocus('name','#4dd0e1')"
        @blur="onBlur('name')"
      >
        <template v-slot:append>
          <div class="text-cyan-4 q-pt-md text-subtitle2">mois</div>
        </template>
        <template v-slot:prepend>
          <q-icon name="alarm" color="cyan-4"/>
        </template>
      </q-input>
      </div>
      <div class="q-pa-md q-gutter-sm">
        <div>
          <q-toggle
            v-model="blocage_calibration"
            color="green-4"
            icon="stop"
            label="Autoriser dépassement de date"
            size="md"
          />
         </div>
      </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 1" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          <q-btn flat @click="step = 3" color="cyan-4" label="Suivant" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="3"
        title="Communication"
        icon="device_hub"
        :done="step > 3"
      >
        <div class="row">
          <q-select
            v-model="com"
            color="cyan-4"
            class="col-2 hover-effect"
            label="Communication"
            :options="coms"
            option-label="nom"
            option-value="id"
          >
            <template v-slot:prepend>
              <q-icon name="gavel" color="cyan-4"/>
            </template>
          </q-select>
        </div>
        <div class="row">
          <div class="col-12">
            <InstructionsForm v-if="step === 3" :newId="newId" :appareilId="appareilId" :instructions="instructions" :reponses="reponses"/>
          </div>
        </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 2" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          <q-btn flat @click="step = 4" color="cyan-4" label="Suivant" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>

      <div class="row justify-center">
        <q-btn-group>
          <q-btn flat @click="submitForm" color="green-4" label="Enregistrer" class="btn-flat-success-pph"/>
        </q-btn-group>
    </div>
    </q-stepper>
  </div>
</template>

<script>
import InstructionsForm from './InstructionsForm.vue';
import {mapActions, mapGetters } from "vuex";

export default {
  components: {
    InstructionsForm,
  },
  data() {
    return {
      step: 1,
      newId: '',
      appareilId: '',
      type: '',
      nom: '',
      modele: '',
      fabricant: '',
      date_calibration: '',
      duree_calibration: '',
      blocage_calibration: false,
      appareil: [],
      types: [],
      com:'',
      coms: [],
      instructions: [],
      suppliers: [],
      reponses: [],
    };
  },

  computed: {
    ...mapGetters('suppliers', ['allSuppliers']),
    ...mapGetters('appareils', ['allAppareils', 'allTypes', 'allComs', 'allInstructionsAppareils', 'allReponses']),

  },

  async created() {
    await this.loadSuppliersAppareils();
    await this.loadAppareils();
    await this.loadCom();
    await this.loadTypesAppareils();
    this.types = this.allTypes;
    this.coms = this.allComs;
    this.suppliers = this.allSuppliers;
    if(this.$route.params.id){
      this.appareilId = Number(this.$route.params.id);
      await this.loadInstructionsAppareils();
      await this.loadReponses();
      this.instructions = this.allInstructionsAppareils.filter(instruction => instruction.modele_appareil === this.appareilId);
      this.reponses = this.instructions.map((instruction) => {
         return this.allReponses.filter((reponse) => reponse.num_instruction === instruction.id);
      });
      this.reponses = this.reponses.flat();
      this.appareil = this.allAppareils.find(appareil => appareil.id === this.appareilId);
      this.nom = this.appareil.nom;
      this.modele = this.appareil.modele;
      this.fabricant = this.appareil.fabricant.name;
      this.date_calibration = this.appareil.calibration;
      this.duree_calibration = this.appareil.duree_calibration;
      this.blocage_calibration = this.appareil.bloque_calibration;
      this.type = this.appareil.type.nom;
      this.com = this.appareil.com.nom;
    }
    this.newId = this.allAppareils.length;
  },

  methods: {
    ...mapActions('suppliers', ['loadSuppliersAppareils']),
    ...mapActions('appareils', ['addAppareil', 'loadAppareils', 'loadTypesAppareils',
                                'loadCom', 'loadInstructionsAppareils', 'loadReponses']),

    addAppareil() {
      const formData = {
        nom: this.nom,
        modele: this.modele,
        fabricant: this.fabricant,
        calibration: this.calibration,
        duree_calibration: this.duree_calibration,
        blocage_calibration: this.blocage_calibration,
        type: this.type,
        com: this.com,
      };
      this.addAppareil(formData);
    }

  },
};
</script>






