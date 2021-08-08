<template>
    <span>
    <v-card
    v-if="words.length > 0"
    class="mx-auto"
    max-width="344"
    style="height: 100%;"
    >
        <v-card-title>{{word.word}}</v-card-title>
        <v-card-subtitle>{{word.pronunciation}}</v-card-subtitle>
        <v-card-text class='multiline'>{{word.hint}}</v-card-text>
        <v-card-actions class="v-card-actions">
            <v-btn
            text
            color="teal accent-4"
            @click="reveal = true"
            >
            Learn More
            </v-btn>
            <v-spacer></v-spacer>
            <v-icon class="mr2" color="teal accent-4" @click="goBack">mdi-chevron-left</v-icon>
            <v-icon class="mr2" color="teal accent-4" @click="goNext">mdi-chevron-right</v-icon>
            <v-icon class="mr2" color="teal accent-4" @click="goToCourses">mdi-exit-to-app</v-icon>
        </v-card-actions>

        <v-expand-transition>
            <v-card
            v-if="reveal"
            class="transition-fast-in-fast-out v-card--reveal mx-auto"
            >
                <v-card-title>{{word.word}}</v-card-title>
                <v-card-subtitle>{{word.pronunciation}}</v-card-subtitle>
                <v-card-text class='multiline'>{{word.description}}</v-card-text>
                <v-card-actions class="v-card-actions pt-0">
                    <v-btn
                    text
                    color="teal accent-4"
                    @click="reveal = false"
                    >
                    Close
                    </v-btn>
                    <v-spacer></v-spacer>
                    <v-icon class="mr2" color="teal accent-4">mdi-chevron-left</v-icon>
                    <v-icon class="mr2" color="teal accent-4">mdi-chevron-right</v-icon>
                </v-card-actions>
            </v-card>
        </v-expand-transition>
    </v-card>

    <v-card
    v-if="words.length == 0"
    class="mx-auto"
    max-width="344"
    style="height: 100%;"
    >
        <v-card-title>no words</v-card-title>
        <v-card-actions class="v-card-actions">
            <v-spacer></v-spacer>
            <v-icon class="mr2" color="teal accent-4" @click="goToCourses">mdi-exit-to-app</v-icon>
        </v-card-actions>

    </v-card>
    </span>


</template>

<script>
export default {
    name: "PracticeComponent",
    middleware: 'auth',
    data() {
        return {
            words: [],
            word: {
                word: '',
                description: '',
                pronunciation: '',
                hint: '',
            },
            wordIndex: 0,
            courseId: this.$route.params.course_id,
            loading: true,
            reveal: false,
        };
    },
    computed: {
    },
    watch: {
        deep: true,
    },
    mounted() {
        this.readDataFromAPI();
    },
    methods: {
        readDataFromAPI() {
            this.loading = true;
            this.$axios.get(
                `/courses/${this.courseId}/words/practice/`,
                {
                    params:{
                    }
                }
            ).then((response) => {
                this.loading = false;
                this.words = response.data;
                this.updateCard();
            });
        },
        updateCard() {
            Object.assign(this.word, this.words[this.wordIndex]);
        },
        goBack() {
            if(this.wordIndex > 0){
                this.wordIndex--;
                this.updateCard();
            }
        },
        goNext() {
            if(this.wordIndex < this.words.length){
                this.wordIndex++;
                this.updateCard();
            }
        },
        goToCourses (){
            this.$router.go(-1);
        },
    },
};
</script>

<style>
.v-card--reveal {
    top: 0;
    opacity: 1 !important;
    position: absolute;
    width: 100%;
}
.multiline {
    white-space: pre;
}
</style>
