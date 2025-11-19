const express = require('express');
const mongoose = require('mongoose');

const app = express();

app.set('view engine', 'ejs');
app.use(express.urlencoded({ extended: false }));

// -------------------------------------
// MONGODB CONNECTION
// -------------------------------------
console.log('MongoDB url: ' + process.env.MONGO_HOST);

const host = process.env.MONGO_HOST;
const database = process.env.MONGO_DATABASE;
const mongoURL = `mongodb://${host}/${database}`;

console.log("Final MongoDB URL:", mongoURL);

// Track DB connection state for readiness probe
let dbConnected = false;

mongoose
  .connect(mongoURL, { useNewUrlParser: true })
  .then(() => {
    console.log('MongoDB Connected');
    dbConnected = true;
  })
  .catch(err => {
    console.log(err);
    dbConnected = false;
  });

const Item = require('./models/Item');

// -------------------------------------
// ROUTES
// -------------------------------------
app.get('/', (req, res) => {
  Item.find()
    .then(items => res.render('index', { items }))
    .catch(err => res.status(404).json({ msg: 'No items found' }));
});

// -------------------
// LIVENESS PROBE
// -------------------
app.get('/health', (req, res) => {
  res.status(200).json({ status: "UP", message: "I am super healthy" });
});

// -------------------
// READINESS PROBE
// -------------------
app.get('/ready', (req, res) => {
  if (dbConnected) {
    res.status(200).json({ status: "READY" });
  } else {
    res.status(500).json({ status: "NOT_READY" });
  }
});

// -------------------------------------
// START SERVER
// -------------------------------------
const port = process.env.APP_PORT || 3000;
app.listen(port, () => console.log(`Server running on port ${port}...`));
