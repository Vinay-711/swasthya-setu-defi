/**
 * SMS Worker — processes SMS notifications from the Bull queue.
 *
 * In production, this connects to an SMS gateway (e.g., Twilio, MSG91).
 */

const MOCK_GATEWAY = true;

async function processSmsJob(job) {
  const { recipient, message, swasthyaId } = job.data;

  console.log(`📨 SMS → ${recipient} | SwasthyaID: ${swasthyaId}`);
  console.log(`   Message: ${message}`);

  if (MOCK_GATEWAY) {
    // Simulate latency
    await new Promise((r) => setTimeout(r, 200));
    console.log(`   ✅ SMS delivered (mock)`);
    return { delivered: true, provider: "mock" };
  }

  // Real implementation:
  // const response = await smsGateway.send({ to: recipient, body: message });
  // return { delivered: true, provider: "msg91", messageId: response.id };
}

module.exports = { processSmsJob };
