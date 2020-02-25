<template>
    <div id="app">
        <NavbarComponent /> <router-view />
    </div>
</template>
<script>
    import NavbarComponent from './components/Navbar.vue';
    import { apiService } from '@/common/api.service';

    export default {
        name: 'App',
        methods: {
            async setUserInfo() {
                const data = await apiService('/api/profile/');
                const requestUser = data['username'];
                window.localStorage.setItem('username', requestUser);
            }
        },
        created() {
            this.setUserInfo();
        },
        components: {
            NavbarComponent
        }
    }
</script>
<style>
    .btn:focus {
        box-shadow: none !important;
    }

</style>
