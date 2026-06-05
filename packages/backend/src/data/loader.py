"""Load mock customer bundles from the repo-root data directory.

Mock files live at: <repo>/data/customers/<slug>/
This package (backend ``data``) is only the Python loader — not those files.
"""

from pathlib import Path

from schemas.credit_report import CustomerMetadata

# repo root: .../credit-application-analyst
REPO_ROOT = Path(__file__).resolve().parents[4]
CUSTOMERS_DIR = REPO_ROOT / "data" / "customers"


def customer_dir(slug: str) -> Path:
    path = CUSTOMERS_DIR / slug
    if not path.is_dir():
        raise FileNotFoundError(f"No customer data for slug={slug!r} at {path}")
    return path
