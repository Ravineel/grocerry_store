// initial state
const state = () => ({
  user: [],
  managers: [],

  manager_chart: [],
  data_chart: [],

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
  managers: (state) => state.managers,
  manager_chart: (state) => state.manager_chart,
  data_chart: (state) => state.data_chart,
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

  async getManagers({ commit }) {
    commit("setErrors", false);
    commit("setLoading", true);

    try {
      const response = await fetch(
        "http://localhost:5000/api/v1/admin/get/manager",
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            authorization: `Bearer ${sessionStorage.getItem("userToken")}`,
          },
        }
      );

      const status = response.status;
      const data = await response.json();
      console.log(data);

      if (status === 200) {
        commit("setManagers", data);
        commit("setLoading", false);
        return data;
      } else if (status === 401) {
        sessionStorage.removeItem("userToken");
        sessionStorage.removeItem("isAuthenticated");
        commit("setLoading", false);

        if (data.error_code === "TOKEN_EXPIRED") {
          commit("setErrors", "Your session has expired. Please login again.");
        }
        if (data.error_code === "TOKEN_INVALID") {
          commit("setErrors", "Your session is invalid. Please login again.");
        }
        if (data.error_code === "INVALID_ROLE") {
          commit("setErrors", "You are not authorized to perform this action.");
        }
        console.log("An error occured: ", data.error_message);
      } else {
        commit("setCreated", false);
        commit("setLoading", false);
        commit("setErrors", data.error_message);
      }
      manager1_password;
    } catch (err) {
      console.log("An error occured: ", err);
      commit("setErrors", err);
      commit("setLoading", false);
    }
  },

  async updateManagerAccess({ commit }, payload) {
    commit("setErrors", false);
    commit("setLoading", true);

    try {
      const response = await fetch(
        "http://localhost:5000/api/v1/admin/update/manager",
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            authorization: `Bearer ${sessionStorage.getItem("userToken")}`,
          },
          body: JSON.stringify(payload),
        }
      );

      const status = response.status;
      const data = await response.json();
      console.log(data);

      if (status === 200) {
        commit("setLoading", false);
        return data;
      } else if (status === 401) {
        sessionStorage.removeItem("userToken");
        sessionStorage.removeItem("isAuthenticated");
        commit("setLoading", false);

        if (data.error_code === "TOKEN_EXPIRED") {
          commit("setErrors", "Your session has expired. Please login again.");
        }
        if (data.error_code === "TOKEN_INVALID") {
          commit("setErrors", "Your session is invalid. Please login again.");
        }
        if (data.error_code === "INVALID_ROLE") {
          commit("setErrors", "You are not authorized to perform this action.");
        }
        console.log("An error occured: ", data.error_message);
      } else {
        commit("setCreated", false);
        commit("setLoading", false);
        commit("setErrors", data.error_message);
      }
    } catch (err) {
      console.log("An error occured: ", err);
      commit("setErrors", err);
      commit("setLoading", false);
    }
  },
  async getManagerChartData({ commit }) {
    commit("setErrors", false);
    commit("setLoading", true);

    try {
      const response = await fetch(
        "http://localhost:5000/api/v1/admin/get/manager_data",
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            authorization: `Bearer ${sessionStorage.getItem("userToken")}`,
          },
        }
      );

      const status = response.status;
      const data = await response.json();
      console.log(data);

      if (status === 200) {
        commit("setManagerChart", data);
        commit("setLoading", false);
        return data;
      } else if (status === 401) {
        sessionStorage.removeItem("userToken");
        sessionStorage.removeItem("isAuthenticated");
        commit("setLoading", false);

        if (data.error_code === "TOKEN_EXPIRED") {
          commit("setErrors", "Your session has expired. Please login again.");
        }
        if (data.error_code === "TOKEN_INVALID") {
          commit("setErrors", "Your session is invalid. Please login again.");
        }
        if (data.error_code === "INVALID_ROLE") {
          commit("setErrors", "You are not authorized to perform this action.");
        }
        console.log("An error occured: ", data.error_message);
      } else {
        commit("setCreated", false);
        commit("setLoading", false);
        commit("setErrors", data.error_message);
      }
      manager1_password;
    } catch (err) {
      console.log("An error occured: ", err);
      commit("setErrors", err);
      commit("setLoading", false);
    }
  },

  async getDataCount({ commit }) {
    commit("setErrors", false);
    commit("setLoading", true);

    try {
      const response = await fetch(
        "http://localhost:5000/api/v1/admin/get/data_count",
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            authorization: `Bearer ${sessionStorage.getItem("userToken")}`,
          },
        }
      );

      const status = response.status;
      const data = await response.json();
      console.log(data);

      if (status === 200) {
        commit("setManagerChart", data);
        commit("setLoading", false);
        return data;
      } else if (status === 401) {
        sessionStorage.removeItem("userToken");
        sessionStorage.removeItem("isAuthenticated");
        commit("setLoading", false);

        if (data.error_code === "TOKEN_EXPIRED") {
          commit("setErrors", "Your session has expired. Please login again.");
        }
        if (data.error_code === "TOKEN_INVALID") {
          commit("setErrors", "Your session is invalid. Please login again.");
        }
        if (data.error_code === "INVALID_ROLE") {
          commit("setErrors", "You are not authorized to perform this action.");
        }
        console.log("An error occured: ", data.error_message);
      } else {
        commit("setCreated", false);
        commit("setLoading", false);
        commit("setErrors", data.error_message);
      }
      manager1_password;
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
  setRole(state, role) {
    state.role = role;
  },
  setSignedUp(state, SignedUp) {
    state.SignedUp = SignedUp;
  },
  setManagers(state, managers) {
    state.managers = managers;
  },
  setManagerChart(state, manager_chart) {
    state.manager_chart = manager_chart;
  },
  setDataChart(state, data_chart) {
    state.data_chart = data_chart;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
