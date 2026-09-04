"""Tests unitaires de findClubByEmail (issue #1) — aucune dépendance à Flask/HTTP."""
import pytest

from server import findClubByEmail

CLUBS = [
    {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
    {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
]


def test_returns_matching_club_when_email_exists():
    result = findClubByEmail(CLUBS, "admin@irontemple.com")
    assert result["name"] == "Iron Temple"


@pytest.mark.parametrize("email", [
    "inconnu@example.com",  # email inconnu mais bien formé
    "banane",                # format invalide (la validation HTML côté navigateur
])
def test_returns_none_when_no_club_matches(email):
    assert findClubByEmail(CLUBS, email) is None


def test_returns_none_when_clubs_list_is_empty():
    assert findClubByEmail([], "john@simplylift.co") is None
