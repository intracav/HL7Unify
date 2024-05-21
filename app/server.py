# Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.medlang import format_hl7, hub, classifier

# Create the FastAPI app
app = FastAPI(
    title="MedLang API",
    description="MedLang's API for standardizing medical data",
    version="0.1.0",
    docs_url="/",
)

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routes
app.include_router(format_hl7.router)
app.include_router(hub.router)
app.include_router(classifier.router)

if __name__ == "__main__":
    # Run the app
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
