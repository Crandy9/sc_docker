<template>
    <section class="flp-section">
      <!-- flps -->
      <section class="flp-title-section">
        <!-- title -->
        <div class="column is-12">
          <h2 class="flp-main-title is-size-3 has-text-centered has-text-white">
            My FLPs
          </h2>
          <p style="padding-top: 1rem;">
            <a style="color:chartreuse !important; text-decoration: none;" target="_blank" href="https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/fformats_save_flp.htm">{{$t('flpview.whatsanflp')}}</a>
          </p>
        </div>
      </section>
      <section class="flp-items-section">
        <!-- unordered list of flps -->
        <ul class="flp-list">
          <!-- Vue for loop -->
          <div v-for="flp, index in flps" v-bind:key="flp.id" class="flp-list-div">
            <li class="flp-list-item" v-bind:id="flp.id">
                <div class="flp-title">
                    <!-- flp name -->
                    <span class="flp-title-inner">
                        {{ flp.flp_name }}
                    </span>
                </div>
                <div>
                  <!-- check if this item is already in the cart; remove it if clicked -->
                  <a class="flps-in-cart-button button is-small price-button has-text-weight-medium" 
                    v-if="checkIfFlpIsInCart(flp)" 
                    @click.stop="modalOpened = false; removeFromCart(flp.id)" data-target="my-modal-id">
                    {{$t('cartview.addedtocart')}}
                  </a>
                  <!-- trigger modal with options to proceed to checkout, or add item to cart -->
                  <a class="button is-small is-black price-button has-text-weight-medium" 
                    v-else-if="flp.flp_is_free"
                    @click.stop="modalOpened = true; setFlpId(flp.id);" data-target="my-modal-id">
                    {{$t('cartview.free')}}
                  </a>
                  <a class="button is-small is-black price-button has-text-weight-medium" 
                    v-else-if="$store.state.region === 'US'" 
                    @click.stop="modalOpened = true; setFlpId(flp.id);" data-target="my-modal-id">
                    ${{ flp.usd_price }}
                  </a>
                  <a class="button is-small is-black price-button has-text-weight-medium" 
                    v-else-if="$store.state.region === 'JP'" 
                    @click.stop="modalOpened = true; setFlpId(flp.id);" data-target="my-modal-id">
                    ¥{{ flp.jpy_price }}
                  </a>
                </div>
            </li>
          </div>
        </ul>
      </section>
      <!-- modal -->
      <Transition>
        <div v-if="modalOpened" id="my-modal-id" class="modal" v-bind:class="{'is-active':modalOpened}">
          <div class="modal-background"></div>
            <div class="modal-card">
              <header class="modal-card-head">
                <p v-if="isFree" class="modal-card-title">{{$t('cartview.downloadnow?')}}</p>
                <p v-else class="modal-card-title">{{$t('cartview.buynow?')}}</p>
                <button @click="modalOpened = false" class="delete" aria-label="close"></button>
              </header>
              <!-- free US -->
              <section v-if="isFree && $store.state.language === 'en'" class="modal-card-body">
                {{$t('cartview.doyouwannadownload?part1')}}"{{ FlpName }}" {{$t('cartview.doyouwannadownload?part2')}}
              </section>
              <!-- free JA -->
              <section v-else-if="isFree && $store.state.language === 'ja'" class="modal-card-body">
                "{{ FlpName }}" {{$t('cartview.doyouwannadownload?part1')}}
              </section>
              <!-- purchase US -->
              <section v-else-if="$store.state.language === 'en'" class="modal-card-body">
                {{$t('cartview.doyouwannabuy?part1')}}"{{ FlpName }}" {{$t('cartview.doyouwannabuy?part2')}}
              </section>
              <!-- purchase JA -->
              <section v-else-if="$store.state.language === 'ja'" class="modal-card-body">
                "{{ FlpName }}"{{$t('cartview.doyouwannabuy?part1')}}
              </section>
              <footer class="modal-card-foot">
                <div v-if="$store.state.isAuthenticated">
                  <!-- pass in the flpname of the free flp to be downloaded -->
                  <button v-if="isFree" @click="modalOpened = false; show = false; purchaseButtonClicked = false; downloadFreeNow(FlpID);" class="my-modal-button-buy-now button">{{$t('cartview.downloadnow')}}</button>
                  <!-- trigger stripe payment on this item only -->
                  <button v-else @click="modalOpened = false; show = true; purchaseButtonClicked = true; scrollToBottom();" class="my-modal-button-buy-now button">{{$t('cartview.buynow')}}</button>
                  <!-- if adding to cart, add the item to cart and close modal -->
                  <button @click.stop="addFlpToCart(FlpID); modalOpened = false" class="my-modal-button-add-to-cart button">{{$t('cartview.addtocart')}}</button>
                </div>
                <!-- if user is not logged in, redirect to login screen -->
                <div v-else>
                  <!-- pass in the flpname of the free flp to be downloaded -->
                  <a v-if="isFree" role="button" @click='redirectToLogin()' class="my-modal-button-buy-now button">{{$t('cartview.downloadnow')}}</a>
                  <!-- trigger stripe payment on this item only -->
                  <a v-else role="button" @click='redirectToLogin()' class="my-modal-button-buy-now button">{{$t('cartview.buynow')}}</a>
                  <!-- if adding to cart, add the item to cart and close modal -->
                  <a role="button" @click='redirectToLogin()' class="my-modal-button-add-to-cart button">{{$t('cartview.addtocart')}}</a>
                </div>
              </footer>
            </div>
        </div>
      </Transition>
      <!-- end modal -->
        <h2 class="flp-guide is-size-5 has-text-centered has-text-warning">
          {{$t('flpview.about')}}
        </h2>
        <p class="flp-guide has-text-danger">
          {{$t('flpview.warning')}}: 
          <p v-if="$store.state.language === 'en'" class="flp-guide has-text-white">
            {{$t('flpview.flstudiowarningmsgp1')}}
            <a target="blank"  class="flp-file-links" href="https://www.image-line.com/fl-studio/compare-editions/">
              {{$t('flpview.here')}}
            </a> 
            {{$t('flpview.flstudiowarningmsgp2')}}
          </p>
          <p v-else-if="$store.state.language === 'ja'" class="flp-guide has-text-white">
            {{$t('flpview.flstudiowarningmsgp1')}}
            <a target="blank"  class="flp-file-links" href="https://www.image-line.com/fl-studio/compare-editions/">
              {{$t('flpview.here')}}
            </a> 
            {{$t('flpview.flstudiowarningmsgp2')}}
          </p>
        </p>
        <div class="is-size-6" style="padding: 1rem;">
          <p style="padding:1.2rem;">
            <a class="flp-file-links" target="blank" href="https://www.homemusicmaker.com/open-flp-files-fl-studio-demo">
              - {{$t('flpview.openingfllink')}}
            </a>
          </p>
        </div>
    </section>

    <!-- FOR BUY NOW -->
    <!-- stripe payment form copied from cart view -->
      <div style="z-index: 9999;" class="my-checkout-div"
        :style="showPaymentForm()" v-bind:class="{'is-active': purchaseButtonClicked}" ref="paymentFormTop">
          <!-- <div class="modal-background"></div> -->
            <div class="card">
              <header class="card-head">
                <!-- <p class="card-title">{{$t('paymentmodal.modaltitle')}}</p> -->
                <button class="delete close-button" @click="show = false; clearFields(); purchaseButtonClicked = false;" aria-label="close"></button>
              </header>
              <section class="card-body">
                <div class="page-checkout">
                  <div class="columns is-multiline">
                      <div class="column is-12 box">
                        <h2 style= "text-align: center;" class="payment-form-sub subtitle has-text-black has-text-center is-underlined">{{$t('paymentmodal.paymentdetails')}}</h2>
                        <h2 class="subtitle has-text-black">{{$t('paymentmodal.billingaddress')}}</h2>
                        <!-- <p class="has-text-danger mb-4">* All fields are required</p> -->
                        <div class="columns is-multiline">
                          <div class="column is-6">
                            <!-- name errors-->
                            <div v-if="errors.nameErrors.length">
                                <p class="my-errors" style="color:red" v-for="error in errors.nameErrors" v-bind:key="error">
                                <span style="color:red !important">*</span> {{ error }}
                                </p>                        
                            </div>
                            <div class="field">
                              <label class="my-label has-text-black">{{$t('paymentmodal.name')}}</label>
                              <div class="control">
                                  <input type="text" class="input" :placeholder="$t('paymentmodal.placeholdername')" v-model="name">
                              </div>
                            </div>
                            <!-- email errors-->
                            <div v-if="errors.emailErrors.length">
                                <p class="my-errors" style="color:red" v-for="error in errors.emailErrors" v-bind:key="error">
                                <span style="color:red !important">*</span> {{ error }}
                                </p>                        
                            </div>
                            <div class="field">
                              <label class="my-label has-text-black">{{$t('paymentmodal.email')}}</label>
                              <div class="control">
                                  <input type="email" class="input" placeholder="123@my-email.com" v-model="email">
                              </div>
                            </div>
                            <!-- address1 errors-->
                            <div v-if="errors.address1Errors.length">
                                <p class="my-errors" style="color:red" v-for="error in errors.address1Errors" v-bind:key="error">
                                <span style="color:red !important">*</span> {{ error }}
                                </p>                        
                            </div>
                            <div class="field">
                              <label class="my-label has-text-black">{{$t('paymentmodal.street1')}}</label>
                              <div class="control">
                                  <input type="text" class="input" :placeholder="$t('paymentmodal.street1placeholder')" v-model="address1">
                              </div>
                            </div>
                              <!-- address2 errors-->
                              <div v-if="errors.address2Errors.length">
                                <p class="my-errors" style="color:red" v-for="error in errors.address2Errors" v-bind:key="error">
                                <span style="color:red !important">*</span> {{ error }}
                                </p>                        
                            </div>
                            <div class="field">
                              <label class="my-label has-text-black">{{$t('paymentmodal.street2')}}</label>
                              <div class="control">
                                  <input type="text" class="input" :placeholder="$t('paymentmodal.street2placeholder')"  v-model="address2">
                              </div>
                            </div>
                          </div>
                          <div class="column is-6">
                              <!-- country errors-->
                              <div v-if="errors.countryErrors.length">
                                <p class="my-errors" style="color:red" v-for="error in errors.countryErrors" v-bind:key="error">
                                <span style="color:red !important">*</span> {{ error }}
                                </p>                        
                              </div>
                              <div class="field">
                                <label class="my-label has-text-black">{{$t('paymentmodal.country')}}</label>
                                <div class="control has-icons-left">
                                    <select class="input" v-model="country" name="country" id="id_country">
                                      <option style="color:rgba(0,0,0,0.4) !important" value="" disabled selected hidden>
                                          {{$t('paymentmodal.countryplaceholder')}}
                                      </option>
                                      <option v-for="cya in $store.state.countries" :value="cya.countryval" style="color: black !important;">{{cya.countryname}}</option>
                                    </select>
                                    <div class="icon is-small is-left">
                                      <i class="fas fa-globe" style="color: rgb(55,195,255)"></i>
                                    </div>
                                </div>
                              </div>
                              <!-- statepref errors-->
                              <div v-if="errors.statePrefErrors.length">
                                <p class="my-errors" style="color:red" v-for="error in errors.statePrefErrors" v-bind:key="error">
                                <span style="color:red !important">*</span> {{ error }}
                                </p>                        
                              </div>
                              <!-- prefectures -->
                              <div v-if="this.country === 'JP'" class="field">
                                <label class="my-label has-text-black">{{$t('paymentmodal.pref')}}</label>
                                <div class="control">
                                  <select v-model="statePref" name="statepref" class="input">
                                    <option value="" disabled selected hidden>
                                            {{$t('paymentmodal.prefplaceholder')}}
                                    </option>
                                    <option v-for="pref in $store.state.prefectures" :key="pref.prefval" :value="pref.prefval" style="color: black !important;">{{pref.prefval}}</option>
                                  </select>
                                </div>
                              </div>
                              <!-- states -->
                              <div v-if="this.country === 'US'" class="field">
                                <label class="my-label has-text-black">{{$t('paymentmodal.state')}}</label>
                                <div class="control">
                                  <select v-model="statePref" name="statepref" class="input">
                                    <option value="" disabled selected hidden>
                                            {{$t('paymentmodal.stateplaceholder')}}
                                    </option>
                                    <option v-for="state in $store.state.usstates" :key="state.stateval" :value="state.stateval" style="color: black !important;">{{state.statename}}</option>
                                  </select>
                                </div>
                              </div>
                              <!-- post code errors-->
                              <div v-if="errors.zipcodeErrors.length">
                                <p class="my-errors" style="color:red" v-for="error in errors.zipcodeErrors" v-bind:key="error">
                                <span style="color:red !important">*</span> {{ error }}
                                </p>                        
                              </div>
                              <div class="field">
                                <label class="my-label has-text-black">{{$t('paymentmodal.postcode')}}</label>
                                <div class="control">
                                    <input type="text" class="input" :placeholder="$t('paymentmodal.postcodeplaceholder')" v-model="zipcode">
                                </div>
                              </div>
                          </div>
                        </div>
                      </div>
                      <hr>
                  </div>
                </div>
                <!-- general errors -->
                <div v-if="errors.generalErrors.length">
                  <p class="my-errors" style="text-align: center; color:red; padding-bottom: 1rem; padding-inline: 2.2rem;" v-for="error in errors.generalErrors" v-bind:key="error">
                    <span style="color:red !important">*</span> {{ error }}
                  </p>                        
                </div>
                <div class="mb-5 has-text-black">
                  <h2 class="my-credit-card-subtitle has-text-black">{{ $t('paymentmodal.cardinfo') }}</h2>
                </div>
                <div class="stripe-card-div">
                  <div id="card-element" class="mb-5 control"></div>
                </div>
              </section>
              <!-- for usd -->
              <footer v-if="$store.state.region === 'US'" class="card-foot">
                <p class="my-subtotal has-text-black">
                  <span>{{$t('cartview.total')}}:</span>
                  <span style="padding-left: 0.5rem;" data-cart--cart-target="total">${{ usdPrice }}</span>
                </p>
                <p class="my-subtotal has-text-black">
                  <span>{{$t('cartview.tax')}}:</span>
                  <span style="padding-left: 0.5rem;" data-cart--cart-target="total">${{ calculateUsdTaxes }}</span>
                </p>
                <p class="my-subtotal has-text-black">
                  <span>{{$t('cartview.subtotal')}}:</span>
                  <span style="padding-left: 0.5rem;" data-cart--cart-target="total">${{ calculateUsdSubtotal }}</span>
                </p>
                <button @click.stop="submitForm();" :disabled="paymentProcessing" class="my-button-buy-now button">
                  <span v-if="paymentProcessing">
                    {{$t('paymentmodal.paymentprocessing')}}
                  </span>
                  <span v-else>
                    {{$t('paymentmodal.pay')}} ${{ calculateUsdSubtotal }}
                  </span>                </button>
                <!-- if adding to cart, add the item to cart and close modal -->
                <button @click="show = false; clearFields(); checkoutClicked = false;" class="my-button-cancel button">
                  {{$t('paymentmodal.cancel')}}
                </button>
              </footer>
              <!-- for jpy -->
              <footer v-else-if="$store.state.region === 'JP'" class="card-foot">
                <p class="my-subtotal has-text-black">
                  <span>{{$t('cartview.total')}}:</span>
                  <span style="padding-left: 0.5rem;" data-cart--cart-target="total">¥{{ jpyPrice }}</span>
                </p>
                <p class="my-subtotal has-text-black">
                  <span>{{$t('cartview.tax')}}:</span>
                  <span style="padding-left: 0.5rem;" data-cart--cart-target="total">¥{{ calculateJpyTaxes }}</span>
                </p>
                <p class="my-subtotal has-text-black">
                  <span>{{$t('cartview.subtotal')}}:</span>
                  <span style="padding-left: 0.5rem;" data-cart--cart-target="total">¥{{ calculateJpySubtotal }}</span>
                </p>
                <button @click.stop="submitForm();" :disabled="paymentProcessing" class="my-button-buy-now button">
                  <span v-if="paymentProcessing">
                    {{$t('paymentmodal.paymentprocessing')}}
                  </span>
                  <span v-else>
                    {{$t('paymentmodal.pay')}} ¥{{ calculateJpySubtotal }}
                  </span>                
                </button>
                <!-- if adding to cart, add the item to cart and close modal -->
                <button @click="show = false; clearFields(); checkoutClicked = false;" class="my-button-cancel button">
                  {{$t('paymentmodal.cancel')}}
                </button>
              </footer>
            </div>
      </div>
  </template>

<!-- modal animation fade-in/out -->
<style>
  .v-enter-active,
  .v-leave-active {
    transition: opacity 0.3s ease;
  }

  .v-enter-from,
  .v-leave-to {
    opacity: 0;
  }
</style>
  
  <script>
  // @ is an alias to /src
  
  // use axios to get api data from backend to frontend
  // axios was installed during initial vue setup. found in package.json
  // need to import axios in main.js as well
  import axios from 'axios'
  // for pop up notifying user about added item to cart
  import { toast } from 'bulma-toast'

  export default {
    name: 'Flps',
    data() {
      return {
        paymentProcessing: false,
        purchaseButtonClicked: false,
        show: false,
        usdPrice: '',
        jpyPrice: '',
        usdTaxRate: .0,
        jpyTaxRate: 0.1,
        usdTax: '',
        jpyTax: '',
        usdSubTotal: '',
        jpySubtotal:'',
        modalOpened: false,
        flps: [],
        FlpID: '',
        FlpName: '',
        isFree: '',
        // stripe stuff
        stripe: {},
        card: {},
        name: '',
        email: '',
        // phone: '',
        address1: '',
        address2:'',
        statePref: '',
        country: '',
        zipcode: '',
        errors: {
                generalErrors: [],
                nameErrors: [],
                emailErrors: [],
                // phoneErrors: [],
                address1Errors: [],
                address2Errors: [],
                statePrefErrors: [],
                countryErrors: [],
                zipcodeErrors: [],
            },      
        // check if this a USD or JPY payment
        isUsd: true,
      }
    },
  
    components: {
    },

    mounted() {

      if (this.$store.state.isAuthenticated == true) {
        this.getFlps();
      }

      // show samples only
      else {
        this.getLimitedFlps();
      }

      document.addEventListener('click', this.closeModalOnWindowClick);
      this.$store.state.region === 'US' ? this.stripe = Stripe(process.env.VUE_APP_STRIPEPK, {locale: 'en'}) : this.stripe = Stripe(process.env.VUE_APP_STRIPEPK, {locale: 'ja'})
      const elements = this.stripe.elements();
      this.card = elements.create('card', { hidePostalCode: true })
      this.card.mount('#card-element')
    },

    computed: {

      calculateUsdTaxes() {
        var taxAmount = (parseFloat(this.usdTaxRate * this.usdPrice))
        this.usdTax = taxAmount.toFixed(2);
        return this.usdTax
      },
      calculateUsdSubtotal() {
        // prepending unary operator to these values to treat them as numbers
        // instead of strings for tax calc
        this.usdSubTotal = parseFloat(((this.usdPrice) + (+this.usdTax))).toFixed(2);
        return this.usdSubTotal;
      },

      calculateJpyTaxes() {
        var taxAmount = Math.round(parseFloat(this.jpyTaxRate * this.jpyPrice));

        this.jpyTax = taxAmount;
        return this.jpyTax
      },
      calculateJpySubtotal() {
        this.jpySubtotal = Math.round(parseFloat(this.jpyPrice + this.jpyTax));

        return this.jpySubtotal
      },

    },
    // functions defined here
    methods: {

      // redirect to login screen
      redirectToLogin() {
        // redirect and show toast
        this.$router.push({ path: '/login', query: { loginwarning: true }})
      },
      // scroll to top of payment form
      scrollToBottom() {
        // wait until modal closes, then scroll to payment form
        this.$nextTick(() => this.$refs["paymentFormTop"].scrollIntoView({ behavior: "smooth" }))
      },
      // BUY NOW METHODS
      submitForm() {
        this.paymentProcessing = true;
        this.errors.generalErrors = []
        this.errors.nameErrors = []
        this.errors.emailErrors = []
        // this.errors.phoneErrors = []
        this.errors.address1Errors = []
        this.errors.address2Errors = []
        this.errors.statePrefErrors = []
        this.errors.countryErrors = []
        this.errors.zipcodeErrors = []

        if (this.name === '') {
            this.paymentProcessing = false;
            this.errors.nameErrors.push(this.$t('myaccountview.namefieldmissing'))
        }
        if (this.email === '') {
            this.paymentProcessing = false;
            this.errors.emailErrors.push(this.$t('myaccountview.emailreq'))
        }
        if (!this.email.includes('@')) {
            this.paymentProcessing = false;
            this.errors.emailErrors.push(this.$t('myaccountview.emailreq'))
        }   

        // const phoneNumberRegex = /^[0-9-]+$/;

        // if (!this.phone) {
        //     this.paymentProcessing = false;
        //     this.errors.phoneErrors.push(this.$t('myaccountview.phonefieldmissing'))
        // }
        // else if (!phoneNumberRegex.test(this.phone)) {
        //     this.paymentProcessing = false;
        //     this.errors.phoneErrors.push(this.$t('myaccountview.phonefieldmissing'))
        // }   
        if (this.address1 === '') {
            this.paymentProcessing = false;
            this.errors.address1Errors.push(this.$t('myaccountview.addressfieldmissing'))
        }
        if (this.statePref === '') {
            this.paymentProcessing = false; 
            this.errors.statePrefErrors.push(this.$t('myaccountview.statefieldmissing'))
        }        
        if (this.country === '') {
            this.paymentProcessing = false;
            this.errors.countryErrors.push(this.$t('myaccountview.countryfieldmissing'))
        }
        if (this.zipcode === '') {
            this.paymentProcessing = false;
            this.errors.zipcodeErrors.push(this.$t('myaccountview.zipcodefieldmissing'))
        }

        // if there are no form validation errors, process payment
        if (
            !this.errors.nameErrors.length &&
            !this.errors.emailErrors.length &&
            !this.errors.address1Errors.length &&
            !this.errors.address2Errors.length &&
            !this.errors.statePrefErrors.length &&
            !this.errors.countryErrors.length &&
            !this.errors.zipcodeErrors.length &&
            !this.errors.generalErrors.length
          ) {
            // set loading animation icon
            this.$store.commit('setIsLoading', true)

            // create stripe token based on user card input
            this.stripe.createToken(this.card).then(result => {                    
                if (result.error) {
                    this.$store.commit('setIsLoading', false)
                    this.paymentProcessing = false;
                    this.errors.generalErrors.push(this.$t('cartview.stripeerror'))
                } 
                // if there are no stripe processing errors
                else {
                    this.processPayment(result.token)
                }
            })
          }
      },
      // single flp purchase
      async processPayment(token) {

        // FOR FRONTEND TO PREPARE FOR DOWNLOADS
        this.$store.state.downloadType = 'singleFlpDownload';
        var index = this.flps.findIndex(x => x.id === this.FlpID);
        const flp_obj = {
          flp_zip: this.flps[index].flp_zip,
          flp_name: this.flps[index].flp_name
        }

        this.$store.state.downloadableItems = []
        this.$store.state.downloadableItems.push(flp_obj)


        const flp_items = []
        const flp_obj_for_backend = {
          flp: this.FlpID,
          usd_flp_price: this.usdPrice,        
          jpy_flp_price: this.jpyPrice,
        }
        flp_items.push(flp_obj_for_backend)

        var jpy_paid_amount = 0
        var usd_paid_amount = 0
        // set currency based on language which is being used to set the region as well
        this.$store.state.region === 'US' ? (usd_paid_amount = this.calculateUsdSubtotal, jpy_paid_amount = 0) : (usd_paid_amount = 0, jpy_paid_amount = this.calculateJpySubtotal)
      
        // get user billing data as well as stripe token and all
        // cart items, both flps and tracks
        const data = {
          'name': this.name,
          'email': this.email,
          // 'phone': this.phone,
          'address1': this.address1,
          'address2': this.address2,
          'statePref': this.statePref,
          'country': this.country,
          'zipcode': this.zipcode,
          'flp_items': flp_items,
          'stripe_token': token.id,
          'jpy_paid_amount': jpy_paid_amount,
          'usd_paid_amount': usd_paid_amount,
        }

        // post data to server; have to send token as well
        const flp_id = this.FlpID
        const isfree = false    
        await axios
        .post(
          `${process.env.VUE_APP_CHECKOUT_API_URL}flp/${flp_id}/${isfree}`, 
          data,  
          {
            headers: 
                { 
                  'Authorization': `Token ${this.$store.state.sf_auth_bearer}`,
                  'api-key': process.env.VUE_APP_API_KEY
                }
          }
        )
        .then(response => {

          // redirect to thank you page
          this.paymentProcessing = false;
          this.$router.push('/thankyou')
        })
        .catch(error => {
          this.paymentProcessing = false;
          this.errors.generalErrors.push(this.$t('myaccountview.generror'))
        })
        this.$store.commit('setIsLoading', false)
      },

      showPaymentForm() {
        return this.show === true ? {display: 'block'} : {display: 'none'}
      },
        
      clearFields() {
        this.name = ''
        this.email = ''
        // this.phone = ''
        this.address1 = ''
        this.address2 = ''
        this.zipcode = ''
        this.statePref = '',
        this.country = '',
        this.errors.generalErrors = []
        this.errors.nameErrors = []
        this.errors.emailErrors = []
        // this.errors.phoneErrors = []
        this.errors.address1Errors = []
        this.errors.address2Errors = []
        this.errors.statePrefErrors = []
        this.errors.countryErrors = []
        this.errors.zipcodeErrors = []
      },

      // download free flp now
      async downloadFreeNow(id) {

          // FOR FRONTEND TO PREPARE FOR DOWNLOADS
          this.$store.state.downloadType = 'singleFlpDownload';
          var index = this.flps.findIndex(x => x.id === id);

          const flp_obj = {
            flp_zip: this.flps[index].flp_zip,
            flp_name: this.flps[index].flp_name
          }

          this.$store.state.downloadableItems = []
          this.$store.state.downloadableItems.push(flp_obj)

          const flp_items = []

          const flp_obj_for_backend = {
            flp: this.FlpID,
          }

          flp_items.push(flp_obj_for_backend)

          // get user billing data as well as stripe token and all
          const data = {
            'flp_items': flp_items,
          }

          // post data to server; have to send token as well
          const flp_id = id
          const isfree = true

          await axios
          .post(
            `${process.env.VUE_APP_CHECKOUT_API_URL}flp/${flp_id}/${isfree}`, 
            data,  
            {
              headers: 
                { 
                  'Authorization': `Token ${this.$store.state.sf_auth_bearer}`,
                  'api-key': process.env.VUE_APP_API_KEY
                } 
            }
          )
          .then(response => {
              // redirect to thank you page
              this.paymentProcessing = false;
              this.$router.push('/thankyou')
          })
          .catch(error => {
            this.paymentProcessing = false;
            this.errors.generalErrors.push(this.$t('myaccountview.generror'))
          })
          this.$store.commit('setIsLoading', false)


      },
      // called in modal popup on FREE or price button click
      setFlpId(flp) {
        // set flp name and whether it is free well to show in modal popup
        const item = this.flps.find(item => item.id === flp)
        this.FlpName = item.flp_name;
        this.isFree = item.flp_is_free;
        this.FlpID = flp;
        this.usdPrice = item.usd_price;
        this.jpyPrice = item.jpy_price;
      },

      closeModalOnWindowClick() {
        if (this.modalOpened === false) {

        }
        else if (this.modalOpened === true) {
          this.modalOpened = false;

        }
      },


      async getLimitedFlps() {

        // loading bar while api data is getting fetched
        this.$store.commit('setIsLoading', true);

        // replace the API path with env var
        // .get requests API data from server via HTTP GET
        // .then will take the response data and populate the empty flps list above
        await axios.get(process.env.VUE_APP_LIMITED_FLPS_API_URL,
        { 
          headers: { 
            'api-key': process.env.VUE_APP_API_KEY
          }
        }).then(response => {
            this.flps = response.data
            document.title = 'Flps'
          })
          .catch(error => {
          })

        // stop loading bar after api data is fetched
        this.$store.commit('setIsLoading', false);
      },

      // make this method async and axios.get to await to make sure setIsLoading isn't set to false
      // until axios finished fetching api data
      async getFlps() {

        // loading bar while api data is getting fetched
        this.$store.commit('setIsLoading', true);

        // replace the API path with env var
        // .get requests API data from server via HTTP GET
        // .then will take the response data and populate the empty flps list above
        await axios.get(process.env.VUE_APP_FLPS_API_URL,
        { 
          headers: { 
            'api-key': process.env.VUE_APP_API_KEY
          }
        }).then(response => {
            this.flps = response.data
            document.title = 'Flps'
          })
          .catch(error => {
          })

        // stop loading bar after api data is fetched
        this.$store.commit('setIsLoading', false);
      },
      // add to cart
      addFlpToCart(flp) {


        // check if cart has 10 items already
        let cartSize = this.$store.state.cart.itemsInCart.length;
        if (cartSize == 10) {

          toast({
            message: this.$t('modals.cartFull'),
            type: 'is-warning',
            dismissible: true,
            pauseOnHover: true,
            duration: 4000,
            position: 'center',
            animate: { in: 'fadeIn', out: 'fadeOut' },
          })

          return;
        }
        // get specific flp added to cart
        const item = this.flps.find(item => item.id === flp)

        // calls store/index.js addToCart function
        this.$store.commit('addToCart', item)
        // show toast msg to user https://www.npmjs.com/package/bulma-toast
        // toast fadein/out animation requires animate.css. See README
        toast({
          message: item.flp_name + ' ' + this.$t('modals.addedtocart'),
          type: 'is-info',
          dismissible: true,
          pauseOnHover: true,
          duration: 2000,
          position: 'bottom-right',
          animate: { in: 'fadeIn', out: 'fadeOut' },
        })
      },
      // remove from cart
      removeFromCart(removeItemID) {
        // get specific track added to cart
        const item = this.flps.find(item => item.id === removeItemID)
        // pass entire json track/flp obj to removeFromCart function
        this.$store.commit('removeFromCart', item)
        toast({
          message: item.flp_name + ' ' + this.$t('modals.removedfromcart'),
          type: 'is-danger',
          dismissible: true,
          pauseOnHover: true,
          duration: 2000,
          position: 'bottom-right',
          animate: { in: 'fadeIn', out: 'fadeOut' },
        })
      },
      // check if an item clicked is already in the cart
      checkIfFlpIsInCart(flp) {
        const pendingFlpCartItem = 
        this.
        $store.
        state.
        cart.
        itemsInCart.
        filter(i => i.flp_name === flp.flp_name)
          if (pendingFlpCartItem.length) {
            return true;
          }
      }
    }
  }
  </script>