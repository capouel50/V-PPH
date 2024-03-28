import api from '../../../api';

const state = () => ({
  etapes: [],
});

const getters = {
  allEtapes: (state) => state.etapes,
};

const actions = {

  async addEtape({commit, dispatch}, formData) {
    try {
      await api.post('PPH/etapes/', formData);
      commit('ADD_ETAPE', formData);
      dispatch('notifications/showNotification', {
        message: 'Etape ajouté avec succès',
        type: 'success'
      }, {root: true});
      return Promise.resolve();
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors de l\'ajout de l\'étape',
        type: 'error'
      }, {root: true});
      return Promise.reject(error);
    }
  },

  async addEtapes({dispatch}, jsonData) {
    try {
      await api.post('PPH/etapes/', jsonData,
      {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      dispatch('notifications/showNotification', {
        message: 'Ajout du mode opératoire',
        type: 'info'
      }, {root: true});
      return Promise.resolve();
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors de l\'ajout de l\'étape',
        type: 'error'
      }, {root: true});
      return Promise.reject(error);
    }
  },

  async loadEtapes({commit, dispatch}) {
    try {
      const response = await api.get('/PPH/etapes');
      commit('SET_ETAPES', response.data);
      console.log(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des étapes',
        type: 'error'
      }, {root: true});
      console.error(error);
    }
  },
};

const mutations = {
  ADD_ETAPE(state, etape) {
    state.etapes.push(etape);
  },
  SET_ETAPES(state, etapes) {
    state.etapes = etapes;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};