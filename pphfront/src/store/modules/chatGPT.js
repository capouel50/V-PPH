import api from '../../../api';

const state = {
  response: null, // La réponse de ChatGPT
  history: null,
};

const getters = {
  getResponse: state => state.response,
  allHistory: state => state.history,
};

const actions = {
  async askQuestion({ commit, dispatch }, messageSent) {
    try {
      commit('deleteResponse');
      const response = await api.post('PPH/chatgpt/', { message: messageSent });
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
}

};

const mutations = {
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
