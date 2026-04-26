"""Phishing module - Educational phishing framework with multiple templates"""

from .facebook_phish import FacebookPhishing
from .google_phish import GooglePhishing

__all__ = ['FacebookPhishing', 'GooglePhishing']
