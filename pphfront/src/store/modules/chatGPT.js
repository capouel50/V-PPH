import api from '../../../api';

const state = {
  vpph: [],
  profil: [],
  competences: [],
  situations: [],
  personnas: [],
  response: null,
  history: null,
};

const getters = {
  getResponse: state => state.response,
  allHistory: state => state.history,
  allProfils: state => state.profil,
  getVpph: state => state.vpph,
};

const actions = {
  async askQuestion({ commit, dispatch }, messageSent) {
    try {
      commit('deleteResponse');
      console.log('message', messageSent);
      const response = await api.post('PPH/chatgpt/', messageSent);
      commit('setResponse', response.data.message);
    } catch (error) {
      // Exemple de gestion des erreurs plus détaillée
      let errorMessage = 'Désolé, une erreur est survenue.';
      if (error.response && error.response.data && error.response.data.error) {
        errorMessage = error.response.data.error;
      } else if (error.message) {
        errorMessage = error.message;
      }

      dispatch('notifications/showNotification', {
        message: errorMessage,
        type: 'error'
      }, { root: true });

      console.error('Erreur lors de l\'envoi de la question : ', errorMessage);
      commit('setResponse', errorMessage);
    }
  },

  async getHistory({commit, dispatch}) {
    try {
      const response = await api.get('PPH/chatgpt/');
      commit('setHistory', response.data);
      return Promise.resolve();
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des conversations',
        type: 'error'
      }, {root: true});
      return Promise.reject(error);
    }
  },

  async saveVpph({dispatch}, {id, formData}) {
    try {
      await api.patch(`PPH/personnas/${id}/`, formData);
      dispatch('notifications/showNotification', {
        message: 'Paramètres V-PPH enregistrés',
        type: 'succes'
      }, {root: true});
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors de l\'enregistrement des paramètres',
        type: 'error'
      }, {root: true});
    }
  },

  async loadVpph({commit, dispatch}) {
    try {
      const response = await api.get('PPH/personnas/');
      console.log('VpphData', response.data);
      commit('setVpph', response.data);
      return Promise.resolve();
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement de V-PP',
        type: 'error'
      }, {root: true});
      return Promise.reject(error);
    }
  },

  async newChat(){
    await api.delete('PPH/chatgpt/')
      .then(function (response) {
        // Traitement en cas de succès
        console.log('Ressource supprimée avec succès', response);
      })
      .catch(function (error) {
        // Traitement en cas d'erreur
        console.log('Erreur lors de la suppression de la ressource', error);
      });
  },

  async sciteApi() {
    const { data: result } = await api.get(
      'https://api.scite.ai/search',{
        params: {
          term: "CRISPR"
        }
      }
    )
    console.log(result)
  },

  ajouterProfil({ commit }, profil) {
    console.log('ajout', profil);
    commit('addProfil', profil);
  },

  modifierProfil({ commit }, { index, profil }) {
    console.log('modif', profil);
    commit('updateProfil', { index, nouveauProfil: profil });
  },

};

const mutations = {

  addCompetence(state, newCompetence) {
    state.competences.push(newCompetence);
  },
  addProfil(state, nouveauProfil) {
    console.log('add', nouveauProfil);
    state.profil.push(nouveauProfil);
  },

  updateProfil(state, { index, nouveauProfil }) {
    if (index >= 0 && index < state.profil.length) {
      console.log('update', nouveauProfil);
      state.profil.splice(index, 1, nouveauProfil);
      state.profil = [...state.profil];
    }
  },
  setVpph(state, response) {
    state.vpph = response;
  },
  setResponse(state, response) {
    state.response = response;
  },
  setHistory(state, response) {
    state.history = response;
  },
  deleteResponse(state) {
    state.response = null;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
