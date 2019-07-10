<template>
  <b-card class="mt-3">
    <b-container fluid>
      <!-- User Interface controls -->
      <b-row>
        <b-col md="6" class="my-1">
          <b-form-group label-cols-sm="3" label="Filter" class="mb-0">
            <b-input-group>
              <b-form-input v-model="filter" placeholder="Type to Search"></b-form-input>
              <b-input-group-append>
                <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
              </b-input-group-append>
            </b-input-group>
          </b-form-group>
        </b-col>
        <b-col md="6" class="my-1">
          <b-form-group label-cols-sm="3" label="Per page" class="mb-0">
            <b-form-select v-model="perPage" :options="pageOptions"></b-form-select>
          </b-form-group>
        </b-col>
      </b-row>

      <!-- Main table element -->
      <b-table
        show-empty
        stacked="md"
        :items="items"
        :fields="fields"
        :current-page="currentPage"
        :per-page="perPage"
        :filter="filter"
        :sort-by.sync="sortBy"
        :sort-desc.sync="sortDesc"
        :sort-direction="sortDirection"
        @filtered="onFiltered"
      >
        <template slot="from" slot-scope="row">
          <span class="text-monospace font-weight-bold">Date:</span>
          <span class="text-underline">{{ row.item.date }}</span>
          <div v-for="( item, i ) in row.item.from" :key="i">
            <p class="text-overflow">{{ item.from }}</p>
            <p>
              <span class="text-monospace font-weight-bold">Send amount :</span>
              {{ item.send_amount ? item.send_amount : 'No data' }}
            </p>
          </div>
        </template>
        <template slot="to" slot-scope="row">
          <span class="text-underline">&nbsp;</span>
          <h1 v-if="!row.item.to.length">NoData</h1>
          <div v-for="( itemTo, indexTo ) in row.item.to" :key="indexTo">
            <p>{{ itemTo.to }}</p>
            <p>
              <span class="text-monospace font-weight-bold">Received amount :</span>
              {{ itemTo.receive_amount ? itemTo.receive_amount : 'No data' }}
            </p>
          </div>
        </template>
      </b-table>

      <b-row>
        <b-col md="6" class="my-1">
          <b-pagination
            v-model="currentPage"
            :total-rows="totalRows"
            :per-page="perPage"
            class="my-0"
          ></b-pagination>
        </b-col>
      </b-row>
    </b-container>
  </b-card>
</template>

<script>
export default {
  name: "Table",
  props: {
    items: Array
  },
  data() {
    return {
      fields: [
        {
          key: "from",
          label: "From",
          sortable: true,
          sortDirection: "desc",
          'class': "text-overflow"
        },
        { key: "to", label: "To", sortable: true }
      ],
      totalRows: 1,
      currentPage: 1,
      perPage: 5,
      pageOptions: [5, 10, 15],
      sortBy: null,
      sortDesc: false,
      sortDirection: "asc",
      filter: null
    };
  },
  methods: {
    onFiltered(filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.totalRows = filteredItems.length;
      this.currentPage = 1;
    }
  },
  mounted() {
    // Set the initial number of items
    this.totalRows = this.items.length;
  },
  computed: {
    sortOptions() {
      // Create an options list from our fields
      return this.fields
        .filter(f => f.sortable)
        .map(f => {
          return { text: f.label, value: f.key };
        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.text-overflow {
  overflow: hidden;
  width: 370px;
}
@media only screen and (max-width: 768px) {
  .text-overflow {
    width: 100px;
  }
}
</style>
