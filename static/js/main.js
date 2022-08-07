const player = document.getElementById('videoElement');
if (flvjs.isSupported()) {
    const flvPlayer = flvjs.createPlayer({
        type: 'flv',
        isLive: true,
        hasAudio: true,
        hasVideo: true,
        enableWorker: true,
        enableStashBuffer: false,
        stashInitialSize: 128,
        url: 'ws://trou.ltd:1936/live/live.flv',
    });
    flvPlayer.attachMediaElement(videoElement);
    flvPlayer.load();
    player.play();
}


new Vue({
    el: '#app',
    delimiters: ["<%", "%>"],
    data() {
        return {
            online_users: [],
            comments: [],
            comment_value: ""
        };
    },
    created() {
        this.loadData()
        setInterval(() => {
          this.loadData()
        },5000);
    },
    methods: {
        loadData() {
            this.$axios.get(`http://trou.ltd:8000/status`, {
            }).then(res => {
                this.comments = res.data.msgs
                this.online_users = res.data.online_users
            });
        },

        sendData() {
            this.$axios.get(`http://trou.ltd:8000/comment`, {
                params: {
                    msg: this.comment_value
                }
            }).then(res => {
                this.comment_value = ""
                this.loadData()
            });
        }
    }
});
