"""
BLE (Bluetooth Low Energy) Package

This package contains tools for BLE advertising and spoofing.
"""

from .airpods_spam import airpods_spam, advertise_airpods
from .ad_spam import ad_spam

__all__ = ['airpods_spam', 'advertise_airpods', 'ad_spam']