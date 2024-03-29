<template>
  <q-page>
    <q-stepper
      v-model="step"
      class="bg-op-8"
      vertical
      done-color="cyan-4"
      active-color="orange-4"
      header-nav
      animated
    >
      <q-step>
        <q-stepper-navigation>
          <q-btn flat @click="step = 2" color="cyan-4" label="Suivant" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>
      <div class="row justify-center">
        <q-btn-group>
          <q-btn flat @click="submitForm" color="green-4" label="Enregistrer" class="btn-flat-success-pph"/>
          <q-btn flat color="red-4" label="Supprimer" class="btn-flat-danger-pph"/>
        </q-btn-group>
      </div>
    </q-stepper>
  </q-page>

</template>

<script>
import { mapActions, mapState, mapGetters } from 'vuex';
export default {
  data() {
    return {
      step: 1,
      profils: [],
    }
  },

  computed: {
    ...mapState('chatGPT', ['profil']),
    ...mapGetters('chatGPT', ['allProfils']),
  },

  methods: {
    ...mapActions('chatGPT', ['ajouterProfil', 'modifierProfil']),
  },
}
</script>