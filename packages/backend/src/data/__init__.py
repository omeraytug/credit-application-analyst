"""Mock customer data loading (filesystem → Pydantic)."""

from .loader import CUSTOMERS_DIR, REPO_ROOT, customer_dir

__all__ = ["CUSTOMERS_DIR", "REPO_ROOT", "customer_dir"]
