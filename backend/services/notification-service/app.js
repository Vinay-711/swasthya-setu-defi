require("dotenv").config();
const express = require("express");
const cors = require("cors");

const app = express();
const PORT = process.env.PORT || 3006;

app.use(cors());
app.use(express.json());

/* ── Health Check ── */
app.get("/health", (_req, res) => {
  res.json({
    service: "notification-service",
    status: "healthy",
    timestamp: new Date().toISOString(),
    version: "1.0.0",
    queues: { sms: "idle", whatsapp: "idle" },
  });
});

/* ── Send Notification ── */
app.post("/api/v1/notifications/send", async (req, res) => {
  try {
    const { channel, recipient, message, swasthyaId } = req.body;

    // In production: enqueue via Bull
    const notification = {
      id: `notif-${Date.now()}`,
      channel: channel || "sms",
      recipient,
      message,
      swasthyaId,
      status: "queued",
      createdAt: new Date().toISOString(),
    };

    res.status(201).json(notification);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

/* ── List Notifications ── */
app.get("/api/v1/notifications/:swasthyaId", async (req, res) => {
  try {
    res.json({
      swasthyaId: req.params.swasthyaId,
      notifications: [
        {
          id: "notif-demo-001",
          channel: "sms",
          message: "Your screening is scheduled for tomorrow.",
          status: "sent",
          sentAt: new Date().toISOString(),
        },
      ],
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

/* ── Start ── */
app.listen(PORT, () => {
  console.log(`✅ notification-service running on port ${PORT}`);
});

module.exports = app;
