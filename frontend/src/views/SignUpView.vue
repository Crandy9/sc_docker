<template>
    <section class="my-login-signup-section">
        <div class="page-sign-up">
            <div class="columns">
                <div class="column is-6 is-offset-3">
                    <h1 class="title">
                        {{$t('loginsignupview.signuptitle')}}
                    </h1>
                    <!-- sign up form prevent default action -->
                    <form @submit.prevent="submitForm">
                        <div class="field">
                            <!-- pfp (not required) -->
                            <div class="my-account-pfp-container">
                                <input
                                    type="file"
                                    ref="fileInput"
                                    @change="handleFileUpload"
                                    style="display: none;">
                                <!-- if the user hasn't uplopaded a pfp yet -->
                                <div v-if="!$store.state.profile_pic_background_img"
                                    @click="openFileInput"
                                    class="my-account-upload-pfp">
                                    <div class="my-account-pfp-placeholder">
                                        {{ $t('myaccountview.uploadpfp') }}
                                        <i class="fas fa-camera"></i>
                                    </div>
                                </div>
                                <div v-else
                                    @click="openFileInput"
                                    class="my-account-upload-pfp" 
                                    :style="{ backgroundImage: `url(${$store.state.profile_pic_background_img})` }">
                                </div>
                            </div>
                            <!-- general errors -->
                            <div v-if="errors.generalErrors.length">
                                <p class="my-errors" style="color:red" v-for="error in errors.generalErrors" v-bind:key="error">
                                <span style="color:red !important">*</span> {{ error }}
                                </p>                        
                            </div>
                            <!-- username errors-->
                            <div v-if="errors.usernameErrors.length">
                                <p class="my-errors" style="color:red" v-for="error in errors.usernameErrors" v-bind:key="error">
                                <span style="color:red !important">*</span> {{ error }}
                                </p>
                            </div>
                            <!-- real-time username validation -->
                            <p class="my-errors" style="color:red" v-if="!usernameAvailable && !isUsernameEmpty ">{{ $t('loginsignupview.usernamenotavail') }}</p>
                            <p class="my-errors" style="color:green" v-else-if="usernameAvailable && !isUsernameEmpty ">{{ $t('loginsignupview.usernameavail') }}</p>
                            <!-- username -->
                            <label class="my-label" for="">{{ $t('loginsignupview.usernameonly') }}</label>
                            <div class="control">
                                <!-- v-model connects the data var defined below -->
                                <input type="text" v-model="username" name="username" @input="checkUsername" class="input" :placeholder="$t('loginsignupview.usernameonly')">
                            </div>
                            <!-- email errors-->
                            <div v-if="errors.emailErrors.length">
                                <p class="my-errors" style="color:red" v-for="error in errors.emailErrors" v-bind:key="error">
                                <span style="color:red !important">*</span> {{ error }}
                                </p>
                            </div>
                            <!-- real-time email validation -->
                            <p class="my-errors" style="color:red" v-if="!emailAvailable && !isEmailEmpty">{{ $t('loginsignupview.emailnotavail') }}</p>
                            <p class="my-errors" style="color:green" v-else-if="emailAvailable && !isEmailEmpty">{{ $t('loginsignupview.emailavail') }}</p>
                            <!-- email -->
                            <label class="my-label" for="">{{ $t('loginsignupview.emailonly') }}</label>
                            <div class="control">
                                <input type="text" v-model="email" name="email" @input="checkEmail" class="input" :placeholder="$t('loginsignupview.emailonly')">
                            </div>
                            <!-- not required fields -->
                            <!-- first_name -->
                            <label class="my-label" for="">{{ $t('loginsignupview.firstnamelabel') }}</label>
                            <div class="control">
                                <input type="text" class="input" :placeholder="$t('loginsignupview.firstnamelabel')" v-model="first_name">
                            </div>
                            <!-- lastname -->
                            <label class="my-label" for="">{{ $t('loginsignupview.lastnamelabel') }}</label>
                            <div class="control">
                                <input type="text" class="input" :placeholder="$t('loginsignupview.lastnameplaceholder')" v-model="last_name">
                            </div>
                            <!-- fav color -->
                            <label class="my-label" for="">{{ $t('loginsignupview.favoritecolor') }}</label>
                            <div class="control">
                                <input type="text" class="input" :placeholder="$t('loginsignupview.favoritecolorplaceholder')" v-model="favorite_color">
                            </div>
                            <!-- password errors-->
                            <div v-if="errors.passwordErrors.length">
                                <p class="my-errors" style="color:red" v-for="error in errors.passwordErrors" v-bind:key="error">
                                <span style="color:red !important">*</span> {{ error }}
                                </p>                        
                            </div>
                            <!-- password use click.prevent to prevent form submission action -->
                            <label class="my-label" for="">{{ $t('loginsignupview.password') }}</label>
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
                            <!-- re-enter password errors-->
                            <div class="my-errors" v-if="errors.re_enter_passwordErrors.length">
                                <p style="color:red" v-for="error in errors.re_enter_passwordErrors" v-bind:key="error">
                                <span style="color:red !important">*</span> {{ error }}
                                </p>                           
                            </div>
                            <!--re-enter password use click.prevent to prevent form submission action -->
                            <label class="my-label" for="">{{ $t('loginsignupview.reenterpassword') }}</label>
                            <div class="field has-addons my-password-field">
                                <div class="control is-expanded input-container">
                                    <!-- show password, type has to be text -->
                                    <input v-if="showReEnterPassword" type="text" class="input" v-model="re_enter_password" />
                                    <!-- hide password, type is password -->
                                    <input v-else type="password" class="input" v-model="re_enter_password">
                                    <span @click.prevent="toggleShowReEnterPassword" class="icon is-small is-right my-eye-icon">
                                        <i class="fas" :class="{ 'fa-eye-slash': showReEnterPassword, 'fa-eye': !showReEnterPassword }"></i>
                                    </span>
                                </div>
                            </div> 
                            <!-- submit form -->
                            <div class="field">
                                <div class="control">
                                    <button :class="['button login-signup-button', { 'login-signup-button-disabled': submitButtonDisabled }]">
                                        <span v-if="submitButtonDisabled" class="spinner-border spinner-border-sm text-small" role="status" aria-hidden="true"></span>
                                        {{ $t('loginsignupview.createaccountbutton') }}
                                    </button>
                                </div>
                            </div>
                            <p v-if="$store.state.language === 'en'" class="signup-login-reroute">
                                {{ $t('loginsignupview.login1') }} <a style="color:aqua !important; text-decoration:underline;" href="/login">{{ $t('loginsignupview.login2') }}</a>
                            </p>
                            <p v-else-if="$store.state.language === 'ja'" >
                                <a class="signup-login-reroute" style="text-decoration:underline;" href="/login">{{ $t('loginsignupview.login1') }}</a>
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
    name: 'SignUp',

    data() {
        return {
            timer: '',
            timerRunning: '',
            // 1 second
            api_post_wait_duration: 400,
            username: '',
            usernameAvailable: true,
            email: '',
            emailAvailable: true,
            first_name: '',
            last_name: '',
            password: '',
            re_enter_password: '',
            favorite_color: '',
            errors: {
                generalErrors: [],
                usernameErrors: [],
                emailErrors: [],
                passwordErrors: [],
                re_enter_passwordErrors: [],
            },
            showPassword: false,
            showReEnterPassword: false,
            profile_pic_file: null,
            submitButtonDisabled: false

        };
    },

    mounted () {
        document.title = 'Signup';

    },

    computed: {

        isUsernameEmpty() {
            return this.username.trim().length === 0;
        },

        isEmailEmpty() {
            return this.email.trim().length === 0;
        },
    },
    methods: {

        // set profile pic and resize it for backend
        handleFileUpload(event) {

            // check MIME type
            const allowedImageTypes = ['image/jpeg', 'image/png', 'image/gif']; // List of allowed image MIME types

            const file = event.target.files[0];

            if (!allowedImageTypes.includes(file.type)) {
                this.errors.generalErrors.push(this.$t('loginsignupview.invalidimagefile'))
                return
            }

            this.errors.generalErrors = []

            if (file.size <= 2621440) {
                const imgURL = URL.createObjectURL(file);
                this.$store.state.profile_pic_background_img = imgURL;
                this.profile_pic_file = file
                return
            }

            const reader = new FileReader();
            reader.onload = (e) => {
                const imageDataUrl = e.target.result;

                // Create an image element
                const img = new Image();
                img.src = imageDataUrl;

                // Once the image is loaded, resize it using a canvas
                img.onload = () => {
                    const canvas = document.createElement('canvas');
                    const ctx = canvas.getContext('2d');

                    // Calculate the new dimensions based on the desired file size
                    const maxSize = 2621440; // 2.5 MB
                    const scaleFactor = Math.sqrt(maxSize / (img.width * img.height));
                    const newWidth = Math.floor(img.width * scaleFactor);
                    const newHeight = Math.floor(img.height * scaleFactor);

                    // Set the canvas size to the new dimensions
                    canvas.width = newWidth;
                    canvas.height = newHeight;

                    // Draw the image onto the canvas with the new dimensions
                    ctx.drawImage(img, 0, 0, newWidth, newHeight);

                    // Convert the canvas content to a Blob object
                    canvas.toBlob((blob) => {
                        // Access the size property of the Blob object to get the new file size

                        // Log the new file size
                        
                        // Set the resized image data URL as the background image of the div
                        const resizedImageDataUrl = URL.createObjectURL(blob);
                        this.$store.state.profile_pic_background_img = resizedImageDataUrl;

                        const resizedFile = new File([blob], file.name);
                        this.profile_pic_file = resizedFile;

                    }, file.type);

                };
            };
        reader.readAsDataURL(file);
            this.formEnabled = true;
        },


        // trigger filechooser without ugly default HTML filechooser button
        openFileInput() {
            this.$refs.fileInput.click();
        },

        // dynamically check username validity
        checkUsername() {
            // clear the timeout if it is still running
            if (this.timer) {
                clearTimeout(this.timer);
                this.timerRunning = false;
            }
            if (this.username.trim().length > 0) {
                this.timer = setTimeout(() => {
                    this.timerRunning = true;
                    try {
                        axios.get(process.env.VUE_APP_CHECK_USERNAME_API_URL + `${this.username}`,
                        {
                        headers: {
                            'api-key': process.env.VUE_APP_API_KEY
                        }
                        }).then(response => {
                            const data = response.data;
                            this.usernameAvailable = data.available;
                            this.timerRunning = false;
                        })
                        .catch(error => {
                        })
                    }
                    catch(error) {
                        }   
                }, this.api_post_wait_duration)
            }
        } ,

        checkEmail() {
            // clear the timeout if it is still running
            if (this.timer) {
                clearTimeout(this.timer);
            }
            if (this.email.trim().length > 0) {
                this.timer = setTimeout(() => {
                    try {
                        axios.get(process.env.VUE_APP_CHECK_EMAIL_API_URL + `${this.email}`,
                        {
                        headers: {
                            'api-key': process.env.VUE_APP_API_KEY
                        }
                        }).then(response => {
                            const data = response.data;
                            this.emailAvailable = data.available;
                        })
                        .catch(error => {
                        })
                    }
                    catch(error) {
                        }   
                }, this.api_post_wait_duration)
            }
        },

        submitForm() {
            // reset errors
            this.errors.generalErrors = []
            this.errors.usernameErrors = []
            this.errors.emailErrors = []
            this.errors.passwordErrors = []
            this.errors.re_enter_passwordErrors = []


            // client side validation
            // USERNAME
            // if username is empty
            if (this.username === '') {
                this.submitButtonDisabled = false;
                this.errors.usernameErrors.push(this.$t('loginsignupview.usernamereq'))
            }

            // EMAIL
            if (this.email === '') {
                this.submitButtonDisabled = false;
                this.errors.emailErrors.push(this.$t('loginsignupview.emailreq'))
            }
            // check if email has @ symbol
            if (!this.email.includes('@')) {
                this.submitButtonDisabled = false;
                this.errors.emailErrors.push(this.$t('loginsignupview.email@symbolerror'))

            }

            // PASSWORD
            if (this.password === '') {
                this.submitButtonDisabled = false;
                this.errors.passwordErrors.push(this.$t('loginsignupview.noemptypass'))
            }

            // RE-ENTER PASSWORD
            if (this.re_enter_password === '') {
                this.submitButtonDisabled = false;
                this.errors.re_enter_passwordErrors.push(this.$t('loginsignupview.blankreenterpassword'))
            }

            // if passwords don't match
            if (this.password !== this.re_enter_password) {
                this.submitButtonDisabled = false;
                this.errors.passwordErrors.push(this.$t('loginsignupview.passwordsdontmatch'))
            }
            // if password is similiar to username
            if (this.username.includes(this.password) && this.re_enter_password !== '') {
                this.submitButtonDisabled = false;
                this.errors.passwordErrors.push(this.$t('loginsignupview.passwordtoosimilartousername'))
            }
            // if password is similiar to username
            if (this.email.includes(this.password) && this.re_enter_password !== '') {
                this.submitButtonDisabled = false;
                this.errors.passwordErrors.push(this.$t('loginsignupview.passwordtoosimilartoemail'))
            }



            // if no errors, submit the form and authenticate user
            if (!this.errors.usernameErrors.length && !this.errors.emailErrors.length && !this.errors.passwordErrors.length && !this.errors.re_enter_passwordErrors.length) {


                // disable login button
                this.submitButtonDisabled = true

                // var to hold post data
                // keys must be same strings as model fields in backend api
                // values can be named whatever
                const signUpFormData = {
                    email: this.email,
                    username: this.username,
                    password: this.password,
                    first_name: this.first_name,
                    last_name: this.last_name,
                    profile_pic: this.profile_pic_file,
                    favorite_color: this.favorite_color,
                }

                // send post data to backend server
                axios
                    .post(process.env.VUE_APP_CUSTOM_CREATE_USER, signUpFormData,
                    
                     // header needed to send text and file data
                     {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                    }
                    }).then(response => {
                        // add toast message
                        toast({
                            message: this.$t('modals.accountcreated'),
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 2000,
                            position: 'center',
                            animate: { in: 'fadeIn', out: 'fadeOut' },
                        })
                        this.$router.push('/login')
                    })
                    // catch the error data, strip it down to category, and push
                    // each error to the appropraite error array
                    
                    .catch(error => {
                        this.submitButtonDisabled = false;

                        if (error.response) {
                            for (const property in error.response.data) {
                                // disabled server side password validation
                                // if (property === 'password') {
                                //     this.errors.passwordErrors.push(`${error.response.data[property]}`)
                                // }
                                
                                // check if username is already taken
                                if (property === 'username') {
                                    this.errors.usernameErrors.push(this.$t('loginsignupview.usernameexistserror'))
                                }
                                // check if username is already taken
                                if (property === 'email') {
                                    this.errors.emailErrors.push(this.$t('loginsignupview.emailexistserror'))
                                }
                            }

                        } else if (error.message) {
                            this.errors.generalErrors.push(this.$t('loginsignupview.generror'))
                        }
                    })
            }
            else {
            }

        },
        toggleShowPassword() {
            this.showPassword = !this.showPassword;
        },
        toggleShowReEnterPassword() {
            this.showReEnterPassword = !this.showReEnterPassword;
        },
    }
}
</script>