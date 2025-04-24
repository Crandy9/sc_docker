<template>
  <!-- homepage pic -->
  <section class="banner-section">
    <div class="home">
      <div class="has-text-centered">
        <figure>
          <img class="sheriff-crandy-img" src="@/assets/images/piano.jpg" alt="">
        </figure>
      </div>
      <div class="scripture-banner has-text-centered">
        <h4 class="subtitle my-scripture-sub">
          "{{$t('homeview.body.scripture')}}"
          <p style="font-size:medium"><cite>{{$t('homeview.body.chaptverse')}}</cite></p>
        </h4>
      </div>
    </div>
  </section>


  <!-- youtube video section -->
  <section class="latest-yt-songs-section">
      <h3 id="yt-section-title" class="is-size-3 has-text-centered has-text-white" >
        <u>{{$t('homeview.body.latestSongs')}}</u>
      </h3>
      <div class="yt-player">
        <h3 id="yt-section-title" class="is-size-4 has-text-centered has-text-white" >
          "Praise Him"
        </h3>
        <iframe
          class="yt-iframe"
          src="https://www.youtube.com/embed/KPkC9FKm4fM" 
          title="YouTube video player" 
          frameborder="0" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture;" allowfullscreen>
        </iframe>
        <h3 id="yt-section-title" class="is-size-4 has-text-centered has-text-white" >
          "The Firmament"
        </h3>
        <iframe
          class="yt-iframe"
          src="https://www.youtube.com/embed/vWmroU3Rg6c" 
          title="YouTube video player" 
          frameborder="0" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture;" allowfullscreen>
        </iframe>
        <h3 v-if="$i18n.locale === 'en'" class="is-size-4 has-text-white has-text-centered" style="padding-top: 3rem;">
          {{$t('homeview.body.purchaseNowMusicLink')}}<a class="music-links" href="/music"> {{$t('homeview.body.here')}}</a>
        </h3>
        <h3 v-else-if="$i18n.locale === 'ja'" class="is-size-4 has-text-white has-text-centered" style="padding-top: 3rem;">
          <a class="music-links" href="/music"> {{$t('homeview.body.here')}}</a>{{$t('homeview.body.purchaseNowMusicLink')}}
        </h3>
      </div>
  </section>
</template>

<script>

export default {
    name: 'Home',
    data() {
      return {
        
      }
    },
    mounted() {
      document.title = 'Sheriff Crandy Music' 
    },

    methods: {
      
    }

}
</script>