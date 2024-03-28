<template>
  <div class="row">
    <div class="col-12">

    <div
      v-for="(row, index) in formRows"
      :key="index"
      class="row"
    >
      <div class="col-1 q-mr-md">
        <q-input
        v-model="row.action"
        color="cyan-4"
        label="Action"
      />
      </div>
      <div class="col-5 q-mr-md">
        <q-input
        v-model="row.description"
        color="cyan-4"
        label="Description"
      />
      </div>
      <div class="col-1 q-mr-md">
        <q-input
        v-model="row.nom"
        color="cyan-4"
        label="Nom"
      />
      </div>
      <div class="col-1">
        <q-input
        v-model="row.instruction"
        color="cyan-4"
        label="Instruction"
      />
      </div>
      <div class="col-2 q-mt-md q-ml-smm">
        <q-toggle
          v-model="row.button"
          color="green-4"
          label="Bouton"
        />
      </div>

      <q-btn-group flat class="q-mt-sm">
        <q-btn
            flat
            size="sm"
            icon="compare_arrows"
            class="hover-effect-success"
            color="cyan-4"
            @click.stop="editReponse(row)"
        >
          <q-tooltip>Réponses</q-tooltip>
        </q-btn>
        <q-btn flat size="sm" @click="addInstructionState(row)" icon="check_circle" color="green-4"/>
        <q-btn flat size="sm" @click="removeRow(row)" icon="delete_forever" color="red-4"/>
      </q-btn-group>
      <q-dialog v-model="reponseDialog" full-width>
          <q-card>
            <q-card-section>
              <div class="row text-cyan-4 text-h6 justify-center">
                Réponses à l'instruction
              </div>
              <div class="row text-orange-4 text-subtitle1 justify-center">
                {{ currentRow.action }} ({{ currentRow.nom }})
              </div>
              <div class="row text-italic justify-center">
                ({{ currentRow.description }})
              </div>
            </q-card-section>

            <q-separator/>

            <q-card-section>
            <div
              v-for="(reponseRow, index) in reponseRows"
              :key="index"
              class="row"
            >
              <q-input
                  class="col-2 q-mr-md"
                  color="cyan-4"
                  label="Nom"
                  v-model="reponseRow.nom"
              />
              <q-input
                  class="col-3 q-mr-md"
                  color="cyan-4"
                  label="Format"
                  v-model="reponseRow.format"
              />
              <q-input
                  class="col-3 q-mr-md"
                  color="cyan-4"
                  label="Message"
                  v-model="reponseRow.message"
              />
              <q-toggle
                  class="col-2 q-pt-sm"
                  color="red-4"
                  v-model="reponseRow.erreur"
                  icon="error"
                  label="Erreur"
              />
              <q-btn-group flat class="q-pa-xs">
                <q-btn flat size="sm" @click="addInstructionState(row)" icon="check_circle" color="green-4"/>
                <q-btn flat size="sm" @click="removeRow(row)" icon="delete_forever" color="red-4"/>
              </q-btn-group>
            </div>
            </q-card-section>

            <q-separator/>
            <div class="row justify-center">
              <q-btn flat label="Valider" color="green-4" @click="reponseDialog=false"/>
              <q-btn flat label="Annuler" color="red-4" @click="reponseDialog=false"/>
            </div>
          </q-card>
        </q-dialog>
    </div>

    </div>
  </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations} from 'vuex';

export default {
  props: ['newId', 'appareilId', 'instructions', 'reponses'],
  data() {
    return {
      currentRow: null,
      reponseDialog: false,
      formRows: [
        {
          num_appareil: null,
          instructionId: null,
          nom: null,
          action: null,
          instruction: null,
          description: null,
          reponse: null,
          button: false,
        }
      ],
      reponseRows: [
        {
          num_instruction: null,
          reponseId: null,
          nom: null,
          format: null,
          message: null,
          erreur: false,
        }
      ],
    };
  },
  computed: {
    ...mapGetters('appareils', ['allAppareils', 'allInstructionsAppareils']),

  },

  async created() {
    console.log('instructions', this.instructions);
    console.log('reponses', this.reponses);
      this.loadLastId();
      this.fetchInstructionsAndAddRow();
      if(this.appareilId){
          this.formRows = this.instructions
            .filter(instruction => instruction.modele_appareil === this.appareilId)
            .map(instruction => ({
              num_appareil: instruction.modele_appareil,
              instructionId: instruction.id,
              instruction: instruction.instruction,
              nom: instruction.nom,
              action: instruction.action,
              description: instruction.description,
              reponse: instruction.format_reponse,
              button: instruction.button,
            }));
          this.addRow();
        }
    },

  methods: {
    ...mapActions('appareils', ['loadAppareils', 'loadInstructionsAppareils', 'loadReponses']),
    ...mapMutations('appareils', ['ADD_INSTRUCTION', 'REMOVE_INSTRUCTION']),

    async editReponse(row){
       if (row.instructionId) {
          try {
            this.currentRow = row;
            this.reponseRows = this.reponses
            .filter(reponse => reponse.num_instruction === row.instructionId)
            .map(reponse => ({
              num_instruction: reponse.num_instruction,
              reponseId: reponse.id,
              nom: reponse.nom,
              format: reponse.format,
              message: reponse.message,
              erreur: reponse.erreur,
            }));
            this.addReponseRow(row.instructionId)
          } catch (error) {
            console.error('Erreur lors de la récupération des instructions', error);
          }
       }
      this.reponseDialog = true;
    },

    async fetchInstructionsAndAddRow() {
        if (!this.appareilId) {
          try {
            const instructions = await this.getInstructions();
            if (instructions.length > 0) {
              this.formRows = instructions.map((instruction) => ({
                num_appareil: instruction.modele_appareil,
                instructionId: instruction.id,
                instruction: instruction.instruction,
                nom: instruction.nom,
                action: instruction.action,
                description: instruction.description,
                reponse: instruction.format_reponse,
                button: instruction.button,
              }));
              this.addRow();
            }
          } catch (error) {
            console.error('Erreur lors de la récupération des instructions', error);
          }
        }
      },

    async getInstructions() {
      const numAppareil = this.newId;

      return this.instructions.filter(instruction => instruction.modele_appareil === numAppareil);
    },

    async loadLastId() {
      try {
        this.formRows[0].num_appareil = this.newId;
        console.log('NewId', this.newId)
      } catch (error) {
        console.error('Erreur lors de la récupération du dernier ID de la formule', error);
      }
    },

    async addRow() {
      try {
        if(this.appareilId){
          this.formRows.push({
          num_appareil: this.appareilId,
          instructionId: null,
          nom: null,
          action: null,
          instruction: null,
          description: null,
          reponse: null,
          button: false,
        });
        }else {
          this.formRows.push({
          num_appareil: this.newId,
          instructionId: null,
          nom: null,
          action: null,
          instruction: null,
          description: null,
          reponse: null,
          button: false,
          });
        }
      } catch (error) {
        console.error('Erreur lors de la récupération du dernier ID du modèle Formule', error);
      }
    },

    async addReponseRow(instructionId) {
      try {
        if(instructionId){
          this.reponseRows.push({
          num_instruction: instructionId,
          reponseId: null,
          nom: null,
          format: null,
          message: null,
          erreur: false,
        });
        }else {
          this.reponseRows.push({
          num_instruction: instructionId,
          reponseId: null,
          nom: null,
          format: null,
          message: null,
          erreur: false,
          });
        }
      } catch (error) {
        console.error('Erreur lors de la récupération du dernier ID du modèle Formule', error);
      }
    },

    addInstructionState(row) {
        this.ADD_INSTRUCTION({
          num_appareil: this.appareilId,
          instructionId: null,
          nom: null,
          action: null,
          instruction: null,
          description: null,
          reponse: null,
          button: false,
        });
      if(this.formRows.indexOf(row) === this.formRows.length - 1) {
        this.addRow();
      }
    },

    removeRow(row) {
      this.REMOVE_INSTRUCTION({
        num_appareil: row.num_appareil,
        instructionId: row.instructionId,
      });
      // Supprime la ligne qui contient le bouton
      const index = this.formRows.indexOf(row);
      this.formRows.splice(index, 1);
    },

  },
};
</script>


