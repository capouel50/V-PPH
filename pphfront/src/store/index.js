import { createStore } from 'vuex';
import suppliers from './modules/suppliers';
import users from './modules/users';
import notifications from './modules/notifications';
import contact from './modules/contact';
import auth from './modules/auth';
import user from './modules/user';
import errorModule from './modules/errorModule';
import screen from './modules/screen';
import forms from './modules/forms';
import matieresPremieres from './modules/matieresPremieres';
import formules from './modules/formules';
import voiesAdministration from './modules/voiesAdministration';
import demandes from './modules/demandes';
import fiches from './modules/fiches';
import spinner from './modules/spinner';
import websocket from './modules/websocket';
import dateFormatter from './modules/dateFormatter';
import services from './modules/services';
import epi from './modules/epi';
import balances from './modules/balances';
import resetData from './modules/resetData';
import apiError from './modules/apiError';

const store = createStore({
  modules: {
    balances,
    epi,
    apiError,
    resetData,
    services,
    dateFormatter,
    websocket,
    spinner,
    fiches,
    demandes,
    voiesAdministration,
    formules,
    matieresPremieres,
    suppliers,
    users,
    notifications,
    contact,
    user,
    auth,
    errorModule,
    screen,
    forms,
  }
});

export default store;

