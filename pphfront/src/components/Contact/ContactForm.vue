<template>
  <q-dialog v-model="showForm" persistent>
    <q-card>
      <q-toolbar>
          <q-toolbar-title><span class="text-cyan-4">Contactez-nous !</span></q-toolbar-title>
          <q-btn flat round icon="close" class="hover-effect" v-close-popup />
        </q-toolbar>
      <q-card-section class="q-pt-none">
        <q-form @submit="submitForm">
          <q-input
            v-model="message"
            label="Message"
            icon="message"
            required
          />
          <div class="row justify-center">
            <q-btn glossy rounded class="btn-grey-success-pph q-my-sm" icon="send" type="submit"/>
          </div>
        </q-form>
      </q-card-section>

    </q-card>
  </q-dialog>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex';
export default {

  computed: {
    ...mapState('contact', ['contactData']),
    ...mapGetters('auth', ['user']),

    message: {
      get() {
        return this.contactData.message;
      },
      set(value) {
        this.$store.commit('contact/SET_CONTACT_DATA', { ...this.contactData, message: value });
      }
    },

    showForm: {
      get() {
        return this.$store.state.contact.showForm;
      },
      set(value) {
        this.$store.commit('contact/SET_SHOW_FORM', value);
      }
    }
  },

  methods: {
    
    ...mapActions('contact', ['submitContactForm']),

    async submitForm() {
      let formData = {
        name: this.user.firstName + ' ' + this.user.lastName, // Utilisez les données utilisateur depuis le store
        email: this.user.email,
        message: this.message
      };

      await this.submitContactForm(formData);
      // Vous devrez peut-être modifier la méthode submitContactForm pour qu'elle accepte des données en tant qu'argument
    },
  }
};
</script>

<style scoped>
.floating-button {
  position: fixed;
  bottom: 60px; /* ou la marge que vous souhaitez depuis le bas de l'écran */
  right: 10px; /* ou la marge que vous souhaitez depuis le côté droit de l'écran */
  z-index: 10000; /* assurez-vous qu'il passe par-dessus les autres éléments, ajustez si nécessaire */
}
</style>
