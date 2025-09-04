import asyncio
import logging
import sys
from pathlib import Path

# Add the src directory to Python path for direct execution
if __name__ == "__main__":
    src_path = Path(__file__).parent.parent
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

# Try relative import first, then absolute
try:
    from .wxo_bootcamp_tools import main_async
except ImportError:
    try:
        from src.wxo_bootcamp_mcp_server.wxo_bootcamp_tools import main_async
    except ImportError:
        from src.wxo_bootcamp_mcp_server.wxo_bootcamp_tools import main_async

# Set up logging to stderr (so it doesn't interfere with STDIO transport)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,  # Important: log to stderr, not stdout
)
logger = logging.getLogger(__name__)


def main():
    """Console script entry point for STDIO transport"""
    try:
        logger.info("MCP Hospital Data Server starting with STDIO transport")
        logger.info("This server is designed for GitHub/Watson Orchestrate integration")

        # Run the async main function
        asyncio.run(main_async("STDIO"))

    except KeyboardInterrupt:
        logger.info("Server stopped by user (Ctrl+C)")
        sys.exit(0)

    except ImportError as e:
        logger.error(f"Import error - missing dependency: {e}")
        sys.exit(1)

    except FileNotFoundError as e:
        logger.error(f"File not found error: {e}")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected server error: {e}")
        logger.error("Full traceback:", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
