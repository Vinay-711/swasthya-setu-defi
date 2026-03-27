const mongoose = require("mongoose");

const workerSchema = new mongoose.Schema(
  {
    swasthyaId: { type: String, unique: true, required: true, index: true },
    abhaNumber: { type: String, unique: true, sparse: true },
    name: { type: String, required: true },
    phone: { type: String, required: true },
    age: Number,
    occupation: String,
    state: String,
    language: { type: String, default: "hi" },
    bloodType: String,
    allergies: [String],
    currentMedications: [String],
    consentGranted: { type: Boolean, default: true },
    isActive: { type: Boolean, default: true },
  },
  { timestamps: true }
);

module.exports = mongoose.model("Worker", workerSchema);
