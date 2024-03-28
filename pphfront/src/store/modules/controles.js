import api from '../../../api';

const state = {
  typesControles: [],
  controles: [],
  showMenu: {},
  settings: {},
};

const getters = {
  showMenu: (state) => state.showMenu,

  settings: (state) => state.settings,

  allTypesControles: state => state.typesControles,

  allControles: state => state.controles,

};

const actions = {

  async addType({dispatch}, typeData) {
    try {
      await api.post('PPH/type-controle/', typeData);
      dispatch('notifications/showNotification', {
        message: 'Contrôle enregistré avec succès',
        type: 'success'
      }, {root: true});
      return Promise.resolve();
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors de l\'ajout du contrôle',
        type: 'error'
      }, {root: true});
      return Promise.reject(error);
    }
  },

  async loadTypes({commit, dispatch}) {
    try {
      const response = await api.get('PPH/type-controle/');
      commit('SET_TYPES', response.data);
      return Promise.resolve();
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des contrôles',
        type: 'error'
      }, {root: true});
      return Promise.reject(error);
    }
  },

  toggleInfo({ commit }, id) {
    commit('TOGGLE_INFO', id);
  },

  toggleMenu({ commit }, id) {
    commit('TOGGLE_MENU', id);
  },

  toggleSettings({ commit }, id) {
    commit('TOGGLE_SETTINGS', id);
  },

};

const mutations = {
  ADD_TYPE: (state, type) => {
    state.typesControles.push(type);
  },

  SET_TYPES: (state, typesControles) => {
    state.typesControles = typesControles;
  },

  TOGGLE_MENU(state, id) {
    state.showMenu[id] = !state.showMenu[id];
  },

  TOGGLE_SETTINGS(state, id) {
    state.settings[id] = !state.settings[id];
  },

};
export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
