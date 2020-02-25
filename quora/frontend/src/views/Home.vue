<template>
    <div class="home">
        <div class="container mt-5">
            <div v-for="question in questions" :key="question.pk">
                <p class="mb-0">Posted by:
                    <span class="author_name_in_question_list">{{ question.author }}</span>
                </p>
                <router-link
                    :to="{ name: 'Question', params: { slug: question.slug } }"
                    class="question-link"
                > {{ question.content }} </router-link>
                <p>Answers: {{ question.answers_count }}</p>
                <hr>
            </div>
            <div class="my-4">
                <p v-show="loading_questions">...</p>
                <button
                    v-show="next"
                    @click="getQuestions"
                    class="btn btn-sm btn-outline-success"
                >
                    Load more
                </button>
            </div>
        </div>
    </div>
</template>

<script>
    import { apiService } from "../common/api.service";

    export default {
        name: "Home",
        data() {
            return {
                questions: [],
                next: null,
                loading_questions: false
            };
        },
        methods: {
            getQuestions() {
                let endpoint = 'api/questions/';
                if (this.next){
                    endpoint = this.next;
                }
                this.loading_questions = true;
                apiService(endpoint).then(data => {
                    this.questions.push(...data.results);
                    this.loading_questions = false;
                    if (data.next){
                        this.next = data.next;
                    } else {
                        this.next = null;
                    }
                });
            }
        },
        created() {
            this.getQuestions();
            document.title = 'Quora';
        }
    };
</script>
<style scoped>
    .author_name_in_question_list {
        font-weight: bold;
        color: red;
    }

    .question-link {
        font-weight: bold;
        color: black;
    }
    .question-link:hover {
        text-decoration: none;
        color: #343A40;
    }
</style>
