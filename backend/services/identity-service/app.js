require("dotenv").config();
const express = require("express");
const cors = require("cors");

const identityRoutes = require("./routes/identity");

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

/* ── Health Check ── */
app.get("/health", (_req, res) => {
  res.json({
    service: "identity-service",
    status: "healthy",
    timestamp: new Date().toISOString(),
    version: "1.0.0",
  });
});

/* ── Routes ── */
app.use("/api/v1/identity", identityRoutes);

/* ── Start ── */
app.listen(PORT, () => {
  console.log(`✅ identity-service running on port ${PORT}`);
});

module.exports = app;
