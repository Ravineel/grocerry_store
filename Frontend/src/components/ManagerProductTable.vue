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
        field: "product_id",
        headerName: "Product ID",
        minWidth: 100,
        filter: "agNumberColumnFilter",
        filterParams: numberFilterParams,
        sort: "asc",
      },
      {
        field: "product_name",
        headerName: "Product Name",
        minWidth: 150,
        filter: "agTextColumnFilter",
        filterParams: textfilterParams,
      },
      {
        field: "category_name",
        headerName: "Category",
        minWidth: 150,
        filter: "agTextColumnFilter",
        filterParams: textfilterParams,
      },
      {
        field: "manufacturer",
        headerName: "Manufacturer",
        minWidth: 150,
        filter: "agTextColumnFilter",
        filterParams: textfilterParams,
      },
      {
        field: "rate",
        headerName: "Rate",
        minWidth: 100,
        filter: "agNumberColumnFilter",
        filterParams: numberFilterParams,
      },
      {
        field: "unit",
        headerName: "Unit",
        minWidth: 100,
        filter: "agTextColumnFilter",
        filterParams: textfilterParams,
      },
      {
        field: "mfg_date",
        headerName: "Mfg Date",
        minWidth: 150,
        filter: "agDateColumnFilter",
        filterParams: dateFilterParams,
      },
      {
        field: "qty",
        headerName: "Quantity Available",
        minWidth: 100,
        filter: "agNumberColumnFilter",
        filterParams: numberFilterParams,
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

      this.$store.dispatch("products/getAllProducts").then((data) => {
        updateData(data);
      });
    },
    onSelectionChanged() {
      const selectedRows = this.gridApi.getSelectedRows();
      this.selectedRow = selectedRows[0];
    },
    onEditClick(param) {
      this.$router.push({
        name: "EditProduct",
        params: { product_id: param.product_id },
      });
    },
    onDeleteClick(param) {
      const payload = {
        product_id: param.product_id,
      };

      if (confirm("Are you sure you want to delete this product?")) {
        this.$store.dispatch("products/deleteProduct", payload).then((data) => {
          this.$toast.success("Product deleted successfully");
          this.gridApi.applyTransaction({ remove: [param] });
        });
      } else {
        this.$toast.error("Product not deleted");
      }
    },
  },
};
</script>
