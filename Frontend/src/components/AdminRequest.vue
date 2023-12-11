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
import StatusRenderer from "@/components/StatusRenderer.vue";
import TypeRenderer from "@/components/TypeRenderer.vue";
import ActionsAdminRequest from "@/components/ActionsAdminRequest.vue";

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
    StatusRenderer,
    TypeRenderer,
    ActionsAdminRequest,
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
        field: "category_id",
        headerName: "Category ID",
        minWidth: 100,
        filter: "agNumberColumnFilter",
        filterParams: numberFilterParams,
        sort: "asc",
      },
      {
        field: "category_name",
        headerName: "Category Name",
        minWidth: 150,
        filter: "agTextColumnFilter",
        filterParams: textfilterParams,
      },

      {
        field: "description",
        headerName: "Description",
        minWidth: 150,
        filter: "agTextColumnFilter",
        filterParams: textfilterParams,
      },
      {
        field: "create_date",
        headerName: "Create Date",
        minWidth: 150,
        filter: "agDateColumnFilter",
        filterParams: dateFilterParams,
      },
      {
        field: "type",
        headerName: "Type",
        minWidth: 150,
        filter: "agTextColumnFilter",
        filterParams: textfilterParams,
        cellRenderer: "TypeRenderer",
      },
      {
        field: "request_status",
        headerName: "Request Status",
        minWidth: 150,
        filter: "agTextColumnFilter",
        filterParams: textfilterParams,
        cellRenderer: "StatusRenderer",
      },

      {
        field: "requested_by_name",
        headerName: "Requested By",
        minWidth: 150,
        filter: "agTextColumnFilter",
        filterParams: textfilterParams,
      },
      {
        field: "approved_date",
        headerName: "Approved Date",
        minWidth: 150,
        filter: "agDateColumnFilter",
        filterParams: dateFilterParams,
      },
      {
        headerName: "Actions",
        minWidth: 250,
        cellRenderer: ActionsAdminRequest,
        cellRendererParams: {
          onApprove: this.onApprove,
          onReject: this.onReject,
        },
      },
    ];

    this.components = {
      statusRenderer: StatusRenderer,
      typeRenderer: TypeRenderer,
    };
  },

  methods: {
    onGridReady(params) {
      this.gridApi = params.api;

      const updateData = (data) => (this.rowData = data);

      this.$store
        .dispatch("categories/getRequestCategoryAdmin")
        .then((data) => {
          if (this.$store.getters["categories/error"]) {
            this.$toast.error(this.$store.getters["categories/error"]);
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
        category_id: param.id,
        has_approved: "true",
      };
      this.$store
        .dispatch("categories/approveRequestCategory", paylod)
        .then((res) => {
          if (this.$store.getters["categories/error"]) {
            this.$toast.error(this.$store.getters["categories/error"]);
          } else {
            this.$toast.success("Category Approved");
            this.$router.push({ name: "AdminRequest" });
          }
        });
    },
    onReject(param) {
      const paylod = {
        category_id: param.id,
        has_approved: "false",
      };
      this.$store
        .dispatch("categories/approveRequestCategory", paylod)
        .then((res) => {
          if (this.$store.getters["categories/error"]) {
            this.$toast.error(this.$store.getters["categories/error"]);
          } else {
            this.$toast.success("Category Rejected");
            this.$router.push({ name: "AdminRequest" });
          }
        });
    },
  },
};
</script>
