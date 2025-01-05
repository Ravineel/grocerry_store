import { API_ENDPOINTS } from "@/constants/api";

// initial state
const state = () => ({
  orders: [],
  isLoading: false,
  error: null,
});

// getters
const getters = {
  orders: (state) => state.orders,
  isLoading: (state) => state.isLoading,
  error: (state) => state.error,
};

// actions
const actions = {
  async getAllOrders({ commit }) {
    commit("setLoading", true);
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_BASE_URL}${API_ENDPOINTS.ORDER.GET_ALL}`,
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

      if (status === 200) {
        commit("setOrders", data);
        commit("setLoading", false);
        return data;
      } else if (status === 401) {
        sessionStorage.removeItem("userToken");
        sessionStorage.removeItem("isAuthenticated");
        commit("setLoading", false);
        commit("setError", "Authentication error");
      } else {
        commit("setLoading", false);
        commit("setError", data.error_message);
      }
    } catch (err) {
      console.log("An error occurred: ", err);
      commit("setError", err);
      commit("setLoading", false);
    }
  },
};

// mutations
const mutations = {
  setOrders: (state, orders) => (state.orders = orders),
  setLoading: (state, loading) => (state.isLoading = loading),
  setError: (state, error) => (state.error = error),
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
