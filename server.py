import json
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for


def load_clubs():
    with open("clubs.json") as c:
        list_of_clubs = json.load(c)["clubs"]
        return list_of_clubs


def load_competitions():
    with open("competitions.json") as comps:
        list_of_competitions = json.load(comps)["competitions"]
        return list_of_competitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = load_competitions()
clubs = load_clubs()


@app.route("/")
def index():
    return render_template("index.html")


def find_club_by_email(clubs, email):
    matching_clubs = [club for club in clubs if club["email"] == email]
    return matching_clubs[0] if matching_clubs else None


@app.route("/showSummary", methods=["POST"])
def show_summary():
    club = find_club_by_email(clubs, request.form["email"])
    if not club:
        flash("Sorry, that email wasn't found.")
        return render_template("index.html")
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    found_club = [c for c in clubs if c["name"] == club][0]
    found_competition = [c for c in competitions if c["name"] == competition][0]

    if not is_competition_in_the_future(found_competition["date"]):
        flash("Sorry, you cannot book a place for a competition that has already taken place.")
        return render_template("welcome.html", club=found_club, competitions=competitions)

    return render_template("booking.html", club=found_club, competition=found_competition)

def calculate_remaining_places(competition_places, places_required):
    """Renvoie le solde de points restant, ou None si trop de place prise par rapport
    aux nombres de places disponible"""
    if places_required > competition_places:
        return None
    return  competition_places - places_required


def calculate_remaining_points(club_points, places_required):
    """Renvoie le solde de points restant, ou None si pas assez de points disponibles."""
    if places_required > club_points:
        return None
    return club_points - places_required


def is_places_request_valid(places_required, max_places=12):
    return places_required <= max_places

def is_competition_in_the_future(competition_date):
    actual_date = datetime.now()
    competition_date = datetime.strptime(competition_date, "%Y-%m-%d %H:%M:%S")
    return actual_date < competition_date

@app.route("/purchasePlaces", methods=["POST"])
def purchase_places():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][0]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    places_required = int(request.form["places"])
    remaining_points = calculate_remaining_points(int(club["points"]), places_required)

    if remaining_points is None:
        flash("Sorry, you don't have enough points for that many places.")
        flash("Please, remake your request")
        return render_template("welcome.html", club=club, competitions=competitions)

    elif not is_places_request_valid(places_required):
        flash("Sorry, you cannot book more than 12 places for a competition.")
        return render_template("welcome.html", club=club, competitions=competitions)

    elif not is_competition_in_the_future(competition["date"]):
        flash("Sorry, you cannot book a place for a competition that has already taken place.")
        return render_template("welcome.html", club=club, competitions=competitions)

    remaining_places = calculate_remaining_places(
        int(competition["numberOfPlaces"]), places_required
    )
    if remaining_places is None:
        flash("Sorry, there are not enough places available for this competition.")
        return render_template("welcome.html", club=club, competitions=competitions)

    competition["numberOfPlaces"] = remaining_places
    club["points"] = remaining_points
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
