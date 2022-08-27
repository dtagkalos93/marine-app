<template>
  <div class="">
    <h1 style="text-align: center;">Marine App</h1>
    <v-data-table
      :page="page"
      :pageCount="numberOfPages"
      :headers="headers"
      :items="vessel_positions"
      :options.sync="options"
      :server-items-length="vesselPosition"
      :loading="loading"
      :footer-props="{
        'items-per-page-options': [25,50,100]
        }"
      class="elevation-1"
    >
    </v-data-table>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "DatatableComponent",
  data() {
    return {
      page: 1,
      vesselPosition: 0,
      numberOfPages: 0,
      vessel_positions: [],
      loading: true,
      options: {},
      headers: [
        { text: "Vessel ID", value: "vessel_id" },
        { text: "Latitude", value: "latitude" },
        { text: "Longitude", value: "longitude" },
        { text: "Position Time", value: "position_time" },
      ],
    };
  },
  watch: {
    options: {
      handler() {
        this.readDataFromAPI();
      },
    },
    deep: true,
  },
  methods: {
    readDataFromAPI() {
      this.loading = true;
      const { page, itemsPerPage } = this.options;
      console.log("Page Number ", page, itemsPerPage);
      let pageNumber = page - 1;
      axios
        .get(
          "http://localhost:8002/vessel-position?limit=" +
            itemsPerPage +
            "&skip=" +
            pageNumber
        )
        .then((response) => {
          this.loading = false;
          this.vessel_positions = response.data.data;
          this.vesselPosition = response.data.total_vessel_position;
          this.numberOfPages = response.data.number_of_pages;
        });
    },
  },
  mounted() {
    this.readDataFromAPI();
  },
};
</script>
