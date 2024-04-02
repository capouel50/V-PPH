<template>
  <q-page class="row justify-center">
    <div class="col-8" >
      <div class="row text-purple-4 text-h6 justify-center">
        <div class="q-mt-sm">Assistant V-PPH</div>
      </div>
      <div class="row text-orange-4 text-subtitle2 text-italic justify-center">
        <div>Ne remplace pas une publication ou l'expertise d'un professionnel</div>
      </div>
      <div class="row justify-center">
        <q-input
          class="col-8"
          v-model="question"
          label="Posez votre question ici..."
          @keyup.enter="demande"
        >
          <template v-slot:append>
            <q-btn
            flat
            class="hover-effect-success"
            color="purple-4"
            size="md"
            icon="send"
            @click="demande"
          />
          </template>
        </q-input>
      </div>

        <div v-if="ask && !response" class="row justify-center q-mt-xl q-pt-xl">
            <atom-spinner
            class="bg-op-8"
            :animation-duration="1000"
            :size="70"
            :color="'#ff1d5e'"
          />
          </div>

        <q-card v-if="response" class="q-mt-md bg-op-8">
        <q-scroll-area
            :thumb-style="thumbStyle"
            :bar-style="barStyle"
            style="height: 350px;"
        >
        <q-card-section>
          <q-btn flat icon="restart_alt" color="purple-4" class="hover-effect absolute-top-right q-mt-sm" @click.stop="newGpt">
            <q-tooltip class="bg-blue-grey-4">Nouvelle conversation</q-tooltip>
          </q-btn>
          <div v-for="(message, index) in conversation" :key="index">
            <div class="text-purple-4 text-subtitle2">{{ message.role === 'user' ? user.firstName : 'V-PPH' }}:</div>
            <div class="q-mb-xs">{{ message.content }}</div>
          </div>
        </q-card-section>
        </q-scroll-area>
      </q-card>

    </div>
  </q-page>

</template>

<script>
import { mapActions, mapState, mapMutations, mapGetters } from 'vuex';
import {AtomSpinner} from 'epic-spinners'
export default {
  components: {
    AtomSpinner
  },
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
      question: '',
      ask: false,
      conversation: [],
    };
  },
  computed: {
    ...mapState('auth', ['user']),
    ...mapGetters('chatGPT', ['allHistory']),
    ...mapState('chatGPT', ['response', 'history']),

  },

  async created() {
    this.newChat();
  },

  methods: {
    ...mapActions('chatGPT', ['askQuestion', 'newChat', 'getHistory']),
    ...mapMutations('chatGPT', ['deleteResponse']),

    async demande() {
      if (this.question.trim()) {
        this.ask = true;
        await this.askQuestion(this.question);
        await this.getHistory();
        this.conversation = this.allHistory.conversation_history.slice().reverse();
        this.question = '';
        this.ask = false;
      }
    },

    newGpt(){
      this.newChat();
      this.question= '';
      this.deleteResponse();
      this.ask= false;
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