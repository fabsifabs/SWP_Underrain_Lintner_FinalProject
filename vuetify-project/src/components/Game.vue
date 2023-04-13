<template>
    <h2 style="margin-left: 1cm;">Game</h2>
    <h3 style="margin-left:1cm">Winning Streak: {{ streak }}</h3>
    <v-container :style="myStyle" v-cloak>
        <v-responsive class="d-flex align-center text-center fill-height">
          <v-row class="d-flex align-center justify-center" style="margin-bottom: 1cm; margin-top: 1cm;">
            <v-col>
                <v-select  v-model="difficulty" label="difficulty" :items="difficulties"/>
            </v-col>
            <v-col>
                <v-select  v-model="category" label="category" :items="categories"/>
            </v-col>    
          </v-row>
          <v-row class="d-flex align-center justify-center" style="margin-bottom: 20px;">
            <v-chip>{{ result["question"] }}</v-chip>
          </v-row>
          <v-row>
            <v-col>
                <v-btn :disabled="isDisabled" id="0" @click = "checkAnswer(0)">{{ result["answers"][0] }}</v-btn>
            </v-col>
            <v-col>
                <v-btn :disabled="isDisabled" id="1" @click = "checkAnswer(1)">{{ result["answers"][1] }}</v-btn>
            </v-col>
          </v-row>
          <v-row style="margin-bottom:1cm;">
            <v-col>
                <v-btn :disabled="isDisabled" id="2" @click = "checkAnswer(2)">{{ result["answers"][2] }}</v-btn>
            </v-col>
            <v-col>
                <v-btn :disabled="isDisabled" id="3" @click = "checkAnswer(3)">{{ result["answers"][3] }}</v-btn>
            </v-col>
          </v-row>
          <v-row class="d-flex align-center justify-center" style="margin-bottom: 20px;">
            <v-btn id="nextBtn" @click="newQuestion()" :class="{'d-none': !showNext}">next Question</v-btn>
          </v-row>
        </v-responsive>
      </v-container>
</template>

<script>
import axios from 'axios';
    export default{
        data(){
            return {
                result: {
                            "answers": [],
                            "id": "",
                            "question": ""
                            },
                difficulty: "easy",
                category: "arts",
                confirm : "",
                myStyle:{
                    backgroundColor:""
                },
                difficulties: ['easy', 'medium', 'hard'],
                categories: ['arts', 'movies', 'food', 'general_knowledge', 'geography', 'history', 'music', 'science', 'culture', 'sport'],
                streak: 0,
                showNext: false,
                isDisabled: false
                
            }
        },
        methods:
        {
            async getQuestion(){
                await axios.get(`http://127.0.0.1:5000/getQuestion/${this.difficulty}/${this.category}`)
                .then(result => this.result = result.data);
            },
            async checkAnswer(num){
                await axios.get(`http://127.0.0.1:5000/getCorrect/${this.result.id}`)
                .then(result => this.confirm = result.data);
                let isCorrect = false
                console.log(this.confirm)
                if (this.confirm === this.result.answers.at(num)){
                    isCorrect = true
                    
                }else{
                    if (sessionStorage.username != null){
                        await axios.put(`http://127.0.0.1:5000/userManagement/updateHighscore`,
                    {
                        params:{
                            username: sessionStorage.getItem("username"),
                            highscore: this.streak
                        }
                    });
                    }  
                }
                
                let button = document.getElementById(num);
            
                if (isCorrect==true){
                    button.style.backgroundColor = "#00ba57";
                    this.streak++ 
                }else{
                    button = document.getElementById(num);
                    button.style.backgroundColor='red';
                    button = document.getElementById(this.result.answers.findIndex(element => element === this.confirm));
                    button.style.backgroundColor = "#00ba57";
                    this.streak = 0;
                }
                this.isDisabled = true
                this.showNext = true
                
            },
            newQuestion(){
                this.resetBtns()
                this.getQuestion()
            },
            resetBtns(){
                this.showNext = false
                this.isDisabled = false
                let button
                for (let i = 0;i<4;i++){
                    button = document.getElementById(i)
                    button.style.backgroundColor = "white";
                    
                }
            }

        },
        watch:{
            difficulty: function (){
                this.getQuestion()
                this.resetBtns()
            },
            category: function (){
                this.getQuestion()
                this.resetBtns()
            }
        },
        created(){
            this.getQuestion()
        }
    }
</script>