"""Tests unitaires de calculate_remaining_points (issue #2) — sans Flask/HTTP."""
from server import calculate_remaining_points


def test_returns_none_when_not_enough_points():
    assert calculate_remaining_points(club_points=4, places_required=5) is None


def test_returns_remaining_balance_when_enough_points():
    assert calculate_remaining_points(club_points=13, places_required=5) == 8


def test_returns_zero_when_places_equal_available_points():
    assert calculate_remaining_points(club_points=4, places_required=4) == 0
