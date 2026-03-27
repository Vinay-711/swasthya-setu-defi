/**
 * WhatsApp Worker — processes WhatsApp notifications from the Bull queue.
 *
 * In production, this connects to WhatsApp Business API.
 */

const MOCK_GATEWAY = true;

async function processWhatsAppJob(job) {
  const { recipient, message, swasthyaId, templateName } = job.data;

  console.log(`💬 WhatsApp → ${recipient} | SwasthyaID: ${swasthyaId}`);
  console.log(`   Template: ${templateName || "custom"}`);
  console.log(`   Message: ${message}`);

  if (MOCK_GATEWAY) {
    await new Promise((r) => setTimeout(r, 300));
    console.log(`   ✅ WhatsApp delivered (mock)`);
    return { delivered: true, provider: "mock" };
  }

  // Real implementation:
  // const response = await whatsappApi.sendTemplate({
  //   to: recipient,
  //   template: templateName,
  //   parameters: { message },
  // });
  // return { delivered: true, provider: "meta", messageId: response.id };
}

module.exports = { processWhatsAppJob };
