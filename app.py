"""
Hugging Face Spaces Entry Point
Serves the Manufacturing QC Environment on Hugging Face Spaces
"""

from server import app

# This file is used by Hugging Face Spaces to start the application
# The actual FastAPI app is defined in server.py

if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
