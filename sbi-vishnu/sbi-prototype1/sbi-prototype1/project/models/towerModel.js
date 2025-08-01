const mongoose = require("mongoose");

const towerSchema = new mongoose.Schema({
  towerId: { type: String, required: true, unique: true },
  latitude: Number,
  longitude: Number,
  address: String
});

const Tower = mongoose.model("SBI_tower_data", towerSchema);
