<template>
    <section class="my-login-signup-section" id="content">
        <div class="page-sign-up">
            <!-- toast messages will be here -->
            <!-- The toast container div -->
            <div class="toast-container" ref="toastContainer">
            <!-- The Bulma toast will be rendered here -->
            </div>
            <div class="columns">
                <div class="column is-5 is-offset-3">
                    <h1 class="title my-login-title">
                        {{$t('loginsignupview.logintitle')}}
                    </h1>
                    <!-- sign up form prevent default action -->
                    <form @submit.prevent="submitForm">
                        <div class="field">
                            <!-- general errors-->
                            <div class="my-errors" v-if="errors.generalErrors.length">
                                <p style="color:red" v-for="error in errors.generalErrors" v-bind:key="error">
                                <span style="color:red !important">*</span> {{ error }}
                                </p>                           
                            </div>
                            <!-- username/email errors-->
                            <div class="my-errors" v-if="errors.usernameOrEmailErrors.length">
                                <p style="color:red" v-for="error in errors.usernameOrEmailErrors" v-bind:key="error">
                                <span style="color:red !important">*</span> {{ error }}
                                </p>                           
                            </div>
                            <!-- users can enter their email address or username to login -->
                            <label class="my-label" for="">{{$t('loginsignupview.username')}}</label>
                            <div class="control">
                                <!-- v-model connects the data var defined below -->
                                <input type="text" class="input" v-model="username_or_email">
                            </div>
                            <!-- password errors-->
                            <div class="my-errors" v-if="errors.passwordErrors.length">
                                <p style="color:red" v-for="error in errors.passwordErrors" v-bind:key="error">
                                <span style="color:red !important">*</span> {{ error }}
                                </p>                           
                            </div>
                            <!-- password -->
                            <label class="my-label" for="">{{$t('loginsignupview.password')}}</label>
                            <div class="field has-addons my-password-field">
                                <div class="control is-expanded input-container">
                                    <!-- show password, type has to be text -->
                                    <input v-if="showPassword" type="text" class="input" v-model="password" />
                                    <!-- hide password, type is password -->
                                    <input v-else type="password" class="input" v-model="password">
                                    <span @click.prevent="toggleShowPassword" class="icon is-small is-right my-eye-icon">
                                        <i class="fas" :class="{ 'fa-eye-slash': showPassword, 'fa-eye': !showPassword }"></i>
                                    </span>
                                </div>
                            </div>
                            <!-- submit form -->
                            <div class="field">
                                <div class="control">
                                    <button :class="['button login-signup-button', { 'login-signup-button-disabled': submitButtonDisabled }]">
                                        <span v-if="submitButtonDisabled" class="spinner-border spinner-border-sm text-small" role="status" aria-hidden="true"></span>
                                        {{$t('loginsignupview.logintitle')}}
                                    </button>
                                </div>
                                <p class="forgot-password-link">
                                    <a style="color:aqua !important; text-decoration: underline;" href="/forgotpassword">{{$t('loginsignupview.forgotpassword')}}</a>
                                </p>  
                            </div>
                            <p v-if="$i18n.locale === 'en'" class="signup-login-reroute">
                                {{$t('loginsignupview.signup1')}} <a style="color:aqua !important; text-decoration: underline;" href="/signup">{{$t('loginsignupview.signup2')}}</a>
                            </p>
                            <p v-else-if="$i18n.locale === 'ja'" >
                                <a class="signup-login-reroute" style="text-decoration: underline;" href="/signup">{{$t('loginsignupview.signup2')}}</a>
                            </p>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'

export default {

    name: 'LogIn',
    data() {
        return {
            username_or_email: '',
            password: '',
            errors: {
                generalErrors: [],
                usernameOrEmailErrors: [],
                passwordErrors: [],
            },            
            showPassword: false,
            submitButtonDisabled: false
        }
    },

    // change button appearance when clicked
    computed: {

        // buttonStyle() {
        //     if (this.submitButtonDisabled) {
        //         // If the button is disabled, apply a default style or any custom style you want
        //         return {

        //             // opacity value (0.65) to control the faded look
        //             backgroundColor: 'rgba(0, 128, 107, 0.1)',
        //             color: 'white'
        //         };
        //     } else {
        //         // If the button is enabled, apply the original background color
        //         return {
        //             backgroundColor: 'rgb(0, 128, 107)',
        //             color: 'white',
        //         };
        //     }
        // },
    },

    // show toast if it exists
    mounted () {
        document.title = 'Login';

        if (this.$store.state.currentAudioElementPlaying === true) {
            this.$store.commit('playPauseController')
        }

        if (this.$route.query.loginwarning) {
            document.querySelector('#content').scrollIntoView()
            toast({
                message: this.$t('modals.redirectoToLogin'),
                type: 'is-warning',
                dismissible: true,
                pauseOnHover: true,
                duration: 2000,
                position: 'center',
                animate: { in: 'fadeIn', out: 'fadeOut' },
            })
        }
    },

    methods: {


        submitForm() {
            // reset errors
            this.errors.generalErrors = []
            this.errors.usernameOrEmailErrors = []
            this.errors.passwordErrors = []


            // validate fields
            // USERNAME/EMAIL
            if (this.username_or_email === '') {
                this.submitButtonDisabled = false;
                this.errors.usernameOrEmailErrors.push(this.$t('loginsignupview.errors.usernameemailerrors'))
            }
            // PASSWORD
            if (this.password === '') {
                this.submitButtonDisabled = false;
                this.errors.passwordErrors.push(this.$t('loginsignupview.errors.passworderrors'))
            }
            // if no errors, submit the form and authenticate user
            if (!this.errors.usernameOrEmailErrors.length && !this.errors.passwordErrors.length ) {

                // disable login button
                this.submitButtonDisabled = true

                // var to hold post data
                // keys must be same strings as model fields in backend api user model
                // values can be named whatever
                const loginFormData = {
                    username: this.username_or_email,
                    password: this.password,
                }

                // send post data to backend server
                axios.post(process.env.VUE_APP_AUTHENTICATE_USERS_API_URL, loginFormData)
                    .then(response => {

                        // set auth token
                        const sf_auth_bearer = response.data.auth_token
                        // set token in store which sets is_authenticated var to true
                        this.$store.commit('setToken', sf_auth_bearer)
                        // setting token in axios header
                        axios.defaults.headers.common['Authorization'] = 'Token ' + sf_auth_bearer
                        // set token in localstorage
                        localStorage.setItem("sf_auth_bearer", sf_auth_bearer)

                        // get user's cart data
                        axios
                            .get(process.env.VUE_APP_GET_CART_URL + '?_=' + Date.now(), 
                                {           
                                    headers: 
                                    { 
                                        'Authorization': `Token ${this.$store.state.sf_auth_bearer}`,
                                        'api-key': process.env.VUE_APP_API_KEY
                                    } 
                            }).then(response => {

                                const cart_data = response.data.cart;
                                if (cart_data.length === 0) {
                                }
                                else {
                                    // there are cart items, clear the cart if the user added items to cart anonymously
                                    this.$store.commit('clearCart')

                                    for (let i = 0; i < cart_data.length; i++) {
                                        const item = cart_data[i];
                                        // add item to cart in store
                                        this.$store.commit('addToCart', item)
                                    }
                                }
                                // populate purchasedTracksList
                                this.getPurchasedTracks();

                                // check if there is a pending route to be redirected to
                                // else go to home
                                // const toPath = this.$route.query.to || '/'
                                // re-route to homepage
                                // this.$router.push(toPath)
                                window.location.href = '/music';


                            })
                            .catch(error => {

                            })
                        
                        // get user pfp if it exists
                        axios
                        .get(process.env.VUE_APP_GET_USER_PFP, 
                            {
                                headers: 
                                    { 
                                        'Authorization': `Token ${this.$store.state.sf_auth_bearer}`,
                                        'api-key': process.env.VUE_APP_API_KEY
                                    } 
                        }).then(response => {
                            
                            const userdata = response.data
                            this.$store.state.profile_pic_background_img = userdata.get_profile_pic

                        })
                        .catch(error => {
                            this.submitButtonDisabled = false;
                        })

                    })
                    .catch(error => {
                        this.submitButtonDisabled = false;
                        if (error.response) {
                            this.errors.generalErrors.push(this.$t('loginsignupview.errors.invalidusernamepassword'))
                        } 
                        
                        else if (error.message) {
                            this.errors.generalErrors.push(this.$t('loginsignupview.errors.generalerrors'))
                        }
                    })
            }
            else {
            }
        },
        toggleShowPassword() {
            this.showPassword = !this.showPassword;
        },
        async getPurchasedTracks() {

            await axios.get(process.env.VUE_APP_GET_TRACK_ORDERS_URL, 
            {
                headers: 
                { 
                  'Authorization': `Token ${this.$store.state.sf_auth_bearer}`,
                  'api-key': process.env.VUE_APP_API_KEY
                }
            }).then(response => {
                if (response.data.length === 0) {
                }
                else {
                    this.$store.commit('populatePurchasedTrackArray', response.data)
                }
                })
                .catch( error => {
                })
        },
    }
}
</script>