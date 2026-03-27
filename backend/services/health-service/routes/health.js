const express = require("express");
const { v4: uuidv4 } = require("uuid");

const router = express.Router();

/**
 * POST /api/v1/health-records
 * Create a new health record for a worker.
 */
router.post("/", async (req, res) => {
  try {
    const { swasthyaId, recordType, vitals, diagnosis, notes } = req.body;

    const record = {
      id: uuidv4(),
      swasthyaId,
      recordType: recordType || "checkup",
      vitals: vitals || {},
      diagnosis: diagnosis || [],
      notes: notes || "",
      createdAt: new Date().toISOString(),
    };

    res.status(201).json(record);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

/**
 * GET /api/v1/health-records/:swasthyaId
 * Get all health records for a worker.
 */
router.get("/:swasthyaId", async (req, res) => {
  try {
    // In production: query MongoDB
    res.json({
      swasthyaId: req.params.swasthyaId,
      records: [
        {
          id: "demo-rec-001",
          recordType: "checkup",
          vitals: { bp: "120/80", spo2: 98, heartRate: 72 },
          diagnosis: ["Healthy"],
          createdAt: new Date().toISOString(),
        },
      ],
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

/**
 * GET /api/v1/health-records/:swasthyaId/timeline
 * Get health timeline for a worker.
 */
router.get("/:swasthyaId/timeline", async (req, res) => {
  try {
    res.json({
      swasthyaId: req.params.swasthyaId,
      timeline: [
        { date: "2025-01-15", event: "Annual checkup", status: "completed" },
        { date: "2025-03-10", event: "Spirometry test", status: "completed" },
        { date: "2025-06-01", event: "Follow-up", status: "scheduled" },
      ],
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
