import os
import sys
from pathlib import Path

# Avoid scanning every installed package for Pydantic plugins during tests. This
# is slow and can fail on cloud-synced worktrees when dist-info files are evicted.
os.environ.setdefault("PYDANTIC_DISABLE_PLUGINS", "1")

# Pandas probes optional pyarrow support at import time. In this OneDrive-backed
# local environment that optional import can block collection, and the unit tests
# do not exercise parquet/feather functionality.
sys.modules.setdefault("pyarrow", None)

# Ensure src/ package is importable when running pytest without editable install.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
