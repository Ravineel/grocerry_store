<template>
  <ag-grid-vue
    style="width: 100%; height: 400px"
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
import ActionsRenderer from "@/components/ActionsRenderer.vue";

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
    ActionsRenderer,
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
    (this.columnDefs = [
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
        headerName: "Actions",
        minWidth: 200,
        filter: false,
        cellRenderer: "ActionsRenderer",
        cellRendererParams: {
          onEdit: this.onEditClick,
          onDelete: this.onDeleteClick,
        },
      },
    ]),
      (this.components = {
        ActionsRenderer: ActionsRenderer,
      });
  },

  methods: {
    onGridReady(params) {
      this.gridApi = params.api;

      const updateData = (data) => (this.rowData = data);

      this.$store.dispatch("categories/getAllCategories").then((data) => {
        updateData(data);
      });
    },
    onSelectionChanged() {
      const selectedRows = this.gridApi.getSelectedRows();
      this.selectedRow = selectedRows[0];
    },
    onEditClick(param) {
      this.$router.push({
        name: "EditCategory",
        params: { category_id: param.category_id },
      });
    },
    onDeleteClick(param) {
      const payload = {
        category_name: param.category_name,
        description: param.description,
        type: "DELETE",
      };

      this.$store
        .dispatch("categories/createCategoryRequestManager", payload)
        .then((data) => {
          if (data.success == "true") {
            this.$toast.success("Category Request for Delete is Successfull");
          } else {
            this.$router.push("/login");
            this.$toast.error(this.$store.getters["categories/error"]);
          }
        });
    },
  },
};
</script>
