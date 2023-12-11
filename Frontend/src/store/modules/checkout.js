const state = () => ({
  checkoutStatus: null,

  isLoading: false,
  created: false,
  error: null,
});

// getters
const getters = {
  isLoading: (state) => state.isLoading,
  created: (state) => state.created,
  error: (state) => state.error,
  checkoutStatus: (state) => state.checkoutStatus,
};

// actions USING FETCH API
const actions = {
  async createOrder({ commit }, payload) {
    commit("setLoading", true);
    commit("setError", null);
    commit("setCreated", false);

    try {
      console.log("payload: ", payload);
      const response = await fetch(
        "http://localhost:5000/api/v1/order/checkout",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            authorization: `Bearer ${sessionStorage.getItem("userToken")}`,
          },
          body: JSON.stringify(payload),
        }
      );
      console.log("response: ", response);

      const status = response.status;

      const responseData = await response.json();

      if (status === 200) {
        commit("setLoading", false);
        commit("setCreated", true);
        commit("setError", null);
        return responseData;
      } else if (status === 401) {
        console.log("Unauthorized");

        sessionStorage.removeItem("userToken");
        sessionStorage.removeItem("isAuthenticated");
        commit("setLoading", false);
        commit("setCreated", false);

        if (responseData.error_code === "TOKEN_EXPIRED") {
          commit("setError", "Your session has expired. Please login again.");
        }
        if (responseData.error_code === "TOKEN_INVALID") {
          commit("setError", "Your session is invalid. Please login again.");
        }
        if (responseData.error_code === "INVALID_ROLE") {
          commit("setError", "You are not authorized to perform this action.");
        }
        console.log("An error occured: ", responseData.error_message);
      } else {
        console.log("An error occured: ", responseData.error_message);
        commit("setLoading", false);
        commit("setCreated", false);
        commit("setError", responseData.error_message);
      }
    } catch (error) {
      console.log("An error occured: ", error);
      commit("setLoading", false);
      commit("setCreated", false);
      commit("setError", error.message);
    }
  },
};

// mutations
const mutations = {
  setLoading: (state, payload) => (state.isLoading = payload),
  setCreated: (state, payload) => (state.created = payload),
  setError: (state, payload) => (state.error = payload),
  setCheckoutStatus: (state, payload) => (state.checkoutStatus = payload),
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
