import api from '../../../api';

const state = () => ({
  appareils: [],
  types: [],
  coms: [],
  instructionsAppareils: [],
  reponses: [],
  showMenu: {},
  expanded: {},
});

const getters = {
  allReponses: (state) => state.reponses,
  allAppareils: (state) => state.appareils,
  allTypes: (state) => state.types,
  allComs: (state) => state.coms,
  allInstructionsAppareils: (state) => state.instructionsAppareils,
  showMenu: (state) => state.showMenu,
  expanded: (state) => state.expanded,
};

const actions = {

  async addAppareil({dispatch}, formData) {
    try {
      await api.post('PPH/appareils/', formData);
      dispatch('notifications/showNotification', {
        message: 'Appareil ajouté avec succès',
        type: 'success'
      }, {root: true});
      return Promise.resolve();
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors de l\'ajout de la appareil',
        type: 'error'
      }, {root: true});
      return Promise.reject(error);
    }
  },

  async loadAppareils({commit, dispatch}) {
    try {
      const response = await api.get('/PPH/appareils');
      commit('SET_APPAREILS', response.data);
      console.log(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des appareil',
        type: 'error'
      }, {root: true});
      console.error(error);
    }
  },

  async loadTypesAppareils({commit, dispatch}) {
    try {
      const response = await api.get('/PPH/types-appareils');
      commit('SET_TYPES_APPAREILS', response.data);
      console.log(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des types d\'appareil',
        type: 'error'
      }, {root: true});
      console.error(error);
    }
  },

  async loadCom({commit, dispatch}) {
    try {
      const response = await api.get('/PPH/type-com');
      commit('SET_COM_APPAREILS', response.data);
      console.log(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des communications',
        type: 'error'
      }, {root: true});
      console.error(error);
    }
  },

  async loadInstructionsAppareils({ commit, dispatch }) {
    try {
      const response = await api.get('/instructions-appareils');
      commit('SET_INSTRUCTIONS_APPAREILS', response.data);

    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement de instructions',
        type: 'error'
      }, {root: true});
      console.error('Erreur lors du chargement des instructions :', error);
    }
  },

  async loadReponses({ commit, dispatch }) {
    try {
      const response = await api.get('/reponses-appareils');
      commit('SET_REPONSES_APPAREILS', response.data);

    } catch (error) {
      dispatch('notifications/showNotification', {
        message: `Erreur lors du chargement des réponses: ${error}`,
        type: 'error'
      }, {root: true});
      console.error('Erreur lors du chargement des réponses :', error);
    }
  },

  async getCalibration({dispatch}, appareil) {
    try {
      console.log('appareil', appareil)
      const response = await api.get(`PPH/appareils/${appareil.id}/`);
      const calibrationDate = new Date(response.data.calibration);
      const currentDate = new Date();
      currentDate.setDate(currentDate.getDate() + 30);
      const daysRemaining = Math.floor((calibrationDate.getTime() - currentDate.getTime()) / (1000*60*60*24));
      if (calibrationDate < currentDate) {
        dispatch('notifications/showNotification', {
          message: `La calibration expire dans ${daysRemaining} jours`,  // Insertion du nombre de jours restants dans le message
          type: 'error'
        }, {root: true});
      }
      return Promise.resolve();
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors de l\'obtention de la date de calibration',
        type: 'error'
      }, {root: true});
      return Promise.reject(error);
    }
  },

  async toggleActivation({ dispatch }, payload) {
    const { appareilId, isActive, appareilName } = payload;
    try {
      if (isActive) {
        await api.patch(`/PPH/appareils/${appareilId}/`, { is_activate: false });
        dispatch('notifications/showNotification', {
          message: `${appareilName} désactivée`,
          type: 'success'
        }, { root: true });
      } else {
        await api.patch(`/PPH/appareils/${appareilId}/`, { is_activate: true });
        dispatch('notifications/showNotification', {
          message: `${appareilName} activée`,
          type: 'success'
        }, { root: true });
      }
      dispatch('loadSuppliers');
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du changement d\'état',
        type: 'error'
      }, { root: true });
      console.error(error);
    }
  },

  toggleMenu({ commit }, id) {
    commit('TOGGLE_MENU', id);
  },
  toggleInfo({ commit }, id) {
    commit('TOGGLE_INFO', id);
  },
};

const mutations = {
  TOGGLE_MENU(state, id) {
    state.showMenu[id] = !state.showMenu[id];
  },
  TOGGLE_INFO(state, id) {
    state.expanded[id] = !state.expanded[id];
  },
  ADD_APPAREIL(state, appareil) {
    state.appareils.push(appareil);
  },
  SET_APPAREILS(state, appareils) {
    state.appareils = appareils;
  },
  SET_TYPES_APPAREILS(state, types) {
    state.types = types;
  },
  SET_COM_APPAREILS(state, coms) {
    state.coms = coms;
  },
  SET_INSTRUCTIONS_APPAREILS(state, instructionsAppareils) {
    state.instructionsAppareils = instructionsAppareils;
  },
  SET_REPONSES_APPAREILS(state, reponses) {
    state.reponses = reponses;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};