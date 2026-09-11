"""Tests unitaires de la vérification des places disponibles (issue #282).

La fonction `calculate_remaining_places` n'existe pas encore côté server.py —
c'est normal, ces tests pilotent sa création. Même patron que
`calculate_remaining_points` (issue #2) : None si pas assez, sinon le solde
restant.
"""
from server import calculate_remaining_places


def test_returns_none_when_not_enough_places_available():
    assert calculate_remaining_places(competition_places=3, places_required=5) is None


def test_returns_remaining_places_when_enough_available():
    assert calculate_remaining_places(competition_places=25, places_required=5) == 20


def test_returns_zero_when_places_required_equals_available():
    assert calculate_remaining_places(competition_places=3, places_required=3) == 0
