const express = require('express');
const restful = require('node-restful');
const server = express();
const mongoose = restful.mongoose;
const bodyparser = require('body-parser');
const cors = require('cors');
const bodyParser = require('body-parser');

mongoose.Promise = global.Promise;
mongoose.connect('mongodb://db/mydb');

// Middlewares
server.use(bodyParser.urlencoded({
    extended: true
}));
server.use(bodyParser.json());
server.use(cors());

//ODM
const client = restful.model('Client', {
    name: {
        type: String,
        required: true
    }
});

// Rest API
client.methods(['get', 'post', 'put', 'delete']);
client.updateOptions({
    new: true,
    runValidators: true
});

//Routes
client.register(server, '/clients');

server.listen(3000);