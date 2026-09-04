import pytest

import server


@pytest.fixture
def client():
    """Client de test Flask, avec les données clubs/compétitions rechargées
    depuis les fichiers JSON avant chaque test.

    Important : server.py charge `clubs` et `competitions` une seule fois au
    démarrage de l'app (variables de module). Certaines routes (ex: purchasePlaces)
    modifient ces données en mémoire. Sans ce fixture, un test pourrait laisser
    des données modifiées qui fausseraient le test suivant.
    """
    server.clubs = server.loadClubs()
    server.competitions = server.loadCompetitions()

    # Volontairement PAS de TESTING=True : on veut que Flask catch les
    # exceptions non gérées et renvoie une vraie réponse 500, comme en
    # conditions réelles (c'est ce que le navigateur/l'utilisateur voit).
    with server.app.test_client() as test_client:
        yield test_client
