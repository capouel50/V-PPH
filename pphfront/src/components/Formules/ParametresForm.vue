<template>
  <div class="row">
     <q-list bordered class="col-3" v-if="rows.length > 0">
       <q-item v-for="(row, index) in rows" :key="index" class="row">
         <q-item-section>
           <q-select
            :label="row.parametre ? 'Parametre n° ' + (index + 1) : 'Ajouter un paramètre'"
            v-model="row.parametre"
            color="cyan-4"
            class="hover-effect"
            :options="parametres"
            option-label="nom"
            option-value="id"
          />
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
import {mapActions, mapGetters } from 'vuex';

export default {
  props: ['newId', 'formuleId', 'parametresRows'],
  data() {
    return {
      parametre: "",
      unite: '',
      parametreDialog: false,
      selectedRowIndex: null,
      rows: [
        {
          num_formule: '',
          parametre: '',
          unite: '',
        }
      ],
      parametres: [],
    };
  },
  computed: {
    ...mapGetters('formules', ['allParametres', 'allParametresFormules']),

  },

  async created() {
      this.parametres =  this.allParametres.map(parametre => ({
        nom: `${parametre.nom} - ${parametre.unite}`,
        id: parametre.id
      }));
      this.rows = this.parametresRows;
    },

  methods: {
    ...mapActions('formules', ['loadParametres', 'loadParametresFormules', 'addParametre']),

    updateParametresRows() {
      this.$emit('parametresRows', this.rows);
    },

    validRows(){
      this.updateParametresRows();
      this.showNotification({message: 'Parametres ajoutés', type: 'success'});
    },

    addLine() {
      this.updateParametresRows();
      if(this.formuleId) {
        this.rows.push({num_formule: this.formuleId, parametre: ''});
      }else{
        this.rows.push({num_formule: this.newId, parametre: ''});
      }
      console.log('rows', this.rows);
    },

    removeLine(index) {
      this.rows.splice(index, 1);
      this.updateParametresRows();
    },

  },
};
</script>


