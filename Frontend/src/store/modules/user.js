// initial state
const state = () => ({
  user: [],
  isAuthenticated: false,
  token: null,
  errors: [],
  loading: false,
  created: false,
});

// getters
const getters = {
  user: (state) => state.user,
  isAuthenticated: (state) => state.isAuthenticated,
  getToken: (state) => state.token,
  getErrors: (state) => state.errors,
  isloading: (state) => state.loading,
  isCreated: (state) => state.created,
};

// actions using fetch()
const actions = {
  async login({ commit }, payload) {
    commit("setErrors", []);
    commit("setLoading", true);

    try {
      const response = await fetch("http://localhost:5000/api/v1/user/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });
      const data = await response.json();

      console.log(data);

      if (data.success) {
        commit("setToken", data.token);
        commit("setUser", data.user);
        commit("setIsAuthenticated", true);
        commit("setLoading", false);
        sessionStorage.setItem("token", data.token);
        sessionStorage.setItem("User Name", data.user.user_name);
        sessionStorage.setItem("role", data.user.role);
      } else {
        commit("setErrors", data.errors);
        commit("setLoading", false);
        console.log(data.errors);
      }
    } catch (err) {
      console.log("An error occured: ", err);
      commit("setErrors", err);
      commit("setLoading", false);
    }
  },
};

// mutations
const mutations = {
  setUser(state, user) {
    state.user = user;
  },
  setToken(state, token) {
    state.token = token;
  },
  setIsAuthenticated(state, isAuthenticated) {
    state.isAuthenticated = isAuthenticated;
  },
  setErrors(state, errors) {
    state.errors = errors;
  },
  setLoading(state, loading) {
    state.loading = loading;
  },
  setCreated(state, created) {
    state.created = created;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
