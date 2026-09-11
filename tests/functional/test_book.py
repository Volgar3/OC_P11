"""Tests fonctionnels de /book — blocage des compétitions passées (issue #5).

Contrat attendu :
- Une compétition passée ne doit PAS afficher booking.html : un message
  d'erreur est affiché à la place :
  "Sorry, you cannot book a place for a competition that has already taken place."
- Une compétition future doit afficher normalement booking.html.
- (Les compétitions passées restent visibles dans welcome.html — déjà le cas,
  pas besoin d'y toucher.)
"""
import html


def test_book_rejected_for_past_competition(client):
    """Fall Classic est daté de 2025 (passé) : la page de réservation ne doit pas s'afficher."""
    response = client.get("/book/Fall%20Classic/Simply%20Lift")

    assert response.status_code == 200
    page_text = html.unescape(response.get_data(as_text=True))

    assert "How many places?" not in page_text
    assert (
        "Sorry, you cannot book a place for a competition that has already taken place."
        in page_text
    )


def test_book_allowed_for_future_competition(client):
    """Spring Festival est daté de 2027 (futur) : la page de réservation doit s'afficher."""
    response = client.get("/book/Spring%20Festival/Simply%20Lift")

    assert response.status_code == 200
    assert "How many places?" in response.get_data(as_text=True)
