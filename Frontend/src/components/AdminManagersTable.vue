<template>
  <ag-grid-vue
    style="width: 100%; height: 600px"
    :class="themeClass"
    :columnDefs="columnDefs"
    @grid-ready="onGridReady"
    :defaultColDef="defaultColDef"
    :suppressRowClickSelection="false"
    :rowSelection="rowSelection"
    :paginationAutoPageSize="true"
    :pagination="true"
    :rowData="rowData"
    @selection-changed="onSelectionChanged"
  ></ag-grid-vue>
</template>

<script>
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css";
import { AgGridVue } from "ag-grid-vue3";
import ManagerStatus from "@/components/ManagerStatus.vue";
import ManagerApprovalRender from "@/components/ManagerApprovalRender.vue";

const textfilterParams = {
  filterOptions: [
    "contains",
    "notContains",
    "startsWith",
    "endsWith",
    "equals",
    "notEqual",
  ],
  suppressAndOrCondition: true,
  textFormatter: function (r) {
    if (r == null) return null;
    return r.toLowerCase();
  },
};

const numberFilterParams = {
  filterOptions: [
    "equals",
    "notEqual",
    "lessThan",
    "lessThanOrEqual",
    "greaterThan",
    "greaterThanOrEqual",
    "inRange",
  ],
  suppressAndOrCondition: true,
};

const dateFilterParams = {
  filterOptions: [
    "equals",
    "notEqual",
    "lessThan",
    "lessThanOrEqual",
    "greaterThan",
    "greaterThanOrEqual",
    "inRange",
  ],
  suppressAndOrCondition: true,
};

export default {
  components: {
    AgGridVue,
    ManagerStatus,
    ManagerApprovalRender,
  },
  data: function () {
    return {
      gridApi: null,
      themeClass: "ag-theme-quartz-dark",
      defaultColDef: {
        editable: false,
        filter: true,
        flex: 1,
        minWidth: 100,
        sortable: true,
        resizable: true,
      },

      rowSelection: null,
      rowData: null,
      selectedRow: null,
      columnDefs: null,
      components: null,
    };
  },
  created() {
    this.rowSelection = "single";
  },

  beforeMount() {
    this.columnDefs = [
      {
        field: "id",
        headerName: "Request ID",
        minWidth: 100,
        filter: "agNumberColumnFilter",
        filterParams: numberFilterParams,
        sort: "asc",
      },
      {
        field: "first_name",
        headerName: "First Name",
        minWidth: 100,
        filter: "agTextColumnFilter",
        filterParams: textfilterParams,
      },
      {
        field: "last_name",
        headerName: "Last Name",
        minWidth: 100,
        filter: "agTextColumnFilter",
        filterParams: textfilterParams,
      },
      {
        field: "email",
        headerName: "Email",
        minWidth: 100,
        filter: "agTextColumnFilter",
        filterParams: textfilterParams,
      },
      {
        field: "is_manager_active",
        headerName: "Status",
        minWidth: 100,
        filter: "agTextColumnFilter",
        filterParams: textfilterParams,
        cellRenderer: "ManagerStatus",
      },
      {
        headerName: "Actions",
        minWidth: 200,
        cellRenderer: "ManagerApprovalRender",
        cellRendererParams: {
          onApprove: this.onApprove,
          onReject: this.onReject,
        },
      },
    ];

    this.components = {
      managerStatus: ManagerStatus,
    };
  },

  methods: {
    onGridReady(params) {
      this.gridApi = params.api;

      const updateData = (data) => (this.rowData = data);

      this.$store.dispatch("user/getManagers").then((data) => {
        if (this.$store.getters["user/getErrors"]) {
          this.$toast.error(this.$store.getters["categories/getErrors"]);
        } else if (sessionStorage.getItem("isAuthenticated")) {
          updateData(data);
        } else {
          this.$router.push({ name: "Login" });
          this.$toast.error("Please Login First");
        }
      });
    },
    onSelectionChanged() {
      const selectedRows = this.gridApi.getSelectedRows();
      this.selectedRow = selectedRows[0];
    },
    onApprove(param) {
      const paylod = {
        manager_id: param.id,
        is_manager_active: !param.is_manager_active,
      };
      this.$store.dispatch("user/updateManagerAccess", paylod).then((res) => {
        if (this.$store.getters["user/getErrors"]) {
          this.$toast.error(this.$store.getters["user/getErrors"]);
        } else {
          this.$toast.success("Manger Approved");
          this.$router.push({ name: "Admin" });
        }
      });
    },
    onReject(param) {
      const paylod = {
        manager_id: param.id,
        is_manager_active: !param.is_manager_active,
      };

      this.$store.dispatch("user/updateManagerAccess", paylod).then((res) => {
        if (this.$store.getters["user/getErrors"]) {
          this.$toast.error(this.$store.getters["user/getErrors"]);
        } else {
          this.$toast.success("Manager Access Revoked");
          this.$router.push({ name: "Admin" });
        }
      });
    },
  },
};
</script>
