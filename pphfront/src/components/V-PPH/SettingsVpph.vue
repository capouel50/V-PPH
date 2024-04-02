<template>
  <q-page>
    <div clas="q-pa-md">
      <q-stepper
      v-model="step"
      class="bg-op-8"
      vertical
      done-color="cyan-4"
      active-color="orange-4"
      header-nav
      animated
    >
      <q-step
        :name="1"
        title="Profils"
        icon="person"
        :done="step > 1"
      >
        <div class="row">
          <q-list class="col-8">
          <q-item v-for="(profil, index) in profils" :key="index" class="row">
            <q-item-section class="col-4">
              <q-input
                label="Nom"
                v-model="profil.nom"
                color="cyan-4"
                class="hover-effect"
              />
            </q-item-section>
            <q-item-section class="col-6">
              <q-input
                autogrow
                label="Description"
                v-model="profil.description"
                color="cyan-4"
                class="hover-effect"
              />
            </q-item-section>
            <q-item-section side>
              <q-btn flat size="md" @click="removeLine(index)" icon="delete_forever" color="red-4"/>
            </q-item-section>
          </q-item>
        </q-list>
          <q-btn flat size="md" @click="addLine" icon="add_box" color="cyan-4" class="hover-effect" label="Ajouter"/>
          <q-btn v-if="profils.length > 0" flat size="md" @click="validProfils" icon="check_circle" color="green-4" label="Valider"/>
        </div>
        <q-stepper-navigation>
          <q-btn flat @click="step = 2" color="cyan-4" label="Suivant" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>
      <q-step
        :name="2"
        title="Compétences"
        icon="person"
        :done="step > 1"
      >
        <div class="row">
          <q-list class="col-8">
          <q-item v-for="(competence, index) in competences" :key="index" class="row">
            <q-item-section class="col-4">
              <q-input
                label="Nom"
                v-model="competence.nom"
                color="cyan-4"
                class="hover-effect"
              />
            </q-item-section>
            <q-item-section class="col-6">
              <q-input
                autogrow
                label="Description"
                v-model="competence.description"
                color="cyan-4"
                class="hover-effect"
              />
            </q-item-section>
            <q-item-section side>
              <q-btn flat size="md" @click="removeLineCompetences(index)" icon="delete_forever" color="red-4"/>
            </q-item-section>
          </q-item>
        </q-list>
          <q-btn flat size="md" @click="addLineCompetences" icon="add_box" color="cyan-4" class="hover-effect" label="Ajouter"/>
        </div>
        <q-stepper-navigation>
          <q-btn flat @click="step = 1" color="cyan-4" label="Précédent" class="hover-effect"/>
          <q-btn flat @click="step = 3" color="cyan-4" label="Suivant" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>
      <q-step
        :name="3"
        title="Situations"
        icon="person"
        :done="step > 3"
      >
        <q-stepper-navigation>
          <q-btn flat @click="step = 2" color="cyan-4" label="Précédent" class="hover-effect"/>
          <q-btn flat @click="step = 4" color="cyan-4" label="Suivant" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>
      <q-step
        :name="4"
        title="Personnas"
        icon="person"
        :done="step > 3"
      >
        <q-stepper-navigation>
          <q-btn flat @click="step = 5" color="cyan-4" label="Terminer" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>
      <div class="row justify-center">
        <q-btn-group>
          <q-btn flat @click="postVpph" color="green-4" label="Enregistrer" class="btn-flat-success-pph"/>
          <q-btn flat color="red-4" label="Supprimer" class="btn-flat-danger-pph"/>
        </q-btn-group>
      </div>
    </q-stepper>
    </div>
  </q-page>

</template>

<script>
import { mapActions, mapState, mapGetters } from 'vuex';
export default {
  data() {
    return {
      step: 1,
      vpph: [],
      profils: [],
      competences: [],
      situations: [],
      personnas: [],
    }
  },

  computed: {
    ...mapState('chatGPT', ['profil']),
    ...mapGetters('chatGPT', ['allProfils', 'getVpph']),
  },

  created(){
    this.loadVpph();
    this.vpph = this.getVpph;
    console.log('vpphload', this.getVpph);
    const vpph = this.vpph.find(v => v.id === 1);
    this.profils = vpph.profil;
    console.log('profils', this.profils);
  },

  methods: {
    ...mapActions('chatGPT', ['ajouterProfil', 'modifierProfil', 'loadVpph', 'saveVpph']),

    addLine() {
      this.profils.push({ nom: '', description: ''});
    },

    removeLine(index) {
      this.profils.splice(index, 1);
    },

    addLineCompetences() {
      this.competences.push({ nom: '', description: ''});
    },

    removeLineCompetences(index) {
      this.competences.splice(index, 1);
    },

    validProfils(){
      this.profils.forEach((profil) => {
        const existingProfil = this.allProfils.find(p => p.nom === profil.nom);
        if(existingProfil) {
          // Profil déjà existant : mettre à jour
          this.modifierProfil({ index: this.allProfils.indexOf(existingProfil), profil });
          console.log('profilModif', profil)
        } else {
          // Profil non trouvé : ajouter
          this.ajouterProfil(profil);
          console.log('profilAjout', profil)
        }
      });
      console.log('profils', this.allProfils);
    },

    postVpph(){
      const formData = {
        profil: this.profils,
        competences: this.competences,
      };
      console.log('vpph', formData);
      console.log('getvpph', this.getVpph);
      const id = 1;
      this.saveVpph({id, formData});
    }
  },

}
</script>