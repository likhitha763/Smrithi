from fastapi import FastAPI
from app.routes import profile, sessions, reminders, dashboard, settings

app = FastAPI(
    title="SPARSH — Smrithi API",
    description=(
        "Backend for SPARSH cognitive-care platform. "
        "All /api/* endpoints require Authorization: Bearer <Firebase ID token>."
    ),
    version="1.0.0",
)

# ── Health ────────────────────────────────────────────────────────────────────
@app.get("/health", tags=["infra"])
def health():
    """Liveness check — no auth required."""
    return {"status": "ok"}

# ── PRD endpoint set ──────────────────────────────────────────────────────────
app.include_router(profile.router)     # POST/GET/PATCH /api/patients
app.include_router(sessions.router)    # POST/GET /api/patients/{id}/sessions
app.include_router(reminders.router)   # POST/GET/PATCH /api/patients/{id}/reminders
app.include_router(dashboard.router)   # GET /api/patients/{id}/dashboard
app.include_router(settings.router)    # stub (deprecated, kept for import safety)