from locust import HttpUser, between, task

CLUBS = ["Simply Lift", "Iron Temple", "She Lifts"]
EMAILS = {
    "Simply Lift": "john@simplylift.co",
    "Iron Temple": "admin@irontemple.com",
    "She Lifts": "kate@shelifts.co.uk",
}
COMPETITIONS = ["Spring Festival", "Fall Classic"]


class SecretaryUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def fetch_competitions_list(self):
        """Récupérer la liste des compétitions (contrainte : <= 5 secondes)."""
        club = CLUBS[0]
        with self.client.post(
            "/showSummary",
            data={"email": EMAILS[club]},
            name="/showSummary (liste des compétitions)",
            catch_response=True,
        ) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure("Plus de 5 secondes pour récupérer la liste des compétitions")

    @task(1)
    def update_points_total(self):
        with self.client.post(
            "/purchasePlaces",
            data={"competition": COMPETITIONS[0], "club": CLUBS[0], "places": "1"},
            name="/purchasePlaces (mise à jour des points)",
            catch_response=True,
        ) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure("Plus de 2 secondes pour mettre à jour le total de points")

    @task(1)
    def view_points_board(self):
        self.client.get("/points", name="/points (tableau public)")
