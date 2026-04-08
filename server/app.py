"""
Hugging Face Spaces Entry Point
Serves the Manufacturing QC Environment on Hugging Face Spaces
"""

import os
import uvicorn
from server import app


def main():
    """Main entry point for the server"""
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
