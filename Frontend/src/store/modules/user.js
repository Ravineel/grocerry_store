// initial state
const state = () => ({
  user: [],
  isAuthenticated: false,
  token: null,
  errors: [],
  loading: false,
  created: false,
  role: "guest",

  SignedUp: false,
});

// getters
const getters = {
  user: (state) => state.user,
  isAuthenticated: (state) => state.isAuthenticated,
  getToken: (state) => state.token,
  getErrors: (state) => state.errors,
  isloading: (state) => state.loading,
  isCreated: (state) => state.created,
  role: (state) => state.role,
  SignedUp: (state) => state.SignedUp,
};

// actions using fetch()
const actions = {
  async login({ commit }, payload) {
    const roles = ["guest", "user", "manager", "admin"];
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

        commit("setRole", roles[data.user.role]);

        sessionStorage.setItem("userToken", data.token);
        sessionStorage.setItem("UserName", data.user.user_name);
        sessionStorage.setItem("userRole", data.user.role);
        sessionStorage.setItem("isAuthenticated", true);
      } else {
        commit("setErrors", data.error_message);
        commit("setLoading", false);
        console.log(data.error_message);
      }
    } catch (err) {
      console.log("An error occured: ", err);
      commit("setErrors", err);
      commit("setLoading", false);
    }
  },

  async signup({ commit }, payload) {
    commit("setErrors", []);
    commit("setLoading", true);

    console.log(payload);
    try {
      const response = await fetch("http://localhost:5000/api/v1/user/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (data.success) {
        commit("setLoading", false);
        commit("setCreated", true);
        commit("setSignedUp", true);
      } else {
        commit("setErrors", data.error_message);
        commit("setLoading", false);
        commit("setCreated", false);
        console.log(data.error_message);
      }
    } catch (err) {
      console.log("An error occured: ", err);
      commit("setErrors", err);
      commit("setLoading", false);
      commit("setCreated", false);
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
  setRole(state, role) {
    state.role = role;
  },
  setSignedUp(state, SignedUp) {
    state.SignedUp = SignedUp;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
