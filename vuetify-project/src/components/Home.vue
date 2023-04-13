<template>
  <v-container>
      <v-row class="d-flex align-center text-center fill-height" style="margin-bottom: 1cm;"> 
        <v-col>
          <h1>Login/Register</h1>
        </v-col>
        <v-col>
          <h1>LeaderBorad</h1>
        </v-col>
      </v-row>
      <v-row class="d-flex align-center text-center fill-height">
        <v-col>
          <v-form ref="form">
            <v-text-field
              v-model="username"
              :counter= "10"
              :rules="usernameRules"
              label="Username"
              aria-required="requierd"
            ></v-text-field>
            <v-text-field
            type="password"
            v-model="password"
            :rules="passwordRules"
            
            label="Password"
            aria-required="requierd"
          ></v-text-field>
            <v-col>
              <v-btn @click="login()" color="success" block class="mt-2">Login</v-btn>
            </v-col>
            <v-col>
              <v-btn @click="register()" block class="mt-2">Register</v-btn>
            </v-col>
            
            
          </v-form>
        </v-col>
        <v-col>
          <v-table>
            <thead>
              <tr>
                <th class="text-left">
                  Username
                </th>
                <th class="text-left">
                  Highscore
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="item in boardTop"
                :key="item.username"
              >
                <td>{{ item.username }}</td>
                <td>{{ item.highscore }}</td>
              </tr>
            </tbody>
          </v-table>
        </v-col>
      </v-row>
      
  </v-container>
</template>
<script>

import axios from 'axios'


export default{
  data(){
    return{
      username:"",
      usernameRules:[
        v => !!v || 'Name is required',
        v => (v && v.length <= 10) || 'Name must be less than 10 characters',
      ],
      password:"",
      passwordRules:[
        v => !!v || 'Password is required',
        v => (v && v.length >= 10) || 'Name must be at least 10 characters',
      ],
      boardTop:{},
      board: {}
    }
  },
  methods:{
    async register(){
      let valid = await this.$refs.form.validate()
      if (valid.valid == true){
        let result =await axios.put(`http://127.0.0.1:5000/userManagement`,
        {
          params:{
          pwd:this.password,
          username: this.username
          }
        })
        if (result.data == true){
          this.login()
        }
      }
    },
    async login(){
      let valid = await this.$refs.form.validate()
      if (valid.valid == true){
        let result = await axios.put(`http://127.0.0.1:5000/userManagement/login`,
        {
          params:{
          pwd:this.password,
          username:this.username
          }
        })
        if (result.data == true){
          sessionStorage.setItem("username",String(this.username))
          console.log(sessionStorage)
          this.$refs.form.reset()
        }
      }
    },
    async updateLeaderboard(){
      let result = await axios.get(`http://127.0.0.1:5000/userManagement/leaderboard`)
      for (let i = 0; i<6;i++){
        this.boardTop[i] = result.data[i]
      }
    }
  },
  created(){
    this.updateLeaderboard()
  }
}
</script>
