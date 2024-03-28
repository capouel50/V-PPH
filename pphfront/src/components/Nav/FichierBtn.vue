<template>
<div>
<q-btn :class="{ 'text-cyan-1': !menuOpen, 'text-cyan-4': menuOpen, 'hover-effect': true }" flat label="Fichier">
  <q-menu transition-show="jump-down" transition-hide="jump-up" @show="menuOpen = true" @hide="resetMenu">
    <q-list class="bg-blue-grey-4" dense style="min-width: 100px">

      <q-item clickable class="hover-effect" v-close-popup>
        <router-link class="pph-link" :to="`/user/${userId}`">
          <q-item-section class="text-cyan-1 hover-effect">Mon compte</q-item-section>
        </router-link>
      </q-item>

      <q-item clickable class="hover-effect" v-close-popup>
        <router-link class="pph-link" to="/users/">
          <q-item-section class="text-cyan-1 hover-effect">Utilisateurs</q-item-section>
        </router-link>
      </q-item>
      <q-separator />
      <q-item clickable class="hover-effect">
        <q-item-section :class="{ 'text-cyan-1': !submenuOpen, 'text-cyan-4': submenuOpen, 'hover-effect': true }">Paramètres</q-item-section>
        <q-item-section side>
          <q-icon name="keyboard_arrow_right" />
        </q-item-section>

        <q-menu anchor="top end" self="top start" @show="submenuOpen = true" @hide="submenuOpen = false">
          <q-list class="bg-blue-grey-3">
            <q-item clickable class="hover-effect" v-close-popup>
              <router-link class="pph-link" to="/etablissement/">
                <q-item-section class="text-cyan-1 hover-effect">Etablissement</q-item-section>
              </router-link>
            </q-item>
            <q-item clickable class="hover-effect" v-close-popup>
              <router-link class="pph-link" to="/unites-soin/">
                <q-item-section class="text-cyan-1 hover-effect">Unités de soin</q-item-section>
              </router-link>
            </q-item>
            <q-item clickable class="hover-effect" v-close-popup>
              <router-link class="pph-link" to="/users/">
                <q-item-section class="text-cyan-1 hover-effect">Utilisateurs</q-item-section>
              </router-link>
            </q-item>
            <q-item clickable class="hover-effect" v-close-popup>
              <router-link class="pph-link" to="/vpph-settings/">
                <q-item-section class="text-cyan-1 hover-effect">V-PPH</q-item-section>
              </router-link>
            </q-item>
          </q-list>
        </q-menu>

      </q-item>
      <q-separator />
      <q-item clickable v-close-popup>
        <q-item-section @click="resetApp" class="text-cyan-1 hover-effect">Réinitialisation</q-item-section>
      </q-item>
      <q-separator />
      <q-item class="logout" clickable v-close-popup>
        <q-item-section class="logout-text text-red-5">Fermer</q-item-section>
      </q-item>

    </q-list>
  </q-menu>
</q-btn>
</div>
</template>

<script>
import {mapActions, mapState} from "vuex";

export default {
  name: 'FichierBtn',
  data() {
    return {
      menuOpen: false,
      submenuOpen: false,
    };
  },
  computed: {
    ...mapState('auth',{
      userId: state => state.user.id
    })
  },

  methods: {
    ...mapActions('resetData', ['resetData']),
    resetMenu() {
      this.menuOpen = false;
      this.submenuOpen = false;
    },
    resetApp() {
      console.log('ResetApp');
      this.resetData();
    }
  }
}
</script>

