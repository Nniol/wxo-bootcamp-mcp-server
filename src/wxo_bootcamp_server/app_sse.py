import asyncio
import logging
import sys
import traceback
from .hospital_data_tools import main_async

# Set up detailed logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def main():
    """Console script entry point with comprehensive error handling"""
    try:
        print("=" * 60)
        print("MCP Hospital Data Server Starting...")
        print("=" * 60)
        print("Server will bind to: 0.0.0.0:8080")
        print("Access from host at: http://localhost:8080")
        print("SSE endpoint: http://localhost:8080/sse")
        print("Messages endpoint: http://localhost:8080/messages")
        print("=" * 60)

        logger.info("Starting server initialization...")

        # Run the async main function
        asyncio.run(main_async("SSE"))

    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("Server stopped by user (Ctrl+C)")
        print("=" * 60)
        sys.exit(0)

    except ImportError as e:
        logger.error(f"Import error - missing dependency: {e}")
        print(f"ERROR: Missing dependency - {e}")
        sys.exit(1)

    except FileNotFoundError as e:
        logger.error(f"File not found error: {e}")
        print(f"ERROR: Required file not found - {e}")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected server error: {e}")
        print(f"ERROR: Server failed to start - {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
