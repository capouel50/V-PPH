<template>
      <div class="row">
        <q-list bordered class="col-3" v-if="rows.length > 0">
          <q-item v-for="(row, index) in rows" :key="index" class="row">
            <q-item-section>
              <q-select
                :label="row.controle ? 'Contrôle n° ' + (index + 1) : 'Ajouter un contrôle'"
                v-model="row.controle"
                color="cyan-4"
                class="hover-effect"
                :options="controles"
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
import { mapActions, mapGetters } from 'vuex';

export default {
  props: ['controlesRows'],
  data() {
    return {
      controles: [],
      rows: [],
    };
  },
  computed: {
    ...mapGetters('controles', ['allTypesControles']),
  },

  async created() {
    await this.loadTypes();
    this.controles = this.allTypesControles;
    this.rows = this.controlesRows;
    console.log('controles', this.allTypesControles);
  },

  methods: {
    ...mapActions('controles', ['loadTypes']),
    ...mapActions('notifications', ['showNotification']),

    updateControlesRows() {
      this.$emit('controleRows', this.rows);
    },

    validRows(){
      this.updateControlesRows();
      this.showNotification({message: 'Contrôles ajoutés', type: 'success'});
    },

    addLine() {
      this.updateControlesRows();
      this.rows.push({ controle: ''});
      console.log('rows', this.rows);
    },
    removeLine(index) {
      this.rows.splice(index, 1);
      this.updateControlesRows();
    },


  },
};
</script>


