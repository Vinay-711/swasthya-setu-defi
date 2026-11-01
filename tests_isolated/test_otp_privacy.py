import contextlib
import importlib.util
import io
import secrets
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

settings = types.SimpleNamespace(redis_url="redis://example.invalid", environment="development")
redis_client = types.SimpleNamespace(set=AsyncMock(), get=AsyncMock(), delete=AsyncMock())
redis_async = types.ModuleType("redis.asyncio")
redis_async.from_url = lambda *args, **kwargs: redis_client
redis_package = types.ModuleType("redis")
redis_package.asyncio = redis_async
config = types.ModuleType("app.core.config")
config.settings = settings
spec = importlib.util.spec_from_file_location("otp_under_test", Path(__file__).parents[1] / "backend/app/services/otp_service.py")
service = importlib.util.module_from_spec(spec)
with patch.dict(sys.modules, {"redis": redis_package, "redis.asyncio": redis_async, "app.core.config": config}):
    spec.loader.exec_module(service)

class OTPPrivacyTests(unittest.IsolatedAsyncioTestCase):
    async def test_generated_code_and_phone_are_not_printed(self):
        output = io.StringIO()
        with patch.object(service.OTPService, "_generate_otp", return_value="012345"), contextlib.redirect_stdout(output):
            result = await service.OTPService().create_otp("synthetic-phone")
        self.assertEqual(result, "012345")
        self.assertNotIn("012345", output.getvalue())
        self.assertNotIn("synthetic-phone", output.getvalue())
    def test_generation_uses_security_randomness_and_preserves_leading_zeros(self):
        with patch("secrets.choice", return_value="0") as choice:
            result = service.OTPService()._generate_otp()
        self.assertEqual(result, "000000")
        self.assertEqual(choice.call_count, 6)
    def test_only_explicit_development_and_test_responses_include_debug_code(self):
        for environment in ("production", "staging", "unknown", ""):
            with self.subTest(environment=environment):
                settings.environment = environment
                self.assertNotIn("DEBUG_OTP", service.build_otp_response("012345"))
        for environment in ("development", "test"):
            settings.environment = environment
            self.assertEqual(service.build_otp_response("012345")["DEBUG_OTP"], "012345")
        settings.environment = "development"
