<template>
  <div class="row">
     <q-list bordered class="col-6" v-if="rows.length > 0">
       <q-item v-for="(row, index) in rows" :key="index" class="row">
         <q-item-section>
           <q-select
            :label="row.epi ? 'Epi n° ' + (index + 1) : 'Ajouter un Epi'"
            v-model="row.epi"
            color="cyan-4"
            class="hover-effect"
            :options="epis"
            option-label="nom"
            option-value="id"
           >
            <template v-slot:append v-if="!row.epi">
              <q-btn flat @click="epiDialog=true" icon="add_box" color="green-4" class="q-px-none hover-effect"/>
            </template>
           </q-select>
           <q-dialog v-model="epiDialog">
      <q-card>
        <q-card-section>
          <div class="row text-subtitle1 text-cyan-4 justify-center">
            Créer un epi
          </div>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <q-input
            v-model="newEpi"
            label="Nom"
            color ='cyan-4'
            @mouseover="changeLabelColor('nameInput','#ffb74d')"
            @mouseleave="changeLabelColor('nameInput','')"
            @focus="onFocus('name','#4dd0e1')"
            @blur="onBlur('name')"
          />
        </q-card-section>
        <q-separator/>
        <div class="row justify-center">
        <q-btn flat @click="creerEpi" label="Ajouter" color="green-4"/>
        <q-btn flat @click="epiDialog=false" label="Annuler" color="red-4"/>
        </div>
      </q-card>
     </q-dialog>
         </q-item-section>
         <q-item-section side>
           <q-btn flat size="md" @click="removeLine(index)" icon="delete_forever" color="red-4"/>
         </q-item-section>
       </q-item>
     </q-list>
    <q-btn flat size="md" @click="addLine" icon="add_box" color="cyan-4" class="hover-effect" label="Ajouter"/>
    <q-btn v-if="rows.length > 0" flat size="md" @click="validRows" icon="check_circle" color="green-4" label="Valider"/>
  </div>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from 'vuex';

export default {
  props: ['newId', 'formuleId', 'episRows'],
  data() {
    return {
      epiDialog: false,
      selectedRowIndex: null,
      newEpi: null,
      epis: [],
      rows: [
        {
          num_formule: null,
          epi: null,
        }
      ],
    };
  },
  computed: {
    ...mapGetters('epi', ['allEpis', 'allEpisFormules']),

  },

  async created() {
    this.epis = this.allEpis;
    this.rows = this.episRows;
    console.log('epis', this.epis);
  },

  methods: {
    ...mapActions('epi', ['addEpi', 'loadEpis']),
    ...mapMutations('epi', ['SET_EPI_FORMULES', 'SET_EPI']),
    ...mapActions('notifications', ['showNotification']),

    async creerEpi(){
      const formData = {
        nom: this.newEpi,
      };
      await this.addEpi(formData);
      await this.loadEpis;
      this.epis = this.allEpis;
      this.epiDialog = false;
    },

    updateEpisRows() {
      this.$emit('episRows', this.rows);
    },

    validRows(){
      this.updateEpisRows();
      this.showNotification({message: 'Epis ajoutés', type: 'success'});
    },

    addLine() {
      let id = this.allEpisFormules.length + 1;
      if(this.formuleId) {
        this.rows.push({id: id, num_formule: this.formuleId, epi: ''});
      }else{
        this.rows.push({id: id, num_formule: this.newId, epi: ''});
      }
      this.updateEpisRows();
    },

    removeLine(index) {
      this.rows.splice(index, 1);
      this.updateEpisRows();
    },
  },
};
</script>


