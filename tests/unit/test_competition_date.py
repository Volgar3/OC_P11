"""Tests unitaires de la validation de date d'une compétition (issue #5).

La fonction `is_competition_in_the_future` n'existe pas encore côté server.py —
c'est normal, ces tests pilotent sa création.

Format de date attendu (celui de competitions.json) : "%Y-%m-%d %H:%M:%S".
"""
from server import is_competition_in_the_future


def test_returns_false_for_a_past_date():
    assert is_competition_in_the_future("2020-03-27 10:00:00") is False


def test_returns_true_for_a_future_date():
    assert is_competition_in_the_future("2099-01-01 00:00:00") is True
