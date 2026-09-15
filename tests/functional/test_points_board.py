"""Tests fonctionnels du tableau public des points (issue #7, Phase 2).
Contrat attendu :
- Route GET /points, accessible directement (sans passer par /showSummary).
- Affiche le nom et le solde de points de chaque club.
"""


def test_points_board_accessible_without_login(client):
    """La page doit être accessible directement, sans jamais s'être connecté."""
    response = client.get("/points")
    assert response.status_code == 200


def test_points_board_lists_all_clubs_with_their_points(client):
    """Chaque club (nom + solde de points) doit apparaître dans le tableau."""
    response = client.get("/points")
    page_text = response.get_data(as_text=True)

    assert "Simply Lift" in page_text
    assert "13" in page_text
    assert "Iron Temple" in page_text
    assert "4" in page_text
    assert "She Lifts" in page_text
    assert "12" in page_text


def test_points_board_also_shown_on_home_page(client):
    response = client.get("/")
    page_text = response.get_data(as_text=True)

    assert "Simply Lift" in page_text
    assert "13" in page_text
    assert "Iron Temple" in page_text
    assert "4" in page_text
    assert "She Lifts" in page_text
    assert "12" in page_text
