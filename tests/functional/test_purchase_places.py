"""Tests fonctionnels de /purchasePlaces — validation du solde de points (issue #2).

Un club ne doit pas pouvoir utiliser plus de points qu'il n'en a disponible
(le solde ne doit jamais devenir négatif), et les points utilisés doivent être
correctement déduits du total du club en cas de réservation réussie.

Données de référence (clubs.json) :
- Iron Temple  : 4 points
- Simply Lift  : 13 points

Contrat attendu par ces tests (à respecter dans le fix) :
- Message d'erreur si pas assez de points : "Sorry, you don't have enough points
  for that many places."
- En cas de succès, le message existant "Great-booking complete!" reste affiché.
"""
import html


def test_purchase_rejected_when_not_enough_points(client):
    """Iron Temple a 4 points ; réserver 5 places doit être refusé, sans effet de bord."""
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Spring Festival", "club": "Iron Temple", "places": "5"},
    )

    assert response.status_code == 200
    page_text = html.unescape(response.get_data(as_text=True))

    assert "Great-booking complete!" not in page_text
    assert "Sorry, you don't have enough points for that many places." in page_text
    # Le solde du club ne doit pas avoir bougé (pas de déduction sur un achat refusé).
    assert "Points available: 4" in page_text


def test_purchase_places_deducts_points_when_enough_available(client):
    """Simply Lift a 13 points ; réserver 5 places doit réussir et déduire les points."""
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Fall Classic", "club": "Simply Lift", "places": "5"},
    )

    assert response.status_code == 200
    page_text = html.unescape(response.get_data(as_text=True))

    assert "Great-booking complete!" in page_text
    assert "Points available: 8" in page_text


def test_purchase_allowed_when_places_equal_available_points(client):
    """Réserver exactement le nombre de points disponibles doit réussir (limite incluse)."""
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Spring Festival", "club": "Iron Temple", "places": "4"},
    )

    assert response.status_code == 200
    page_text = html.unescape(response.get_data(as_text=True))

    assert "Great-booking complete!" in page_text
    assert "Points available: 0" in page_text
