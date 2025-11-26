"""
External Feature APIs für Time Series Forecasting.

Verfügbare Clients:
- HolidayAPIClient: Feiertage für verschiedene Länder
- BundesbankAPIClient: Deutsche Wirtschaftsdaten (EZB Zinsen, etc.)
- ECBAPIClient: Euro-Raum Statistiken
- ExternalFeatureOrchestrator: Koordiniert alle APIs
"""

from .base_client import FeatureAPIClient
from .holiday_client import HolidayAPIClient
from .bundesbank_client import BundesbankAPIClient
from .orchestrator import ExternalFeatureOrchestrator
from .data_manager import FeatureDataManager

__all__ = [
    'FeatureAPIClient',
    'HolidayAPIClient',
    'BundesbankAPIClient',
    'ExternalFeatureOrchestrator',
    'FeatureDataManager',
]

__version__ = '1.0.0'
