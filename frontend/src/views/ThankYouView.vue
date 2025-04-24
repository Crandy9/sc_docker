<template>
    <section class="thankyou-section">
        <div class="thank-you-div">
            <div class="columns is-multiline">
                <div class="column is-12">
                    <h1 class="title">
                        {{ $t('thankyouview.title') }}
                    </h1>
                    <div class="thank-you-details" style="padding-inline: 2rem;">
                        <p class="has-text-white">
                            {{ $t('thankyouview.waitmsg') }}
                        </p>
                        <br>
                        <p class="has-text-white">
                            {{ $t('thankyouview.aboutdownload') }}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            isSingleTrack: false,
            isSingleFlp: false,
        }
    },
    methods: {

        initFileDownload() {

            try {
                console.log("this.$store.state.fileBlob in thankyou view")
                console.log(JSON.stringify(this.$store.state.fileBlob))

                const blob = window.URL.createObjectURL(this.$store.state.fileBlob);

                const link = document.createElement('a');
                link.href = blob

                if (this.$store.state.isSingleTrackDownload === true && this.$store.state.downloadType === 'singleTrackDownload') {
                    link.setAttribute('download', this.$store.state.downloadableItems[0].title + '.wav')
                }

                else if (this.$store.state.isSingleTrackDownload === true && this.$store.state.downloadType === 'singleFlpDownload') {
                    link.setAttribute('download', this.$store.state.downloadableItems[0].flp_name + '.zip')
                } 

                else {
                    link.setAttribute('download', 'SheriffCrandyDownloadables.zip')

                }

                document.body.appendChild(link)
                link.click();
                window.URL.revokeObjectURL(blob);

                this.$store.state.downloadableItems = []

            } 
            catch (error) {
                console.error('Error:', error);
            }
        },

        getFiles() {
            
            // single track download
            if (this.$store.state.downloadType === 'singleTrackDownload') {
                this.isSingleTrack = true;
                this.isSingleFlp = false;
                this.beginFileDownload(this.$store.state.downloadableItems[0].track, this.$store.state.downloadableItems[0].title)
            }

            // single flp download
            else if (this.$store.state.downloadType === 'singleFlpDownload') {
                this.isSingleTrack = false;
                this.isSingleFlp = true;
                this.beginFileDownload(this.$store.state.downloadableItems[0].flp_zip, this.$store.state.downloadableItems[0].flp_name)
            }

            // else it is a single cart download item
            // else {
            //     // check if this is a single track item being bought from the cart
            //     if (this.$store.state.downloadableItems.some(obj => obj.hasOwnProperty('track'))) {
            //         this.isSingleTrack = true;
            //         this.isSingleFlp = false;
            //         this.beginFileDownload(this.$store.state.downloadableItems[0].track, this.$store.state.downloadableItems[0].title)
            //     }
            //     else if (this.$store.state.downloadableItems.some(obj => obj.hasOwnProperty('flp_zip'))) {
            //         this.isSingleTrack = false;
            //         this.isSingleFlp = true;
            //         this.beginFileDownload(this.$store.state.downloadableItems[0].flp_zip, this.$store.state.downloadableItems[0].flp_name)
            //     }
            // }
            this.$store.state.downloadableItems = []
        },

        beginFileDownload(url, title) {
            axios({
                method: 'get',
                url,
                // responseType: 'arraybuffer',
                responseType: 'blob',
            }).then((response) =>{

                if (this.isSingleTrack === true) {

                    const blob = new Blob([response.data]);
                    const url = window.URL.createObjectURL(blob);
                    const link = document.createElement('a');
                    link.href = url;
                    link.setAttribute('download', title + '.wav');
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    // const url = window.URL.createObjectURL(new Blob([response.data]))
                    // const link = document.createElement('a')
                    // link.href= url
                    // link.setAttribute('download', title + '.wav')
                    // document.body.appendChild(link)
                    // link.click()
                }
                else if (this.isSingleFlp === true) {

                    const blob = new Blob([response.data]);
                    const url = window.URL.createObjectURL(blob);
                    const link = document.createElement('a');
                    link.href = url;
                    link.setAttribute('download', title + '.zip');
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);

                    // const url = window.URL.createObjectURL(new Blob([response.data]))
                    // const link = document.createElement('a')
                    // link.href= url
                    // link.setAttribute('download', title + '.zip')
                    // document.body.appendChild(link)
                    // link.click()
                }

            }).catch((error) => {

            })

        },

        // get new list of purchased tracks
        async getPurchasedTracks() {

            await axios.get(process.env.VUE_APP_GET_TRACK_ORDERS_URL, 
            { 
                headers: 
                    { 
                    'Authorization': `Token ${this.$store.state.sf_auth_bearer}`,
                    'api-key': process.env.VUE_APP_API_KEY
                    }
            }) .then(response => {
                if (response.data.length === 0) {
                }
                else {
                    this.$store.commit('populatePurchasedTrackArray', response.data)
                }
            })
            .catch( error => {
            })
        }

    },

    mounted () {
        document.title = "Thank you!";
        // this.initFileDownload();

        // single file downloads
        if (this.$store.state.downloadType === 'singleTrackDownload' || this.$store.state.downloadType === 'singleFlpDownload') {
            this.getFiles();
        }
        
        this.getPurchasedTracks();
    },
}
</script>