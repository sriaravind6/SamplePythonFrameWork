"""
config.py - Central Configuration Management
Handles all framework-level configuration settings.
"""

import os
import logging

# ─────────────────────────────────────────────
# Logger Setup
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("config")


class Config:
    """
    Singleton-style configuration class.
    All settings can be overridden via environment variables.
    """

    # ── Application Under Test ──────────────────
    BASE_URL: str = os.getenv("BASE_URL", "https://practicetestautomation.com/practice-test-login/")

    # ── Browser Settings ────────────────────────
    BROWSER: str = os.getenv("BROWSER", "chrome")          # chrome | firefox | edge
    HEADLESS: bool = os.getenv("HEADLESS", "false").lower() == "true"
    IMPLICIT_WAIT: int = int(os.getenv("IMPLICIT_WAIT", "10"))
    EXPLICIT_WAIT: int = int(os.getenv("EXPLICIT_WAIT", "20"))
    PAGE_LOAD_TIMEOUT: int = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))

    # ── Directories ─────────────────────────────
    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SCREENSHOT_DIR: str = os.path.join(PROJECT_ROOT, "screenshots")
    REPORT_DIR: str = os.path.join(PROJECT_ROOT, "reports")
    LOG_DIR: str = os.path.join(PROJECT_ROOT, "logs")

    # ── Test Credentials (override via env vars in CI) ──
    VALID_USERNAME: str = os.getenv("TEST_USERNAME", "student")
    VALID_PASSWORD: str = os.getenv("TEST_PASSWORD", "Password123")
    INVALID_USERNAME: str = os.getenv("INVALID_USERNAME", "wrongUser")
    INVALID_PASSWORD: str = os.getenv("INVALID_PASSWORD", "wrongPass")

    @classmethod
    def ensure_directories(cls) -> None:
        """Create required directories if they don't exist."""
        for directory in [cls.SCREENSHOT_DIR, cls.REPORT_DIR, cls.LOG_DIR]:
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Directory ensured: {directory}")

    @classmethod
    def log_config(cls) -> None:
        """Log all current config values (without sensitive data)."""
        logger.info("=" * 55)
        logger.info("  Framework Configuration")
        logger.info("=" * 55)
        logger.info(f"  BASE_URL         : {cls.BASE_URL}")
        logger.info(f"  BROWSER          : {cls.BROWSER}")
        logger.info(f"  HEADLESS         : {cls.HEADLESS}")
        logger.info(f"  IMPLICIT_WAIT    : {cls.IMPLICIT_WAIT}s")
        logger.info(f"  EXPLICIT_WAIT    : {cls.EXPLICIT_WAIT}s")
        logger.info(f"  PAGE_LOAD_TIMEOUT: {cls.PAGE_LOAD_TIMEOUT}s")
        logger.info(f"  SCREENSHOT_DIR   : {cls.SCREENSHOT_DIR}")
        logger.info(f"  REPORT_DIR       : {cls.REPORT_DIR}")
        logger.info("=" * 55)
