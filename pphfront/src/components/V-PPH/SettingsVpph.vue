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
        Step 1
      </q-step>
      <q-step>
        Step 2
      </q-step>
      <q-step>
        Step 3
      </q-step>
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