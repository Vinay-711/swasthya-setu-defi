require("dotenv").config();
const express = require("express");
const cors = require("cors");

const healthRoutes = require("./routes/health");

const app = express();
const PORT = process.env.PORT || 3002;

app.use(cors());
app.use(express.json());

/* ── Health Check ── */
app.get("/health", (_req, res) => {
  res.json({
    service: "health-service",
    status: "healthy",
    timestamp: new Date().toISOString(),
    version: "1.0.0",
  });
});

/* ── Routes ── */
app.use("/api/v1/health-records", healthRoutes);

/* ── Start ── */
app.listen(PORT, () => {
  console.log(`✅ health-service running on port ${PORT}`);
});

module.exports = app;
