import Vue from "vue";
import Vuex from "vuex";
import pathify from "./pathify";
import dashboard from "./modules/dashboard";

Vue.use(Vuex);
export default new Vuex.Store({
  plugins: [pathify.plugin],
  modules: {
    dashboard
  }
});
