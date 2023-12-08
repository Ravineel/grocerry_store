// initial state
const state = () => ({
  categories: [],
  requestCategories: [],

  isloading: false,
  error: null,

  created: false,
  requestCreated: false,
});

// getters
const getters = {
  categories: (state) => state.categories,
  requestCategories: (state) => state.requestCategories,

  isloading: (state) => state.isloading,
  error: (state) => state.error,

  created: (state) => state.created,
  requestCreated: (state) => state.requestCreated,
};

// actions
const actions = {
  async getAllCategories({ commit }) {
    commit("setLoading", true);
    try {
      const response = await fetch(
        "http://localhost:5000/api/v1/category/get/all",
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      const status = response.status;
      const data = await response.json();

      if (status === 200) {
        commit("setCategories", data);
        commit("setLoading", false);
        return data;
      } else {
        commit("setLoading", false);
        commit("setError", data.error_message);
      }
    } catch (err) {
      console.log("An error occured: ", err);
      commit("setError", err);
      commit("setLoading", false);
    }
  },

  async getCategoryById({ commit }, payload) {},

  async createCategoryAdmin({ commit }, payload) {},
  async updateCategoryAdmin({ commit }, payload) {},
  async deleteCategoryAdmin({ commit }, payload) {},

  async createCategoryManager({ commit }, payload) {},
  async updateCategoryManager({ commit }, payload) {},
  async deleteCategoryManager({ commit }, payload) {},

  async getRequestCategory({ commit }) {},
  async approveRequestCategory({ commit }, payload) {},
};

// mutations
const mutations = {
  setCategories: (state, categories) => (state.categories = categories),
  setRequestCategories: (state, requestCategories) =>
    (state.requestCategories = requestCategories),

  setLoading: (state, loading) => (state.isloading = loading),
  setError: (state, error) => (state.error = error),

  setCreated: (state, created) => (state.created = created),
  setRequestCreated: (state, requestCreated) =>
    (state.requestCreated = requestCreated),
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
