from istorage import IStorage
import json
import requests
import os
from movie_app import MovieApp

class StorageJson(IStorage):
    def __init__(self, file_path):
        self._file_path = file_path
        try:
            storage_file = open(file_path)
        except FileNotFoundError:
            with open(file_path, "w") as new_file:
                new_file.write("{}")

                print(f"File did not exist yet. New file is now created as {file_path}")


    def list_movies(self):
        """
        Returns a dictionary of dictionaries that
        contains the movies information in the database.

        The function loads the information from the JSON
        file and returns the data.
        """
        try:
            with open(self._file_path, "r") as handle:
                return json.load(handle)
        except FileNotFoundError:
            with open(self._file_path, "w") as handle:
                handle.write("")


    def add_movie(self, title):
        """
        Adds a movie to the movies database.
        Loads the information from the JSON file, add the movie,
        and saves it. The function doesn't need to validate the input.
        """
        print(f"Inside storage_json -- function add_movie, the title is: {title}")

        try:
            response_API = requests.get("http://www.omdbapi.com/?apikey=4220af53&t=" + str(title))
        except requests.exceptions.HTTPError:
            error_message = "Http Error"
            print(error_message)
            return error_message
        except requests.exceptions.ConnectionError:
            error_message = "Connection Error"
            print(error_message)
            return error_message
        except requests.exceptions.Timeout:
            error_message = "Timeout Error"
            print(error_message)
            return error_message
        except requests.exceptions.RequestException:
            error_message = "Oops, something went wrong"
            print(error_message)
            return error_message

        data = response_API.text
        parse_json = json.loads(data)
        if parse_json["Response"] == "False":
            print(parse_json["Error"])
            return parse_json["Error"]
        else:
            title = parse_json["Title"]
            year_data = parse_json["Year"]
            if len(year_data) > 4:
                year = int(year_data[:4])
                print(f"Multiple years available for this movie."
                      f" Original year {year} used.")
            else:
                year = int(parse_json["Year"][:4])
            rating = float(parse_json["imdbRating"])
            poster_img_url = parse_json["Poster"]
            all_movies = self.list_movies()
            imbd_id = parse_json["imdbID"]
            link_to_imbd_website = "https://www.imdb.com/title/" + imbd_id
            movie_data = {"rating": rating, "year": year, "poster_img_url": poster_img_url, "imbd_website": link_to_imbd_website}
            all_movies[title] = movie_data
            json_str = json.dumps(all_movies)
            with open(self._file_path, "w") as handle:
                handle.write(json_str)

            print(f"The movie {title} successfully added with a rating of {rating}")



    def delete_movie(self, title):
        """
        Deletes a movie from the movies database.
        Loads the information from the JSON file, deletes the movie,
        and saves it. The function doesn't need to validate the input.
        """
        all_movies = self.list_movies()
        if title in all_movies:
            del all_movies[title]
            print(f"The movie {title} has been deleted.")
        json_str = json.dumps(all_movies)
        with open(self._file_path, "w") as handle:
            handle.write(json_str)

    def update_movie(self, title, personal_rating):
        """
        Updates a movie from the movies database.
        Loads the information from the JSON file, updates the rating of the movie,
        and saves it. The function doesn't need to validate the input.
        """
        all_movies = self.list_movies()
        if title in all_movies:
            all_movies[title]["personal rating"] = personal_rating
            json_str = json.dumps(all_movies)
        with open(self._file_path, "w") as handle:
            handle.write(json_str)
