import api from '../../../api';

const state = () => ({
  types: [],
  parametres: [],
  parametresFormules: [],
  articlesFormules: [],
  compositions: [],
  formules: [],
  listes: [],
  showMenu: {},
  expanded: {},
  compo: {},
  settings: {},
  currentFormuleId: null,
});

const getters = {
  compo: (state) => state.compo,
  settings: (state) => state.settings,
  expanded: (state) => state.expanded,
  showMenu: (state) => state.showMenu,
  allTypesPrep: (state) => state.types,
  allCompositions: (state) => state.compositions,
  allParametres: (state) => state.parametres,
  allParametresFormules: (state) => state.parametresFormules,
  allArticlesFormules: (state) => state.articlesFormules,
  allFormules: (state) => state.formules,
  allListes: (state) => state.listes,
};

const actions = {

  async updateArticles({commit, dispatch}, {formData, formuleId}) {
    try {
        const response = await api.put(`PPH/articles-formules/update/${formuleId}/`, formData, {
          headers: {
          'Content-Type': 'application/json'
          }
        })
        commit('SET_ARTICLES_FORMULES', response.data);
        dispatch('notifications/showNotification', {
            message: 'Articles modifiés avec succès',
            type: 'success'
        }, {root: true});
        return Promise.resolve();
    } catch (error) {
        dispatch('notifications/showNotification', {
            message: 'Erreur lors de la modification des articles',
            type: 'error'
        }, {root: true});
        return Promise.reject(error);
    }
  },

  async updateParametres({dispatch}, stateData) {
    try {
      console.log("reception de stateData:", stateData);
        // Assurez-vous que 'formData' est directement le tableau d'objets
        await api.patch('PPH/parametres-formules/', stateData, {
          headers: {
          'Content-Type': 'application/json'
          }
        })
        dispatch('loadArticlesFormules');
        dispatch('notifications/showNotification', {
            message: 'Parametres modifiés avec succès',
            type: 'success'
        }, {root: true});
        return Promise.resolve();
    } catch (error) {
        dispatch('notifications/showNotification', {
            message: 'Erreur lors de la modification des parametres',
            type: 'error'
        }, {root: true});
        return Promise.reject(error);
    }
  },

  async updateFormule({dispatch}, {formData, formuleId}) {
    try {
      await api.patch(`PPH/nouvelle-formule/${formuleId}`, formData);
      dispatch('notifications/showNotification', {
        message: 'Formule modifiée avec succès',
        type: 'success'
      }, {root: true});
      return Promise.resolve();
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors de la modification de la formule',
        type: 'error'
      }, {root: true});
      return Promise.reject(error);
    }
  },

  async addArticles({dispatch}, formData) {
    try {
      console.log("reception de stateData:", formData);
        // Assurez-vous que 'formData' est directement le tableau d'objets
        await api.post('PPH/articles-formules/', formData, {
          headers: {
          'Content-Type': 'application/json'
          }
        })
        dispatch('notifications/showNotification', {
            message: 'Articles ajoutés avec succès',
            type: 'success'
        }, {root: true});
        return Promise.resolve();
    } catch (error) {
        dispatch('notifications/showNotification', {
            message: 'Erreur lors de l\'ajout des articles',
            type: 'error'
        }, {root: true});
        return Promise.reject(error);
    }
  },

  async addParametre({ dispatch }, formData) {
      try {
        await api.post('PPH/parametres-prep/', formData);
        dispatch('loadParametres');
        dispatch('notifications/showNotification', {
          message: `${formData.nom} créé avec succès`,
          type: 'success'
        }, { root: true });
        return Promise.resolve();
      } catch (error) {
        dispatch('notifications/showNotification', {
          message: 'Erreur lors de la création du paramètre',
          type: 'error'
        }, { root: true });
        return Promise.reject(error);
      }
    },

  async addParametres({commit, dispatch}, paramData) {
    try {
      console.log("Envoi de paramData:", paramData);
        // Assurez-vous que 'formData' est directement le tableau d'objets
        const response = await api.post('PPH/parametres-formules/', paramData, {
          headers: {
          'Content-Type': 'application/json'
          }
        })
        commit('SET_PARAMETRES_FORMULES', response.data);
        dispatch('notifications/showNotification', {
            message: 'Paramètres ajoutés avec succès',
            type: 'success'
        }, {root: true});
        return Promise.resolve();
    } catch (error) {
        dispatch('notifications/showNotification', {
            message: 'Erreur lors de l\'ajout des paramètres',
            type: 'error'
        }, {root: true});
        return Promise.reject(error);
    }
  },

  async addFormule({dispatch}, formData) {
    try {
      await api.post('PPH/nouvelle-formule/', formData);
      dispatch('notifications/showNotification', {
        message: 'Formule crée avec succès',
        type: 'success'
      }, {root: true});
      return Promise.resolve();
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors de l\'ajout de la formule',
        type: 'error'
      }, {root: true});
      return Promise.reject(error);
    }
  },

  async addComposition({dispatch}, formData) {
    try {
      await api.post('PPH/composition/', formData);
      dispatch('notifications/showNotification', {
        message: 'Composition ajoutée avec succès',
        type: 'success'
      }, {root: true});
      return Promise.resolve();
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors de l\'ajout de la composition',
        type: 'error'
      }, {root: true});
      return Promise.reject(error);
    }
  },

  async getCompositionsForFormule({ dispatch }, num_formule) {
    try {
      const response = await api.get(`PPH/composition/filter/${num_formule}`);
      return Promise.resolve(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors de la récupération des compositions existantes',
        type: 'error',
      }, { root: true });
      return Promise.reject(error);
    }
  },

  async loadCompositions({commit, dispatch}) {
    try {
      const response = await api.get('/PPH/composition');
      commit('SET_COMPOSITIONS', response.data);
      console.log(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des compositions',
        type: 'error'
      }, {root: true});
      console.error(error);
    }
  },

  async loadFormules({commit, dispatch}) {
    try {
      const response = await api.get('/PPH/formules');
      commit('SET_FORMULES', response.data);
      console.log(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des formules',
        type: 'error'
      }, {root: true});
      console.error(error);
    }
  },

  async loadListes({commit, dispatch}) {
    try {
      const response = await api.get('/PPH/liste');
      commit('SET_LISTE', response.data);
      console.log(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des listes',
        type: 'error'
      }, {root: true});
      console.error(error);
    }
  },

  async loadTypes({commit, dispatch}) {
    try {
      const response = await api.get('/PPH/type-prep');
      commit('SET_TYPE', response.data);
      console.log(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des types de préparations',
        type: 'error'
      }, {root: true});
      console.error(error);
    }
  },

  async loadArticlesFormules({commit, dispatch}) {
    try {
      const response = await api.get('/PPH/articles-formules');
      commit('SET_ARTICLES_FORMULES', response.data);
      console.log(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des articles',
        type: 'error'
      }, {root: true});
      console.error(error);
    }
  },

  async loadParametresFormules({commit, dispatch}) {
    try {
      const response = await api.get('/PPH/parametres-formules');
      commit('SET_PARAMETRES_FORMULES', response.data);
      console.log(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des paramètres',
        type: 'error'
      }, {root: true});
      console.error(error);
    }
  },

  async loadParametres({commit, dispatch}) {
    try {
      const response = await api.get('/PPH/parametres-prep');
      commit('SET_PARAMETRE', response.data);
      console.log(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des paramètres',
        type: 'error'
      }, {root: true});
      console.error(error);
    }
  },

  async toggleActivation({ dispatch }, payload) {
    const { formuleId, isActive } = payload;
    try {
      if (isActive) {
        await api.patch(`/PPH/formules/${formuleId}/`, { is_activate: false });
        dispatch('notifications/showNotification', {
          message: 'Formule désactivée',
          type: 'success'
        }, { root: true });
      } else {
        await api.patch(`/PPH/formules/${formuleId}/`, { is_activate: true });
        dispatch('notifications/showNotification', {
          message: 'Formule activée',
          type: 'success'
        }, { root: true });
      }
      dispatch('loadFormules');
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du changement d\'état',
        type: 'error'
      }, { root: true });
      console.error(error);
    }
  },

  async validFormule({ dispatch }, payload) {
    const { formuleId, isValid } = payload;
    try {
      if (isValid) {
        await api.patch(`/PPH/formules/${formuleId}/`, { is_valid: false });
        dispatch('notifications/showNotification', {
          message: 'Formule non-validée',
          type: 'success'
        }, { root: true });
      } else {
        await api.patch(`/PPH/formules/${formuleId}/`, { is_valid: true });
        dispatch('notifications/showNotification', {
          message: 'Formule validée',
          type: 'success'
        }, { root: true });
      }
      dispatch('loadFormules');
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du changement d\'état',
        type: 'error'
      }, { root: true });
      console.error(error);
    }
  },

  async toggleCloud({ dispatch }, payload) {
    const { formuleId, isCloud } = payload;
    try {
      if (isCloud) {
        await api.patch(`/PPH/formules/${formuleId}/`, { cloud: false });
        dispatch('notifications/showNotification', {
          message: 'Formule retirée du cloud',
          type: 'success'
        }, { root: true });
      } else {
        await api.patch(`/PPH/formules/${formuleId}/`, { cloud: true });
        dispatch('notifications/showNotification', {
          message: 'Formule ajoutée au cloud',
          type: 'success'
        }, { root: true });
      }
      dispatch('loadFormules');
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
  toggleCompo({ commit }, id) {
    commit('TOGGLE_COMPO', id);
  },
  toggleSettings({ commit }, id) {
    commit('TOGGLE_SETTINGS', id);
  },
};

const mutations = {
  updateName(state, newName) {
    state.name = newName;
  },
  updateTypePrep(state, newTypePrep) {
    state.typePrep = newTypePrep;
  },
  
  ADD_TYPE(state, type) {
    state.types.push(type);
  },

  ADD_ARTICLES_FORMULES(state, articles) {
    state.articlesFormules.push(...articles);
  },
  ADD_ARTICLE(state, article) {
    state.articlesFormules.push(article);
  },
  ADD_PARAMETRE(state, parametre) {
    state.parametresFormules.push(parametre);
  },

  SET_COMPOSITIONS(state, compositions) {
    state.compositions = compositions;
  },
  SET_TYPE(state, types) {
    state.types = types;
  },
  SET_LISTE(state, listes) {
    state.listes = listes;
  },
  RESET_ARTICLES_FORMULES(state, num_formule) {
    state.articlesFormules = state.articlesFormules
        .filter(article => article.num_formule !== num_formule);
  },
  RESET_PARAMETRES_FORMULES(state, num_formule) {
    state.parametresFormules = state.parametresFormules
        .filter(parametre => parametre.num_formule !== num_formule);
  },
  REMOVE_ARTICLE(state, { num_formule, articleId }) {
    state.articlesFormules = state.articlesFormules.filter(article => {
      return article.num_formule !== num_formule || article.articleId !== articleId;
    });
  },
  REMOVE_PARAMETRE(state, { num_formule, parametreId }) {
    state.parametresFormules = state.parametresFormules.filter(parametre => {
      return parametre.num_formule !== num_formule || parametre.parametreId !== parametreId;
    });
  },
  SET_PARAMETRE(state, parametres) {
    state.parametres = parametres;
  },
  SET_PARAMETRES_FORMULES(state, parametres) {
    state.parametresFormules = parametres;
  },
  SET_ARTICLES_FORMULES(state, articles) {
    state.articlesFormules = articles;
  },
  SET_FORMULES(state, formules) {
    state.formules = formules;
  },
  TOGGLE_MENU(state, id) {
    state.showMenu[id] = !state.showMenu[id];
  },
  TOGGLE_INFO(state, id) {
    state.expanded[id] = !state.expanded[id];
  },
  TOGGLE_COMPO(state, id) {
    state.compo[id] = !state.compo[id];
  },
  TOGGLE_SETTINGS(state, id) {
    state.settings[id] = !state.settings[id];
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};