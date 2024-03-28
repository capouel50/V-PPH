<template>
  <div class="row">
     <q-list bordered class="col-3" v-if="rows.length > 0">
       <q-item v-for="(row, index) in rows" :key="index" class="row">
         <q-item-section>
           <q-select
            :label="row.article ? 'Article n° ' + (index + 1) : 'Ajouter un article'"
            v-model="row.article"
            color="cyan-4"
            class="hover-effect"
            :options="articles"
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
  props: ['newId', 'formuleId', 'articlesRows'],
  data() {
    return {
      id: null,
      articles: [],
      rows: [
        {
          num_formule: null,
          article: null,
        }
      ],
    };
  },
  computed: {
    ...mapGetters('matieresPremieres', ['allMatieres']),
    ...mapGetters('formules', ['allArticlesFormules']),
    
  },

  async created() {
    this.articles = this.allMatieres.filter(article => article.categorie.nom === "Matériel & Articles de conditionnement");
    this.rows = this.articlesRows;
    this.rows.forEach(row => {
      const matchingArticle = this.articles.find(article => article.id === row.article);
      if (matchingArticle) {
        row.article = matchingArticle;
      }
    });
    console.log('articles', this.articles);
  },

  methods: {
    ...mapActions('notifications', ['showNotification']),

    updateArticlesRows() {
      this.$emit('articlesRows', this.rows);
      console.log(this.rows);
    },

    validRows(){
      this.updateArticlesRows();
      this.showNotification({message: 'Articles ajoutés', type: 'success'});
    },

    addLine() {
      if(this.formuleId) {
        this.rows.push({num_formule: this.formuleId, article: ''});
      }else{
        this.rows.push({num_formule: this.newId, article: ''});
      }
      this.updateArticlesRows();
    },
    removeLine(index) {
      this.rows.splice(index, 1);
      this.updateArticlesRows();
    },
  },
};
</script>


