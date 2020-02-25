<template>
    <div class="single-question mt-2">
        <div v-if="question" class="container">
            <h1>{{ question.content }}</h1>
            <QuestionActions v-if="isQuestionAuthor" :slug="question.slug" />
            <p class="mb-0">
                Posted by:
                <span class="author_name_in_question">{{question.author }}</span>
            </p>
            <p>Created: {{question.created_at}}</p>
            <hr />
            <div v-if="user_has_answered">
                <p class="answer_added">You have already answered that question</p>
            </div>
            <div v-else-if="show_form">
                <form class="card" @submit.prevent="onSubmit">
                    <div class="card-header px-3">Answer the question</div>
                    <div class="card-block">
                        <textarea
                            v-model="answer_to_submit"
                            class="form-control"
                            placeholder="Share your knowledge"
                            rows="3"
                        ></textarea>
                    </div>
                    <div class="card-footer px-3">
                        <button type="submit" class="btn btn-sm btn-success">
                            Submit</button>
                    </div>
                </form>
                <p v-if="answer_error" class="error mt-2">{{ answer_error }}</p>
            </div>
            <div v-else>
                <button
                    class="btn btn-sm btn-success"
                    @click="show_form = true"
                >Add answer</button>
            </div>
            <hr />
        </div>
        <div v-else class="container">
            <h1>404 - Page Not Found</h1>
        </div>
        <div v-if="question" class="container">
            <AnswerComponent
                v-for="answer in answers"
                :key="answer.id"
                :answer="answer"
                :request_user="request_user"
                @delete-answer="deleteAnswer"
            />
            <div class="my-4">
                <p v-show="loading_answers">...</p>
                <button
                    v-show="next"
                    @click="getQuestionAnswers"
                    class="btn btn-sm btn-outline-success"
                >
                    Load more
                </button>
            </div>
        </div>
    </div>
</template>

<script>
    import QuestionActions from "../components/QuestionActions";
    import { apiService } from '@/common/api.service';
    import AnswerComponent from '@/components/Answer.vue';

    export default {
        name: 'Question',
        props: {
            slug: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                question: {},
                answers: [],
                answer_to_submit: null,
                answer_error: null,
                user_has_answered: false,
                show_form: false,
                next: null,
                loading_answers: false,
                request_user: null
            };
        },
        components: {
            QuestionActions,
            AnswerComponent
        },
        computed: {
            isQuestionAuthor() {
                return this.question.author === this.request_user;
            }
        },
        methods: {
            setRequestUser() {
                this.request_user = window.localStorage.getItem('username');
            },
            onSubmit() {
                if (this.answer_to_submit) {
                    let endpoint = `/api/questions/${this.slug}/answer/`;
                    apiService(endpoint, 'POST', {
                        content: this.answer_to_submit
                    }).then(data => {
                        this.answers.unshift(data);
                    });
                    this.answer_to_submit = null;
                    this.show_form = false;
                    this.user_has_answered = true;
                    if (this.answer_error) {
                        this.answer_error = null;
                    }
                } else {
                    this.answer_error = 'Answer is empty!';
                }
            },
            getQuestionAnswers() {
                let endpoint = `/api/questions/${this.slug}/answers/`;
                if (this.next) {
                    endpoint = this.next;
                }
                this.loading_answers = true;
                apiService(endpoint).then(data => {
                    this.answers.push(...data.results);
                    this.loading_answers = false;
                    if (data.next) {
                        this.next = data.next;
                    } else {
                        this.next = null;
                    }
                });
            },
            setPageTitle(title) {
                document.title = title;
            },
            async deleteAnswer(answer) {
                let endpoint = `/api/answers/${answer.id}/`;
                try {
                    await apiService(endpoint, 'DELETE');
                    this.$delete(this.answers, this.answers.indexOf(answer));
                    this.user_has_answered = false;
                } catch (err) {
                    console.log(err);
                }
            },
            getQuestionData() {
                let endpoint = `/api/questions/${this.slug}/`;
                apiService(endpoint).then(data => {
                    if (data) {
                        this.question = data;
                        this.user_has_answered = data.user_has_answered;
                        this.setPageTitle(data.content);
                    } else {
                        this.question = null;
                        this.setPageTitle('404 - not found');
                    }
                });
            }
        },
        created() {
            this.getQuestionData();
            this.getQuestionAnswers();
            this.setRequestUser();
        }
    };
</script>

<style scoped>
    .author_name_in_question {
        font-weight: bold;
        color: red;
    }
    .answer_added {
        font-weight: bold;
        color: green;
    }
    .error {
        font-weight: bold;
        color: red;
    }
</style>
