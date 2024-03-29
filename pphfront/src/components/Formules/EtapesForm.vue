<template>
      <div class="row">
        <q-list bordered class="col-8" v-if="rows.length > 0">
          <q-item v-for="(row, index) in rows" :key="index" class="row">
            <q-item-section class="col-4">
              <q-input
                label="Nom"
                v-model="row.nom"
                color="cyan-4"
                class="hover-effect"
              />
            </q-item-section>
            <q-item-section>
              <q-input
                autogrow
                label="Description"
                v-model="row.description"
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
          <q-btn v-if="rows.length > 0" flat size="md" @click="validFormRows" icon="check_circle" color="green-4" label="Valider"/>
          <q-btn v-if="!ask" flat class="hover-effect fade-blink" size="md" color="purple-4" label="V-PPH" @click.stop="GptMod"/>
          <div v-if="ask && !response" class="row justify-center items-center q-px-md">
            <atom-spinner
            class="bg-op-8"
            :animation-duration="1000"
            :size="40"
            :color="'#ff1d5e'"
          />
          </div>
        <q-card v-if="response" class="col-8 bg-op-8">
          <q-card-section class="row justify-center">
            <div class="col-4">
              <q-input
              v-model="question"
              label="Effectuer une demande"
              @keyup.enter="GptMod"
            >
            <template v-slot:append>
              <q-btn
              flat
              color="purple-4"
              class="hover-effect-success"
              size="md"
              icon="send"
              @click="GptMod"
            />
            </template>
            </q-input>
            </div>
          </q-card-section>
         <q-card-section>
            <div class="text-subtitle1 text-purple-4">Mode opératoire suggéré (à titre informatif) :</div>
             <q-list>
               <q-scroll-area
                  :thumb-style="thumbStyle"
                  :bar-style="barStyle"
                  style="height: 300px;"
                >
               <q-item v-for="(etape, index) in etapes" :key="index" class="q-mb-md">
                <q-item-section>
                  <q-item-label class="text-subtitle1 text-cyan-4">{{ etape.title }}</q-item-label>
                  <q-item-label caption class="text-subtitle2">{{ etape.description }}</q-item-label>
                </q-item-section>
                 <q-btn flat icon="add_box" size="sm" color="purple-4" class="hover-effect" @click.stop="addEtape(index)"/>
              </q-item>
             </q-scroll-area>
             </q-list>
         </q-card-section>
         <q-card-section class="row justify-center">
           <q-btn flat class="hover-effect" size="md" color="green-4" label="Ajouter" @click.stop="addGptModOp"/>
           <q-btn flat class="hover-effect" size="md" color="red-4" label="Fermer" @click.stop="closeGpt"/>
          </q-card-section>
        </q-card>
      </div>
</template>

<script>
import { mapActions, mapGetters, mapState, mapMutations } from 'vuex';
import {AtomSpinner} from 'epic-spinners'
export default {
  components: {
    AtomSpinner
  },
  props: ['newId', 'formuleId', 'controleId', 'etapesRows', 'name', 'prep', 'compoRows'],
  data() {
    return {
      thumbStyle: {
        right: '4px',
        borderRadius: '5px',
        backgroundColor: '#027be3',
        width: '5px',
        opacity: 0.75
      },

      barStyle: {
        right: '2px',
        borderRadius: '9px',
        backgroundColor: '#027be3',
        width: '9px',
        opacity: 0.2
      },
      rows: [],
      question: '',
      context: '',
      result: '',
      etapes: [],
      ask: false,
    };
  },
  computed: {
    ...mapGetters('etapes', ['allEtapes']),
    ...mapState('chatGPT', ['response']),

  },

  async created() {
    this.rows = this.etapesRows;
    this.newChat();
    this.question = '';
  },

  methods: {
    ...mapActions('notifications', ['showNotification']),
    ...mapActions('chatGPT', ['askQuestion', 'newChat']),
    ...mapMutations('chatGPT', ['deleteResponse']),

    async GptMod() {
      const formule = this.prep + ' de ' + this.name;
      const matieresString = this.compoRows.map(compoRow => `${compoRow.matiere.nom} ${compoRow.matiere.forme.nom}(${compoRow.matiere.type.nom}) `).join(', ');
      console.log('compo', matieresString);
      const message = 'Pour une ' + formule + ' dont les composants sont ' + matieresString +
          '. Ton mode opératoire doit contenir uniquement les composants fournis. ' +
          'donne moi un mode opératoire impérativement sous forme d\'étapes pour chaque composants. ' +
          'Chaque étape doit comporter un titre contenu entre deux *' +
          'Ta réponse ne doit comporter que les étapes et préciser le matériel utilisé.'
      this.context = message;
      if (this.question.trim()) {
        await this.askQuestion(this.question);
      }else{
        this.ask = true;
        await this.askQuestion(this.context);
        this.ask = false;
      }

      const regex = /\*([^*]+)\*\n?([^*]+)/g;
      let etapesListe = [];
      let match;

      while ((match = regex.exec(this.response)) !== null) {
        let titreComplet = match[1].trim();
        let titre = titreComplet.replace(/^[^:-]+[-:]\s*/, "");
        let description = match[2].trim().replace(/\n/g, " "); // Remplacer les sauts de ligne par des espaces
        etapesListe.push({ title: titre, description: description });
      }
      console.log('etapes', etapesListe);
      this.etapes = etapesListe;
      this.question='';
    },

    addEtape(index){
      let newEtape = this.etapes[index];
      if (newEtape) {
        this.updateFormRows();
        // Structure conditionnelle basée sur le nom de la route actuelle
        if (this.$route.name === 'CreateControles') {
          this.rows.push({ num: 'c' + this.newId, nom: newEtape.title, description: newEtape.description });
        } else {
          this.rows.push({ num: 'f' + this.newId, nom: newEtape.title, description: newEtape.description });
        }

      }
    },

    addGptModOp(){
      this.etapes.forEach((newEtape) => {
        if (newEtape) {
          this.updateFormRows();
          // Structure conditionnelle basée sur le nom de la route actuelle
          if (this.$route.name === 'CreateControles') {
            this.rows.push({ num: 'c' + this.newId, nom: newEtape.title, description: newEtape.description });
          } else {
            this.rows.push({ num: 'f' + this.newId, nom: newEtape.title, description: newEtape.description });
          }
        }
      });
      this.question = '',
      this.newChat();
      this.deleteResponse();
    },

    closeGpt(){
      this.newChat();
      this.deleteResponse();
    },

    updateFormRows() {
      this.$emit('etapesRows', this.rows);
    },

    validFormRows(){
      this.updateFormRows();
      this.showNotification({message: 'Etapes ajoutées', type: 'success'});
    },

    addLine() {
      if(this.$route.name === 'CreateControles'){
        this.updateFormRows();
        this.rows.push({ num: 'c' + this.newId, nom: '', description: ''});
      }else {
        this.updateFormRows();
        this.rows.push({ num: 'f' + this.newId, nom: '', description: ''});
      }
    },
    removeLine(index) {
      this.rows.splice(index, 1);
      this.updateFormRows();
    },


  },
};
</script>

<style>
.scroll-container {
    max-height: 300px; /* ou toute autre valeur selon vos besoins */
    overflow-y: auto;
}
</style>

