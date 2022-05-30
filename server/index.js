const express = require('express')
const app = express()
const cors = require('cors');
const { json } = require('express');
const axios = require('axios').default;
const fetch = require('node-fetch')

app.use(cors())
app.use(express.json())

app.get('/api/hello', async(req, res) => {
    console.log(req)
    try {
        console.log("Hello")
        res.send({ status: 'ok', body: "Hi"})
    } catch (err) {
        console.log(err)
    }
})




app.get('/api/flaskreq', async(req, res) => {
    console.log(req)
    var config = { headers: {  
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'}}
    try {
        // const res = await fetch('https://localhost:5000/time');
        // const json1 = await res.json();
        // console.log(json1)
        axios.get('https://localhost:5000/time', {
          config
          })
          .then(function (response) {
            // console.log(json(response));
            // res.send({ status: 'ok', body: json(response)});
            if(response.status == 200){
              console.log(response.data.message)
            }
          })
          .catch(function (error) {
            console.log(error);
          })
          .then(function () {
            // always executed
          });  
        


        
    } catch (err) {
        console.log(err)
    }
})

app.listen(1337, () => {
	console.log('Server started on 1337')
});
