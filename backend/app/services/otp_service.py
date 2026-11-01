import secrets
import string
import redis.asyncio as redis
from app.core.config import settings

def build_otp_response(otp: str) -> dict:
    """Keep demo codes out of responses outside explicit local/test environments."""
    response = {"message": "OTP sent successfully"}
    if settings.environment in {"development", "test"}:
        response["DEBUG_OTP"] = otp
    return response


# Global redis connection
redis_client = redis.from_url(settings.redis_url, decode_responses=True)

class OTPService:
    def __init__(self, ttl: int = 300):
        self.ttl = ttl  # OTP valid for 5 minutes by default

    def _generate_otp(self, length: int = 6) -> str:
        """Generate a numeric OTP."""
        return "".join(secrets.choice(string.digits) for _ in range(length))

    async def create_otp(self, phone: str) -> str:
        """Generates and stores an OTP for the phone number."""
        otp = self._generate_otp()
        key = f"otp:{phone}"
        await redis_client.set(key, otp, ex=self.ttl)
        # In a real system, you would integrate Twilio / MSG91 here
        # to send the SMS. This prototype returns it to the caller without logging it.
        return otp

    async def verify_otp(self, phone: str, otp: str) -> bool:
        """Verifies the provided OTP against the stored OTP."""
        key = f"otp:{phone}"
        stored_otp = await redis_client.get(key)
        
        if stored_otp and stored_otp == otp:
            await redis_client.delete(key)
            return True
        return False

otp_service = OTPService()
