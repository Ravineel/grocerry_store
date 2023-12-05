<template>
  <ag-grid-vue
    style="width: 100%; height: 400px"
    :class="themeClass"
    :columnDefs="columnDefs"
    @grid-ready="onGridReady"
    :autoGroupColumnDef="autoGroupColumnDef"
    :defaultColDef="defaultColDef"
    :suppressRowClickSelection="true"
    :groupSelectsChildren="true"
    :rowSelection="rowSelection"
    :rowGroupPanelShow="rowGroupPanelShow"
    :pivotPanelShow="pivotPanelShow"
    :paginationAutoPageSize="true"
    :pagination="true"
    :rowData="rowData"
  ></ag-grid-vue>
</template>

<script>
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css";
import { AgGridVue } from "ag-grid-vue3";

export default {
  components: {
    AgGridVue,
  },
  data: function () {
    return {
      columnDefs: [
        {
          field: "athlete",
          minWidth: 170,
          checkboxSelection: checkboxSelection,
          headerCheckboxSelection: headerCheckboxSelection,
        },
        { field: "age" },
        { field: "country" },
        { field: "year" },
        { field: "date" },
        { field: "sport" },
        { field: "gold" },
        { field: "silver" },
        { field: "bronze" },
        { field: "total" },
        {
          headerName: "Action",
          minWidth: 250,
        },
      ],
      gridApi: null,
      themeClass: "ag-theme-quartz-dark",
      defaultColDef: {
        editable: true,
        enableRowGroup: true,
        enablePivot: true,
        enableValue: true,
        filter: true,
        flex: 1,
        minWidth: 100,
      },
      autoGroupColumnDef: null,
      rowSelection: null,
      rowGroupPanelShow: null,
      pivotPanelShow: null,
      rowData: null,
    };
  },
  created() {
    this.autoGroupColumnDef = {
      headerName: "Group",
      minWidth: 170,
      field: "athlete",
      valueGetter: (params) => {
        if (params.node.group) {
          return params.node.key;
        } else {
          return params.data[params.colDef.field];
        }
      },
      headerCheckboxSelection: true,
      cellRenderer: "agGroupCellRenderer",
      cellRendererParams: {
        checkbox: true,
      },
    };
    this.rowSelection = "multiple";
    this.rowGroupPanelShow = "always";
    this.pivotPanelShow = "always";
  },
  methods: {
    onGridReady(params) {
      this.gridApi = params.api;

      const updateData = (data) => (this.rowData = data);

      fetch("https://www.ag-grid.com/example-assets/olympic-winners.json")
        .then((resp) => resp.json())
        .then((data) => updateData(data));
    },
  },
};

var checkboxSelection = function (params) {
  // we put checkbox on the name if we are not doing grouping
  return params.api.getRowGroupColumns().length === 0;
};

var headerCheckboxSelection = function (params) {
  // we put checkbox on the name if we are not doing grouping
  return params.api.getRowGroupColumns().length === 0;
};
</script>
