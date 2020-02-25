<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light my-navbar">
        <div class="container">
            <router-link :to="{ name: 'Home' }" class="navbar-brand"
                >Quora
            </router-link>

            <div class="collapse navbar-collapse">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item">
                        <router-link
                            :to="{ name: 'Home' }"
                            class="btn btn-sm btn-success"> Home
                        </router-link>
                    </li>
                    <li class="nav-item">
                        <router-link
                            :to="{ name: 'QuestionEditor' }"
                            class="btn btn-sm btn-danger"
                        >Ask question
                        </router-link>
                    </li>
                    <li class="nav-item">
                        <a class="btn btn-sm btn-outline-secondary"
                           href="/accounts/logout/"> Logout
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script>
    export default {
        name: 'NavbarComponent'
    };
</script>

<style scoped>
    .my-navbar {
        border-bottom: 1px solid gray;
    }

    .navbar-brand {
        font-weight: bold;
        font-size: 130%;
    }

    .navbar-brand:hover {
        color: red !important;
    }

    ul {
        list-style: none;
    }
</style>
