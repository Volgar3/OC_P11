import html

# ==========================
# Issue 1
# ==========================


def test_show_summary_with_known_email_displays_welcome_page(client):
    """Tester avec une adresse mail connu"""
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})

    assert response.status_code == 200
    assert b"Simply Lift" in response.data or b"john@simplylift.co" in response.data


def test_show_summary_with_unknown_email_shows_error_without_crashing(client):
    """Tester avec une adresse mail inconnu dans la DB"""
    response = client.post("/showSummary", data={"email": "inconnu@example.com"})

    assert response.status_code == 200
    page_text = html.unescape(response.get_data(as_text=True))
    assert "Sorry, that email wasn't found" in page_text
