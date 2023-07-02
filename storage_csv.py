from istorage import IStorage
import requests
import json


class StorageCsv(IStorage):
    def __init__(self, file_path):
        self._file_path = file_path
        try:
            open(file_path)
        except FileNotFoundError:
            with open(file_path, "w") as new_file:
                new_file.write("title,rating,year,poster_img_url,imbd_website,personal rating")

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
                lines = handle.readlines()
                movie_dictionary = {}
                for line in lines:
                    splitted_line = line.split(",")
                    if len(splitted_line) == 1:
                        continue
                    if splitted_line[0] == "title":
                        continue
                    try:
                        personal_rating = float(splitted_line[5])
                    except ValueError:
                        personal_rating = ""
                    movie_dictionary[splitted_line[0]] = {
                        "rating": float(splitted_line[1]),
                        "year": int(splitted_line[2]),
                        "poster_img_url": splitted_line[3],
                        "imbd_website": splitted_line[4],
                        "personal_rating": personal_rating,
                    }

                return movie_dictionary
        except FileNotFoundError:
            with open(self._file_path, "a") as handle:
                handle.write("")

    def add_movie(self, title):
        """
        Adds a movie to the movies database.
        Loads the information from the JSON file, add the movie,
        and saves it. The function doesn't need to validate the input.
        """
        try:
            response_api = requests.get("http://www.omdbapi.com/?apikey=4220af53&t=" + str(title))
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

        data = response_api.text
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
            imbd_id = parse_json["imdbID"]
            link_to_imbd_website = "https://www.imdb.com/title/" + imbd_id
            personal_rating = ""
            in_database = False
            with open(self._file_path, "r") as handle:
                lines = handle.readlines()
                for line in lines:
                    if title in line:
                        print(f"movie {title} already in database")
                        in_database = True
            if not in_database:
                with open(self._file_path, "a") as handle:
                    handle.write(f"{title},{rating},{year},{poster_img_url},{link_to_imbd_website},{personal_rating}\n")

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

        with open(self._file_path, "w") as handle:
            handle.write("title,rating,year,poster_img_url,imbd_website,personal rating\n")
        for movie in all_movies:
            self.add_movie(movie)

    def update_movie(self, title_to_update, new_personal_rating):
        """
        Updates a movie from the movies database.
        Loads the information from the JSON file, updates the rating of the movie,
        and saves it. The function doesn't need to validate the input.
        """
        updated_lines = []
        with open(self._file_path, "r") as handle:
            all_lines = handle.readlines()
            for line in all_lines:
                splitted_line = line.split(",")
                if line[0] == "title":
                    updated_lines.append(line)
                    continue
                title = splitted_line[0]
                rating = splitted_line[1]
                year = splitted_line[2]
                poster_img_url = splitted_line[3]
                imbd_website = splitted_line[4]
                if splitted_line[0] == title_to_update:
                    personal_rating = new_personal_rating
                else:
                    personal_rating = splitted_line[5]
                new_line = f'{title},{rating},{year},{poster_img_url},{imbd_website},{personal_rating}\n'
                updated_lines.append(new_line)

        open(self._file_path, "w").close()

        with open(self._file_path, "a") as handle:
            for line in updated_lines:
                handle.write(line)
