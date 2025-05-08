
const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const bodyParser = require('body-parser');
const app = express();
const port = 3030;

app.use(cors());
app.use(bodyParser.urlencoded({ extended: false }));

// Read data from files
const reviews_data = JSON.parse(fs.readFileSync("reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("dealerships.json", 'utf8'));

// Connect to MongoDB
mongoose.connect("mongodb://mongo_db:27017/", { dbName: 'dealershipsDB' });

// Load Mongoose models
const Review = require('./review');
const Dealership = require('./dealership');

// Load data into MongoDB
(async () => {
  try {
    await Review.deleteMany({});
    await Dealership.deleteMany({});
    await Review.insertMany(reviews_data['reviews']);
    await Dealership.insertMany(dealerships_data['dealerships']);
    console.log("✅ Data loaded successfully.");
  } catch (error) {
    console.error("❌ Error loading data:", error.message);
  }
})();

// Routes
app.get('/', (req, res) => {
  res.send("Welcome to the Mongoose API");
});

// Fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const reviews = await Review.find();
    res.json(reviews);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching reviews' });
  }
});

// Fetch reviews by dealer ID
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const reviews = await Review.find({ dealership: parseInt(req.params.id) });
    res.json(reviews);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealer reviews' });
  }
});

// Fetch all dealerships
app.get("/fetchDealers", async (req, res) => {
  try {
    const dealers = await Dealership.find({});
    res.status(200).json(dealers);
  } catch (err) {
    console.error("Error in /fetchDealers:", err.message);
    res.status(500).json({ error: "Server error." });
  }
});

// Fetch dealerships by state
app.get("/fetchDealers/:state", async (req, res) => {
  try {
    const state = req.params.state;
    const dealers = await Dealership.find({ state: state });
    res.json(dealers);
  } catch (err) {
    res.status(500).send(err.message);
  }
});

// Fetch dealership by ID
app.get("/fetchDealer/:id", async (req, res) => {
  try {
    const id = parseInt(req.params.id);
    const dealer = await Dealership.findOne({ id: id });
    if (dealer) {
      res.json(dealer);
    } else {
      res.status(404).json({ error: "Dealer not found" });
    }
  } catch (err) {
    res.status(500).send(err.message);
  }
});

// Insert a new review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  const data = JSON.parse(req.body);
  try {
    const latestReview = await Review.findOne().sort({ id: -1 });
    const new_id = latestReview ? latestReview.id + 1 : 1;

    const review = new Review({
      id: new_id,
      name: data['name'],
      dealership: data['dealership'],
      review: data['review'],
      purchase: data['purchase'],
      purchase_date: data['purchase_date'],
      car_make: data['car_make'],
      car_model: data['car_model'],
      car_year: data['car_year'],
    });

    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
    console.error("Error inserting review:", error.message);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`🚀 Server is running on http://localhost:${port}`);
});
