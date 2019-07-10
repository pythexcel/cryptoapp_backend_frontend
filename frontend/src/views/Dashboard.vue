<template>
  <div class="mt-3 mb-5">
    <h2 class="text-center text-white">Dashboard</h2>
    <b-container class="w-75">
      <b-card>
        <b-container class="bv-example-row">
          <b-form @submit="onSubmit">
            <b-row>
              <b-col sm="auto" md="2">
                <b-form-group id="input-group-3" label="Coin" label-for="input-3">
                  <b-form-select id="input-3" v-model="form.symbol" :options="currency" required></b-form-select>
                </b-form-group>
              </b-col>
              <b-col sm="auto" md="10">
                <b-form-group id="input-group-2" label="Your address" label-for="input-2">
                  <b-form-input
                    id="input-2"
                    v-model="form.address"
                    required
                    placeholder="Enter public address"
                  ></b-form-input>
                </b-form-group>
              </b-col>
            </b-row>
            <b-row>
              <b-col>
                <b-form-group id="input-group-3" label="Preferred safename" label-for="input-3">
                  <b-form-input
                    id="input-3"
                    v-model="form.Preferred_Safename"
                    required
                    placeholder="Enter preferred safename"
                  ></b-form-input>
                </b-form-group>
              </b-col>
            </b-row>
            <b-row>
              <b-col>
                <b-form-group id="input-group-4" label="Email" label-for="input-4">
                  <b-form-input
                    id="input-4"
                    v-model="form.Email"
                    type="email"
                    required
                    placeholder="Enter email"
                  ></b-form-input>
                </b-form-group>
              </b-col>
            </b-row>
            <b-row v-if="errorMessage">
              <b-col>
                <div class="text-danger mb-2">{{ errorMessage }}</div>
              </b-col>
            </b-row>
            <b-row>
              <b-col>
                <b-form-group id="input-group-5" label-for="input-5">
                  <b-button
                    :disabled="loading"
                    type="submit"
                    style="width: 80px;"
                    variant="primary"
                  >
                    <span v-if="loading">
                      <b-spinner small></b-spinner>
                    </span>
                    <span v-if="!loading">Submit</span>
                  </b-button>
                </b-form-group>
              </b-col>
            </b-row>
          </b-form>
        </b-container>
      </b-card>
      <b-card class="mt-3" title="Balance" v-if="Object.keys(transactions).length">
        <b-card-text>
          <span class="font-weight-bold">Preferred Safename:</span>
          {{ transactions.Preferred_Safename ? transactions.Preferred_Safename : 'No Data' }}
        </b-card-text>
        <b-card-text>
          <span class="font-weight-bold">Amount Received:</span>
          {{ transactions.amountReceived ? transactions.amountReceived : 'No Data' }}
        </b-card-text>
        <b-card-text>
          <span class="font-weight-bold">Amount AmountSent:</span>
          {{ transactions.amountSent ? transactions.amountSent : 'No data' }}
        </b-card-text>
        <b-card-text>
          <span class="font-weight-bold">Balance:</span>
          {{ transactions.balance }}
        </b-card-text>
        <b-card-text>
          <span class="font-weight-bold">Coin:</span>
          {{ transactions.symbol }}
        </b-card-text>
        <b-card-text>
          <span class="font-weight-bold">Your address:</span>
          {{ transactions.address }}
        </b-card-text>
        <b-card-text>
          <span class="font-weight-bold">Record_id:</span>
          {{ transactions.record_id }}
        </b-card-text>
      </b-card>
      <!-- Table Component -->
      <b-card class="mt-3" title="SWS history" v-if="Object.keys(transactions).length">
        <Table :items="transactions.transactions" />
      </b-card>
    </b-container>
  </div>
</template>

<script>
// @ is an alias to /src
import Table from "@/components/Table.vue";
import { sync, get, call } from "vuex-pathify";
export default {
  name: "dashboard",
  components: {
    Table
  },
  data() {
    return {
      loading: false,
      form: {
        symbol: null,
        address: "",
        Email: "",
        Preferred_Safename: ""
      },
      currency: []
      // errorMessage: ""
    };
  },
  computed: {
    currencySymbol: sync("dashboard/currencySymbol"),
    transactions: sync("dashboard/transactions"),
    errorMessage: sync("dashboard/errorMessage")
  },
  created() {
    this.fetchCurrencySymbols();
  },
  methods: {
    api_getSymbols: call("dashboard/getCurrencySymbols"),
    api_saveTransactionToDB: call("dashboard/saveTransactionToDB"),
    onSubmit(evt) {
      evt.preventDefault();
      this.loading = true;
      this.errorMessage = "";
      // extracting type_id from COIN dropdown
      var getTypeId = this.currencySymbol.find(ele => {
        if (ele.symbol === this.form.symbol) {
          return ele;
        }
      });
      this.form.type_id = getTypeId.type_id;
      this.api_saveTransactionToDB(this.form)
        .then(res => {
          this.loading = false;
          if (res.data.msg) {
            this.errorMessage = res.data.msg;
            this.transactions = {};
          }
          this.clearForm();
        })
        .catch(err => {
          this.loading = false;
          this.clearForm();
        });
    },
    clearForm() {
      (this.form.symbol = null), (this.form.address = "");
      (this.form.Email = ""), (this.form.Preferred_Safename = "");
    },
    fetchCurrencySymbols() {
      this.currencySymbol = [];
      this.currency.push({ text: "Select One", value: null });
      this.api_getSymbols().then(res => {
        this.setCurrencySymbolDropDown();
      });
    },
    // set currency symbol dropdown Data
    setCurrencySymbolDropDown() {
      this.currencySymbol.forEach(element => {
        this.currency.push(element.symbol);
      });
    }
  }
};
</script>
<style >
body {
  background: #616161; /* fallback for old browsers */
  background: -webkit-linear-gradient(
    to bottom,
    #9bc5c3,
    #616161
  ); /* Chrome 10-25, Safari 5.1-6 */
  background: linear-gradient(
    to bottom,
    #9bc5c3,
    #616161
  ); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */

  /* background-repeat: no-repeat; */
  background-attachment: fixed;
}
</style>

