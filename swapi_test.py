import pytest as pytest
import requests

base_url = "https://swapi.dev/api/"
film_id = 2


@pytest.fixture
def films_url():
    return base_url + "films/"


@pytest.fixture
def planets_url():
    return base_url + "planets/"


def test_get_swapi_endpoints():
    response = requests.get(base_url)
    data = response.json()

    print("Доступные SWAPI Эндпоинты:")

    for endpoint, url in data.items():
        print(f"- {endpoint.capitalize()}: {url}")

    assert response.status_code == 200
    assert "films" in response.json()
    assert "planets" in response.json()
    assert "species" in response.json()
    assert "people" in response.json()


def test_get_films(films_url):
    response = requests.get(films_url)
    data = response.json()

    print("Список фильмов:")
    for film in data["results"]:
        print(f"- {film['title']}")

    assert response.status_code == 200
    assert "results" in response.json()


def test_get_selected_film_info(films_url):
    selected_film_url = f"{films_url}{film_id}"
    response = requests.get(selected_film_url)
    selected_film_data = response.json()

    print("\nИНФОРМАЦИЯ О ВЫБРАННОМ ФИЛЬМЕ:\n")
    print(f"Название: {selected_film_data['title']}")
    print(f"Режиссер: {selected_film_data['director']}")
    print(f"Дата выхода: {selected_film_data['release_date']}")
    print(f"Начальные титры: {selected_film_data['opening_crawl']}")

    assert response.status_code == 200
    assert "title" in selected_film_data
    assert "director" in selected_film_data
    assert "release_date" in selected_film_data
    assert "opening_crawl" in selected_film_data


def test_get_planets(planets_url):
    response = requests.get(planets_url)
    data = response.json()

    print("\nСписок всех планет:")
    for planet in data["results"]:
        print(f" - {planet['name']}")

    assert response.status_code == 200
    assert "results" in response.json()


def test_get_planet_info(films_url):
    film_url = f"{films_url}{film_id}"
    response = requests.get(film_url)
    film_data = response.json()

    assert response.status_code == 200
    assert len(film_data["planets"]) > 0

    print("\nИнформация о планете из фильма:")

    first_planet_url_in_list = film_data["planets"][0]
    response_planet = requests.get(first_planet_url_in_list)
    planet_info = response_planet.json()

    print(f" - {planet_info['name']}")
    print(f"   Климат: {planet_info['climate']}")
    print(f"   Местность: {planet_info['terrain']}")
    print(f"   Население: {planet_info['population']}")

    assert response_planet.status_code == 200
    assert "name" in planet_info
    assert "climate" in planet_info
    assert "terrain" in planet_info
    assert "population" in planet_info


def test_get_species_info(films_url):
    films_url = f"{films_url}{film_id}"
    response = requests.get(films_url)
    film_data = response.json()

    print("\nСписок расс:")

    for species_url in film_data['species']:
        species_response = requests.get(species_url)
        species_data = species_response.json()

        print(f"- {species_data['name']}")
        print(f"  Classification: {species_data.get('classification', 'N/A')}")
        print(f"  Language: {species_data.get('language', 'N/A')}")
        print()

        assert species_response.status_code == 200
        assert "name" in species_data
        assert "classification" in species_data
        assert "language" in species_data

    assert response.status_code == 200


def test_get_starship_and_pilots(films_url):
    film_url = f"{films_url}{film_id}"
    response = requests.get(film_url)
    film_data = response.json()

    assert response.status_code == 200
    assert len(film_data) > 0

    starship_url = film_data['starships'][1]
    starship_response = requests.get(starship_url)
    starship_data = starship_response.json()

    print(f"\nКосмический корабль: {starship_data['name']}")

    assert starship_response.status_code == 200
    assert len(starship_data) > 0

    print("\nПилоты:")

    # Получаем информацию о пилотах корабля
    for pilot_url in starship_data['pilots']:
        pilot_response = requests.get(pilot_url)
        pilot_data = pilot_response.json()

        print(f"- {pilot_data['name']}")
        print(f"  Год рождения: {pilot_data.get('birth_year', 'N/A')}")
        print(f"  Пол: {pilot_data.get('gender', 'N/A')}")
        print()

        assert pilot_response.status_code == 200
        assert "name" in pilot_data
        assert "birth_year" in pilot_data
        assert "gender" in pilot_data
