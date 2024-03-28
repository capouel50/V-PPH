import api from '../../../api';

const state = () => ({
  epis: [],
  episFormules: [],
});

const getters = {
  allEpis: (state) => state.epis,
  allEpisFormules: (state) => state.episFormules,
};

const actions = {

  async addEpi({dispatch}, formData) {
    try {
      await api.post('PPH/epi/', formData);
      dispatch('notifications/showNotification', {
        message: 'Epi ajouté avec succès',
        type: 'success'
      }, {root: true});
      return Promise.resolve();
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors de l\'ajout de l\'EPI',
        type: 'error'
      }, {root: true});
      return Promise.reject(error);
    }
  },

  async addEpis({dispatch}, formData) {
    try {
      await api.post('PPH/epi-formules/', formData);
      dispatch('notifications/showNotification', {
        message: 'Epi ajouté avec succès',
        type: 'success'
      }, {root: true});
      return Promise.resolve();
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: `Erreur méthode addEpis: ${error}`,
        type: 'error'
      }, {root: true});
      return Promise.reject(error);
    }
  },

  async updateEpis({dispatch}, {formData, id}) {
    try {
      await api.put(`PPH/epi-formules/${id}/`, formData);
      dispatch('notifications/showNotification', {
        message: 'Epi ajouté avec succès',
        type: 'success'
      }, {root: true});
      return Promise.resolve();
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: error,
        type: 'error'
      }, {root: true});
      return Promise.reject(error);
    }
  },

  async loadEpis({commit, dispatch}) {
    try {
      const response = await api.get('/PPH/epi');
      commit('SET_EPI', response.data);
      console.log(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des EPI',
        type: 'error'
      }, {root: true});
      console.error(error);
    }
  },

  async loadEpisFormules({ commit, dispatch }) {
    try {
      const response = await api.get('/epi-formules');
      commit('SET_EPI_FORMULES', response.data);

    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des EPI',
        type: 'error'
      }, {root: true});
      console.error('Erreur lors du chargement des fiches :', error);
    }
  },
};

const mutations = {
  ADD_EPI(state, epi) {
    state.epis.push(epi);
  },
  SET_EPI(state, epis) {
    state.epis = epis;
  },
  SET_EPI_FORMULES(state, episFormules) {
    state.episFormules = episFormules;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};