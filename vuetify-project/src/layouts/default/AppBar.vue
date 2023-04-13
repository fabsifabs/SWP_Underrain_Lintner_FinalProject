<template>
  <v-app-bar flat>
    <v-app-bar-title>
      <div>
        <v-menu>
          <template v-slot:activator="{ props }">
            <v-btn
              color="primary"
              v-bind="props"
            >
              Menu
            </v-btn>
          </template>
          <v-list>
            <v-list-item
              v-for="(item, index) in items"
              :key="index"
              :value="index"
            >
              <v-list-item-title @click ="changeV(item)" >{{ item }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </div>
    </v-app-bar-title>
    <div v-if="username != ''" >
      <v-btn @click="logout()">
        logout
      </v-btn>
    </div>
  </v-app-bar>
  
</template>

<script>
import {reactive} from 'vue'
  export default{
    data(){
      return{
        items : {home:"Home",game:"Game", leaderboard:"Leaderboard"},
        username: "",
        intervalUser: null
      }
    },
    methods:{
      changeV(route){
        console.log(route)
        if (route==="Home"){
          window.location= "/"
        }else{
          window.location= `/${String(route)}`
        }
      },
      logout(){
        sessionStorage.username = ''
      }
    },
    created(){
      document.title = "QuizShow"
      this.intervalUser = setInterval(() => {
        this.username = sessionStorage.username
       
      }, 1000) 
    },
    beforeUnmount(){
      clearInterval(this.intervalUser)
    }
  }
</script>
