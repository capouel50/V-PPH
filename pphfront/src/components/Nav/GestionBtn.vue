<template>
<div>
<q-btn :class="{ 'text-cyan-1': !menuOpen, 'text-cyan-4': menuOpen, 'hover-effect': true }" flat label="Gestion">
  <q-menu transition-show="jump-down" transition-hide="jump-up" @show="menuOpen = true" @hide="resetMenu">
    <q-list class="bg-blue-grey-4" dense style="min-width: 100px">
      <q-item clickable v-close-popup class="hover-effect">
        <router-link to="/suppliers/" class="pph-link">
          <q-item-section class="text-cyan-1 hover-effect">Fournisseurs</q-item-section>
        </router-link>
      </q-item>

      <q-item clickable class="hover-effect">
        <q-item-section :class="{ 'text-cyan-1': !submenuOpen7, 'text-cyan-4': submenuOpen7, 'hover-effect': true }">Matériel</q-item-section>
        <q-item-section side>
          <q-icon name="keyboard_arrow_right" />
        </q-item-section>

        <q-menu anchor="top end" self="top start" @show="submenuOpen7 = true" @hide="submenuOpen7 = false">
          <q-list class="bg-blue-grey-3">
            <q-item clickable v-close-popup class="hover-effect">
              <router-link to="/materiel/" class="pph-link">
                <q-item-section class="text-cyan-1 hover-effect">Matériel</q-item-section>
              </router-link>
            </q-item>
            <q-item clickable v-close-popup class="hover-effect">
              <router-link to="/appareils/" class="pph-link">
                <q-item-section class="text-cyan-1 hover-effect">Appareils</q-item-section>
              </router-link>
            </q-item>
          </q-list>
        </q-menu>
      </q-item>

      <q-item clickable class="hover-effect">
        <q-item-section :class="{ 'text-cyan-1': !submenuOpen, 'text-cyan-4': submenuOpen, 'hover-effect': true }">Mat.premières</q-item-section>
        <q-item-section side>
          <q-icon name="keyboard_arrow_right" />
        </q-item-section>

        <q-menu anchor="top end" self="top start" @show="submenuOpen = true" @hide="submenuOpen = false">
          <q-list class="bg-blue-grey-3">
            <q-item clickable v-close-popup class="hover-effect">
              <router-link to="/creation-matiere-premiere/" class="pph-link">
                <q-item-section class="text-cyan-1 hover-effect">Créer</q-item-section>
              </router-link>
            </q-item>
            <q-item clickable v-close-popup class="hover-effect">
              <router-link to="/matieres-premieres/" class="pph-link">
                <q-item-section class="text-cyan-1 hover-effect">Préparatoire</q-item-section>
              </router-link>
            </q-item>
            <q-item clickable class="hover-effect" v-close-popup>
              <router-link to="/catalogue/" class="pph-link">
                <q-item-section class="text-cyan-1 hover-effect">Catalogue</q-item-section>
              </router-link>
            </q-item>
          </q-list>
        </q-menu>
      </q-item>

      <q-item clickable class="hover-effect">
        <q-item-section :class="{ 'text-cyan-1': !submenuOpen2, 'text-cyan-4': submenuOpen2, 'hover-effect': true }">Formules</q-item-section>
        <q-item-section side>
          <q-icon name="keyboard_arrow_right" />
        </q-item-section>

        <q-menu anchor="top end" self="top start" @show="submenuOpen2 = true" @hide="submenuOpen2 = false">
          <q-list class="bg-blue-grey-3">
            <q-item clickable class="hover-effect" v-close-popup>
              <router-link to="/nouvelle-formule/" class="pph-link">
                <q-item-section class="text-cyan-1 hover-effect">Créer</q-item-section>
              </router-link>
            </q-item>
            <q-item clickable class="hover-effect" v-close-popup>
              <router-link to="/formules/" class="pph-link">
                <q-item-section class="text-cyan-1 hover-effect">Formules référencées</q-item-section>
              </router-link>
            </q-item>
            <q-item clickable class="hover-effect" v-close-popup>
              <q-item-section class="text-cyan-1 hover-effect">PPH-Cloud</q-item-section>
            </q-item>
          </q-list>
        </q-menu>
      </q-item>

      <q-item clickable class="hover-effect">
        <q-item-section :class="{ 'text-cyan-1': !submenuOpen8, 'text-cyan-4': submenuOpen8, 'hover-effect': true }">Controles</q-item-section>
        <q-item-section side>
          <q-icon name="keyboard_arrow_right" />
        </q-item-section>

        <q-menu anchor="top end" self="top start" @show="submenuOpen8 = true" @hide="submenuOpen8 = false">
          <q-list class="bg-blue-grey-3">
            <q-item clickable class="hover-effect" v-close-popup>
              <router-link :to="{name: 'CreateControles'}" class="pph-link">
                <q-item-section class="text-cyan-1 hover-effect">Créer</q-item-section>
              </router-link>
            </q-item>
            <q-item clickable class="hover-effect" v-close-popup>
              <router-link :to="{name: 'ControlesCards'}" class="pph-link">
                <q-item-section class="text-cyan-1 hover-effect">Contrôles disponibles</q-item-section>
              </router-link>
            </q-item>
          </q-list>
        </q-menu>
      </q-item>

      <q-item clickable class="hover-effect">
        <q-item-section :class="{ 'text-cyan-1': !submenuOpen4, 'text-cyan-4': submenuOpen4, 'hover-effect': true }">Stock</q-item-section>
        <q-item-section side>
          <q-icon name="keyboard_arrow_right" />
        </q-item-section>

        <q-menu anchor="top end" self="top start" @show="submenuOpen4 = true" @hide="submenuOpen4 = false">
          <q-list class="bg-blue-grey-3">
            <q-item clickable class="hover-effect" v-close-popup>
              <router-link to="/stock-preparatoire/" class="pph-link">
                <q-item-section class="text-cyan-1 hover-effect">Péparatoire</q-item-section>
              </router-link>
            </q-item>
            <q-item clickable class="hover-effect" v-close-popup>
              <router-link to="/commande/" class="pph-link">
                <q-item-section class="text-cyan-1 hover-effect">Commandes</q-item-section>
              </router-link>
            </q-item>
            <q-item clickable class="hover-effect" v-close-popup>
              <router-link to="/reception/" class="pph-link">
                <q-item-section class="text-cyan-1 hover-effect">Livraisons</q-item-section>
              </router-link>
            </q-item>
            <q-item clickable class="hover-effect" v-close-popup>
              <router-link to="/reception/" class="pph-link">
                <q-item-section class="text-cyan-1 hover-effect">Historique des livraisons</q-item-section>
              </router-link>
            </q-item>
            <q-item clickable class="hover-effect" v-close-popup>
              <router-link to="/reception/" class="pph-link">
                <q-item-section class="text-cyan-1 hover-effect">Inventaire</q-item-section>
              </router-link>
            </q-item>
          </q-list>
        </q-menu>
      </q-item>

      <q-item clickable class="hover-effect">
        <q-item-section :class="{ 'text-cyan-1': !submenuOpen6, 'text-cyan-4': submenuOpen6, 'hover-effect': true }">Tarification</q-item-section>
        <q-item-section side>
          <q-icon name="keyboard_arrow_right" />
        </q-item-section>

        <q-menu anchor="top end" self="top start" @show="submenuOpen6 = true" @hide="submenuOpen6 = false">
          <q-list class="bg-blue-grey-3">
            <q-item clickable class="hover-effect" v-close-popup>
              <q-item-section class="text-cyan-1 hover-effect">Paramètres</q-item-section>
            </q-item>
            <q-item clickable class="hover-effect" v-close-popup>
              <q-item-section class="text-cyan-1 hover-effect">Générer facture</q-item-section>
            </q-item>
          </q-list>
        </q-menu>
      </q-item>

      <q-item clickable class="hover-effect">
        <q-item-section :class="{ 'text-cyan-1': !submenuOpen5, 'text-cyan-4': submenuOpen5, 'hover-effect': true }">Statistiques</q-item-section>
        <q-item-section side>
          <q-icon name="keyboard_arrow_right" />
        </q-item-section>

        <q-menu anchor="top end" self="top start" @show="submenuOpen5 = true" @hide="submenuOpen5 = false">
          <q-list class="bg-blue-grey-3">
            <q-item clickable class="hover-effect" v-close-popup>
              <q-item-section class="text-cyan-1 hover-effect">Bilan</q-item-section>
            </q-item>
            <q-item clickable class="hover-effect" v-close-popup>
              <q-item-section class="text-cyan-1 hover-effect">Requêtes</q-item-section>
            </q-item>
          </q-list>
        </q-menu>
      </q-item>

    </q-list>
  </q-menu>
</q-btn>
</div>
</template>

<script>
export default {
  name: 'GestionBtn',
  data() {
    return {
      menuOpen: false,
      submenuOpen: false,
      submenuOpen2: false,
      submenuOpen3: false,
      submenuOpen4: false,
      submenuOpen5: false,
      submenuOpen6: false,
      submenuOpen7: false,
    };
  },
  methods: {
    resetMenu() {
      this.menuOpen = false;
      this.submenuOpen = false;
      this.submenuOpen2 = false;
      this.submenuOpen3 = false;
      this.submenuOpen4 = false;
      this.submenuOpen5 = false;
      this.submenuOpen6 = false;
      this.submenuOpen7 = false;
    }
  }
}
</script>