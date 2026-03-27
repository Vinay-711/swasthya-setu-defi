const express = require("express");
const { v4: uuidv4 } = require("uuid");
const QRCode = require("qrcode");
const Worker = require("../models/worker");

const router = express.Router();

/**
 * POST /api/v1/identity/create
 * Generate a new SwasthyaID for a migrant worker.
 */
router.post("/create", async (req, res) => {
  try {
    const { name, phone, age, occupation, state, language } = req.body;

    const swasthyaId = `SID-${uuidv4().slice(0, 8).toUpperCase()}`;
    const qrDataUrl = await QRCode.toDataURL(
      JSON.stringify({ swasthyaId, name })
    );

    const worker = new Worker({
      swasthyaId,
      name,
      phone,
      age,
      occupation,
      state,
      language: language || "hi",
    });

    // In production: await worker.save();

    res.status(201).json({
      swasthyaId,
      worker: worker.toObject(),
      qrDataUrl,
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

/**
 * GET /api/v1/identity/:swasthyaId
 * Lookup worker by SwasthyaID.
 */
router.get("/:swasthyaId", async (req, res) => {
  try {
    // In production: const worker = await Worker.findOne({ swasthyaId: req.params.swasthyaId });
    res.json({
      swasthyaId: req.params.swasthyaId,
      name: "Demo Worker",
      phone: "+91-XXXXXXXXXX",
      consentGranted: true,
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

/**
 * PUT /api/v1/identity/:swasthyaId/consent
 * Update consent status.
 */
router.put("/:swasthyaId/consent", async (req, res) => {
  try {
    const { consentGranted } = req.body;
    res.json({
      swasthyaId: req.params.swasthyaId,
      consentGranted,
      updatedAt: new Date().toISOString(),
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

/**
 * POST /api/v1/identity/:swasthyaId/link-abha
 * Link ABHA number to SwasthyaID.
 */
router.post("/:swasthyaId/link-abha", async (req, res) => {
  try {
    const { abhaNumber } = req.body;
    res.json({
      swasthyaId: req.params.swasthyaId,
      abhaNumber,
      linked: true,
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
