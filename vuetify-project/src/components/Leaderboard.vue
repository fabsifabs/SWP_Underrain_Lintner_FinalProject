<template>
    <v-container class="fill-height">
        <v-responsive class="d-flex align-center text-center fill-height">
          <v-row class="d-flex align-center justify-center">
            <v-table>
              <thead>
                <tr>
                  <th class="text-left">
                    Rank
                  </th>
                  <th class="text-left">
                    Username
                  </th>
                  <th class="text-left">
                    Score
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in board"
                  :key="item.username"
                >
                  <td>{{ board.indexOf(item)+1 }}</td>
                  <td>{{ item.username }}</td>
                  <td>{{ item.highscore }}</td>
                </tr>
              </tbody>
            </v-table>
          </v-row>
        </v-responsive>
      </v-container>
</template>

<script>
import axios from 'axios'
export default{
  data(){
    return{
      board:{},
      headers:[
        {title:'username',key:'username'},
        {title:'score',key:'highscore'},
      ]
    }
  },
  methods:{
    async updateLeaderboard(){
      let result = await axios.get(`http://127.0.0.1:5000/userManagement/leaderboard`)
      this.board = result.data
    }
  },
  created(){
    this.updateLeaderboard()
  }
}
</script>