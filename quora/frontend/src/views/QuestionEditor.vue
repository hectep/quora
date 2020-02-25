<template>
    <div class="container mt-2">
        <h1 class="mb-2">Ask a question</h1>
        <form @submit.prevent="onSubmit">
            <textarea
                v-model="question_body"
                rows="3"
                class="form-control"
                placeholder="Type your question here">
            </textarea>
            <br>
            <button type="submit" class="btn btn-success">publish</button>
        </form>
        <p v-if="error" class="muted mt-2">{{ error }}</p>
    </div>
</template>

<script>
    import { apiService } from "../common/api.service";

    export default {
        name: "QuestionEditor",
        props: {
            slug: {
                type: String,
                required: false
            }
        },
        data() {
            return {
                question_body: null,
                error: null
            };
        },
        methods: {
            onSubmit() {
                if (!this.question_body){
                    this.error = 'The question is empty';
                } else if (this.question_body.length > 240){
                    this.error = 'The question is longer than 240 chars';
                } else {
                    let endpoint = '/api/questions/';
                    let method = 'POST';
                    if (this.slug !== undefined) {
                        endpoint += `${this.slug}/`;
                        method = 'PUT';
                    }
                    apiService(endpoint, method, {
                        content: this.question_body
                    }).then(question_data => {
                        this.$router.push({
                            name: 'Question',
                            params: { slug: question_data.slug }
                        });
                    });
                }
            }
        },
        async beforeRouteEnter(to, from, next) {
            if (to.params.slug !== undefined) {
                let endpoint = `/api/questions/${to.params.slug}/`;
                let data = await apiService(endpoint);
                return next(vm => (vm.question_body = data.content));
            } else {
                return next();
            }
        },
        created() {
            document.title = 'Question editor';
        }
    };
</script>

<style scoped>

</style>
