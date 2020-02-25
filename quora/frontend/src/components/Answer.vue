<template>
    <div>
        <p class="text-muted">
            <strong>{{ answer.author }}</strong> &#8901; {{ answer.created_at }}
        </p>
        <p>{{ answer.content }}</p>
        <div v-if="isAnswerAuthor">
            <router-link
                :to="{name: 'Answer-editor', params: {id: answer.id}}"
                class="btn btn-sm btn-outline-secondary mr-3">Edit</router-link>
            <button
                class="btn btn-sm btn-outline-danger"
                @click="triggerDeleteAnswer"
            >
                Delete
            </button>
        </div>
        <div v-else>
            <button
                class="btn btn-sm"
                @click="toggleLike"
                :class="{
                    'btn-danger': user_liked_answer,
                    'btn-outline-danger': !user_liked_answer
                }">
                <strong>Like [{{likes_counter}}]</strong>
            </button>
        </div>
        <hr />
    </div>
</template>

<script>
    import {apiService} from "../common/api.service";

    export default {
        name: "AnswerComponent",
        props: {
            answer: {
                type: Object,
                required: true
            },
            request_user: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                user_liked_answer: this.answer.user_has_voted,
                likes_counter: this.answer.likes_count
            }
        },
        methods: {
            toggleLike() {
                this.user_liked_answer === false
                    ? this.likeAnswer()
                    : this.unlikeAnswer();
            },
            likeAnswer() {
                this.user_liked_answer = true;
                this.likes_counter += 1;
                let endpoint = `/api/answers/${this.answer.id}/like/`;
                apiService(endpoint, 'POST');
            },
            unlikeAnswer() {
                this.user_liked_answer = false;
                this.likes_counter -= 1;
                let endpoint = `/api/answers/${this.answer.id}/like/`;
                apiService(endpoint, 'DELETE');

            },
            triggerDeleteAnswer() {
                this.$emit('delete-answer', this.answer);
            }
        },
        computed: {
            isAnswerAuthor() {
                return this.answer.author === this.request_user;
            }
        }
    };
</script>

<style scoped>

</style>
