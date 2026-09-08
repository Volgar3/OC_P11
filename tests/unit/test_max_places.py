"""Tests unitaires de la limite de 12 places max par compétition (issue #4).

La fonction `is_places_request_valid` n'existe pas encore côté server.py —
c'est normal, ces tests pilotent sa création.
"""
from server import is_places_request_valid


def test_allows_a_single_place():
    assert is_places_request_valid(1) is True


def test_allows_exactly_the_maximum_of_12_places():
    assert is_places_request_valid(12) is True


def test_rejects_more_than_12_places():
    assert is_places_request_valid(13) is False
