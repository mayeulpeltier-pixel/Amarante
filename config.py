#!/usr/bin/env python3
# config.py — AMARANTE INTEL v1.0 — Configuration centralisée
# =============================================================================
# SOURCE DE VÉRITÉ UNIQUE pour toutes les constantes du projet.
# Importé par tous les scripts.
#
# Inspiré de SENTINEL config.py v3.60 (mêmes patterns de robustesse)
# =============================================================================

from __future__ import annotations

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ---------------------------------------------------------------------------
# VERSION
# ---------------------------------------------------------------------------
VERSION = "1.0"
APP_NAME = "Amarante Intel"

# ---------------------------------------------------------------------------
# CHEMINS ABSOLUS — invalides en cron sinon
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR     = PROJECT_ROOT / "data"
LOGS_DIR     = PROJECT_ROOT / "logs"
OUTPUT_DIR   = PROJECT_ROOT / "output"
PROMPTS_DIR  = PROJECT_ROOT / "prompts"
CACHE_DIR    = DATA_DIR / "cache"
MEMORY_DIR   = DATA_DIR / "memory_by_country"

# Création automatique des répertoires requis
for _d in [DATA_DIR, LOGS_DIR, OUTPUT_DIR, PROMPTS_DIR, CACHE_DIR, MEMORY_DIR,
           OUTPUT_DIR / "charts", OUTPUT_DIR / "reports"]:
    _d.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# MODÈLES ANTHROPIC
# ---------------------------------------------------------------------------
SONNET_MODEL = os.environ.get("AMARANTE_MODEL", "claude-sonnet-4-6")
HAIKU_MODEL  = os.environ.get("HAIKU_MODEL",    "claude-haiku-4-5")
OPUS_MODEL   = os.environ.get("OPUS_MODEL",     "claude-opus-4-7")  # pour analyses critiques

# ---------------------------------------------------------------------------
# CLÉS API
# ---------------------------------------------------------------------------
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
TAVILY_API_KEY    = os.environ.get("TAVILY_API_KEY",    "")
ACLED_API_KEY     = os.environ.get("ACLED_API_KEY",     "")
ACLED_EMAIL       = os.environ.get("ACLED_EMAIL",       "")
NEWSAPI_KEY       = os.environ.get("NEWSAPI_KEY",       "")
GDELT_BASE_URL    = "https://api.gdeltproject.org/api/v2/doc/doc"

# Fallback OpenAI (en cas de surcharge Anthropic, comme Sentinel)
OPENAI_API_KEY    = os.environ.get("OPENAI_API_KEY", "")
OPENAI_FALLBACK_MODEL = os.environ.get("OPENAI_FALLBACK_MODEL", "gpt-4o-mini")

# ---------------------------------------------------------------------------
# PIPELINE — limites pour maîtriser les coûts
# ---------------------------------------------------------------------------
MAX_TOKENS_OUTPUT = int(os.environ.get("AMARANTE_MAX_TOKENS",   "8000"))
TAVILY_MAX_CALLS  = int(os.environ.get("AMARANTE_TAVILY_MAX",   "5"))
NEWS_DAYS_BACK    = int(os.environ.get("AMARANTE_NEWS_DAYS",    "30"))
ACLED_DAYS_BACK   = int(os.environ.get("AMARANTE_ACLED_DAYS",   "90"))
MAX_ARTICLES      = int(os.environ.get("AMARANTE_MAX_ARTICLES", "50"))
CACHE_TTL_HOURS   = int(os.environ.get("AMARANTE_CACHE_TTL",    "6"))

# ---------------------------------------------------------------------------
# BASE DE DONNÉES
# ---------------------------------------------------------------------------
DB_PATH = Path(os.environ.get("AMARANTE_DB", str(DATA_DIR / "amarante.db")))

# ---------------------------------------------------------------------------
# AUTHENTIFICATION (Streamlit)
# ---------------------------------------------------------------------------
AUTH_CONFIG_PATH = PROJECT_ROOT / "auth_config.yaml"
SESSION_TIMEOUT_MIN = int(os.environ.get("AMARANTE_SESSION_TIMEOUT", "60"))

# ---------------------------------------------------------------------------
# NIVEAUX DE RISQUE — Échelle officielle Amarante
# ---------------------------------------------------------------------------
RISK_LEVELS = {
    1: {"label": "FAIBLE",   "color": "#22c55e", "description": "Risques courants, vigilance standard"},
    2: {"label": "MODÉRÉ",   "color": "#eab308", "description": "Vigilance accrue, briefing recommandé"},
    3: {"label": "ÉLEVÉ",    "color": "#f97316", "description": "Mesures renforcées, escorte recommandée"},
    4: {"label": "CRITIQUE", "color": "#ef4444", "description": "Voyage déconseillé sauf nécessité absolue"},
    5: {"label": "EXTRÊME",  "color": "#7f1d1d", "description": "Voyage formellement déconseillé"},
}

# ---------------------------------------------------------------------------
# CIRCUIT-BREAKER (anti-surcharge API)
# ---------------------------------------------------------------------------
CB_FAIL_THRESHOLD = 3  # 3 échecs consécutifs → fallback
CB_RESET_HOURS    = 1  # auto-reset après 1h

# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------
LOG_FILE   = LOGS_DIR / "amarante.log"
LOG_MAX_MB = 50

# ---------------------------------------------------------------------------
# DRY RUN (test sans appels API réels)
# ---------------------------------------------------------------------------
DRY_RUN = os.environ.get("AMARANTE_DRY_RUN", "").lower() in ("1", "true", "yes")

# ---------------------------------------------------------------------------
# VALIDATION CRITIQUE AU DÉMARRAGE
# ---------------------------------------------------------------------------
def validate_config() -> list[str]:
    """Retourne la liste des erreurs de configuration. Liste vide = OK."""
    errors = []
    if not ANTHROPIC_API_KEY:
        errors.append("ANTHROPIC_API_KEY manquante (.env)")
    if not PROMPTS_DIR.exists():
        errors.append(f"Répertoire prompts/ absent : {PROMPTS_DIR}")
    return errors
