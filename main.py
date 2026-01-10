import sys
import traceback

try:
    from api.index import app
    handler = app
    print("✅ Successfully imported app from api.index", file=sys.stderr)
except Exception as e:
    print(f"❌ ERROR importing api.index: {e}", file=sys.stderr)
    print(f"Traceback: {traceback.format_exc()}", file=sys.stderr)
    
    # Fallback: create minimal app
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/")
    async def root():
        return {
            "error": "Failed to import main app",
            "details": str(e),
            "traceback": traceback.format_exc()
        }
    
    handler = app
