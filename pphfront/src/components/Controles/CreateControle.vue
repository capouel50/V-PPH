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
      <div class="text-h5 text-center text-cyan-4">Nouveau Contrôle</div>
       <q-step
        :name="1"
        title="Type de contrôle"
        icon="biotech"
        :done="step > 1"
      >
        <div class="row">
          <q-input
            required
            v-model="typeControle.nom"
            color="cyan-4"
            class="col-3 hover-effect"
            label="Type de contrôle"
          />
        </div>
         <div class="row">
           <q-select
            v-model="typeControle.type_appareil"
            color="cyan-4"
            class="col-2 hover-effect"
            label="Type d'appareil"
            :options="typesAppareils"
            option-label="nom"
            option-value="id"
          />
         </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 2" color="cyan-4" label="Suivant" class="hover-effect" />
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="2"
        title="Mode opératoire"
        icon="vaccines"
        :done="step > 2"
      >
      <div class="row">
        <div class=" col-8">
          <EtapesForm :controleId="controleId" :newId="newId" :rows="formRows" @rows="rows"/>
        </div>
      </div>

      <q-stepper-navigation>
          <q-btn flat @click="step = 1" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
        <q-btn flat @click="step = 3" color="cyan-4" label="Suivant" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="3"
        title="Paramètres"
        icon="settings"
        :done="step > 3"
      >
      <div class="row">
        <q-list bordered class="col-4" v-if="typeControle.structure_formulaire.length > 0">
          <q-item v-for="(field, index) in typeControle.structure_formulaire" :key="index" class="row">
            <q-item-section>
              <q-input v-model="field.name" label="Nom du champ" required></q-input>
            </q-item-section>
            <q-item-section>
              <q-select v-model="field.type" :options="fieldTypes" label="Type du champ" ></q-select>
            </q-item-section>
            <q-item-section side>
              <q-btn flat icon="delete_forever" @click="removeField(index)" color="red-4"></q-btn>
            </q-item-section>
          </q-item>
        </q-list>
        <q-btn flat color="cyan-4" @click="addField" icon="add_box" label="Ajouter" size="md" class="hover-effect"></q-btn>
        <q-btn v-if="typeControle.structure_formulaire.length > 0" flat color="green-4" @click="validParametres" icon="check_circle" label="Valider" size="md"></q-btn>
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
import EtapesForm from '../Formules/EtapesForm.vue';
import {mapActions,  mapGetters} from "vuex";

export default {
  components: {
    EtapesForm,
  },
  data() {
    return {
      step: 1,
      newId: '',
      formRows: [],
      controleId: '',
      typesAppareils: [],
      typeControle: {
        nom: '',
        structure_formulaire: [],
        type_appareil: '',
      },
      fieldTypes: [
        { label: 'Texte', value: 'text' },
        { label: 'Nombre', value: 'number' },
        { label: 'Booléen', value: 'boolean' },
        // Ajoutez d'autres types au besoin
      ]
    };
  },

  computed: {
    ...mapGetters('controles',['allTypesControles']),
    ...mapGetters('appareils',['allTypes']),
  },

  created() {
    this.loadTypes();
    this.loadTypesAppareils();
    this.typesAppareils = this.allTypes;
    console.log('typesAppareils', this.typesAppareils);
    if(this.$route.params.id) {
      this.controleId = this.$route.params.id;
    }else{
      this.newId = this.allTypesControles.length + 1
    }
  },

  methods: {
    ...mapActions('controles',['addType', 'loadTypes']),
    ...mapActions('appareils',['loadTypesAppareils']),
    ...mapActions('notifications',['showNotification']),
    ...mapActions('etapes',['addEtapes']),

    validParametres(){
      this.showNotification({message: 'Paramètres ajoutés', type: 'success'});
    },
    addField() {
      this.typeControle.structure_formulaire.push({ name: '', type: '' });
    },
    removeField(index) {
      this.typeControle.structure_formulaire.splice(index, 1);
    },
    rows(rows) {
      this.formRows = rows;
    },
    submitForm(){
      this.formRows.forEach((row) => {
        this.addEtapes(row);
      });
      const typeData = {
        nom: this.typeControle.nom,
        structure_formulaire: this.typeControle.structure_formulaire,
        type_appareil: this.typeControle.type_appareil.id,
      }
      this.addType(typeData);
      this.formRows = [];
      this.typeControle.nom = '';
      this.typeControle.type_appareil = '';
      this.typeControle.structure_formulaire = [];
      this.loadTypes();
    }
  },
};
</script>






