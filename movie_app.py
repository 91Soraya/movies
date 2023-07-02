import statistics
import random

class MovieApp:
    def __init__(self, storage, username):
        self._storage = storage
        self._username = username


    def _command_list_movies(self):
        """
        For movie in storage, print movie title and movie rating
        """
        movies = self._storage.list_movies()
        for movie in movies:
            print(movie, movies[movie]["rating"])


    def get_list_of_ratings(self):
        """From the movie data file,
        :returns a list of the ratings"""
        movies = self._storage.list_movies()
        ratings = []
        for movie in movies:
            ratings.append(movies[movie]["rating"])

        return ratings

    def average_rating(self):
        """
        From the movie data file calculates the average rating as average.
        returns a string with the average rating
        """
        ratings = self.get_list_of_ratings()
        average = sum(ratings) / len(ratings)
        return average

    def median_rating(self):
        """
        From the movie data file gets the median rating,
        prints the median rating.
        """
        ratings = self.get_list_of_ratings()
        sorted_list_of_ratings = sorted(ratings)
        median = statistics.median(sorted_list_of_ratings)
        return median

    def best_rated_movie(self):
        """
        From the movie data file gets the highest rated movie,
        and prints the movie and its rating.
        """
        best_movies = []
        movies = self._storage.list_movies()
        ratings = self.get_list_of_ratings()
        highest_rating = max(ratings)
        for movie in movies:
            if movies[movie]["rating"] == highest_rating:
                best_movie = (movie, movies[movie]["rating"])
                best_movies.append(best_movie)
        return best_movies


    def worst_rated_movie(self):
        """
        From the movie data file gets the lowest rated movie,
        and prints the movie and its rating.
        """
        worst_movies = []
        movies = self._storage.list_movies()
        ratings = self.get_list_of_ratings()
        lowest_rating = min(ratings)
        for movie in movies:
            if movies[movie]["rating"] == lowest_rating:
                worst_movie = (movie, movies[movie]["rating"])
                worst_movies.append(worst_movie)
        return worst_movies

    def random_movie(self):
        """
        From the movie data file gets a random movie,
        and prints the movie and its rating.
        """
        movies = self._storage.list_movies()
        random_movie = random.choice(list(movies.items()))
        title = random_movie[0]
        rating = movies[random_movie[0]]["rating"]
        print(f"Your movie for tonight: {title}, it´s rated {rating}")

    def search_movie(self):
        """
        Requests part of movie title from user input,
        searches for the movie in the movie data file,
        and prints the movie and the rating.
        """
        movies = self._storage.list_movies()
        user_search_input = input("Enter part of movie name: ")
        for movie in movies:
            if user_search_input.lower() in movie.lower():
                print(f"{movie}, with rating: {movies[movie]['rating']}")

    def movies_sorted_by_rating(self):
        """
        Sorts the movies by rating from the movie data file.
        """
        movies = self._storage.list_movies()
        ratings = self.get_list_of_ratings()
        sorted_ratings = sorted(ratings, reverse=True)
        for rating in sorted_ratings:
            for movie in movies:
                if movies[movie]["rating"] == rating:
                    print(f'{movie}: {movies[movie]["rating"]}')


    def _command_movie_stats(self):
        """
        Invokes functions to get the average rating, median rating,
        best rated movie and worst rated movie from the movie data file,
        that all print the information.
        """
        average = self.average_rating()
        median = self.median_rating()
        best = self.best_rated_movie()
        worst = self.worst_rated_movie()

        print("-" * 100)
        print(f"The average is: {average}")
        print(f"The median is: {median}")
        for best_movie in best:
            print(f"Movie with the highest rating is: {best_movie[0]} ({best_movie[1]})")

        for worst_movie in worst:
            print(f"Movie with the lowest rating is: {worst_movie[0]} ({worst_movie[1]})")

        return "-" * 100

    def create_li_html_movies(self, movie):
        movies = self._storage.list_movies()
        try:
            movie_info = (f"""     
                <li>
                    <div class="movie">
                        <a href={movies[movie]["imbd_website"]} target="_blank" ><img class="movie-poster" src={movies[movie]["poster_img_url"]}></a>
                        <div class="movie-title">{movie}</div>
                        <div class="movie-rating"> IMBD Rating: {movies[movie]["rating"]}</div>
                        <div class="movie-rating"> Personal rating: {movies[movie]["personal rating"]}</div>
                        <div class="movie-year">{movies[movie]["year"]}</div>
                    </div>
                </li>""")
        except KeyError:
            movie_info = (f"""     
                            <li>
                                <div class="movie">
                                    <a href={movies[movie]["imbd_website"]} target="_blank" ><img class="movie-poster" src={movies[movie]["poster_img_url"]}></a>
                                    <div class="movie-title">{movie}</div>
                                    <div class="movie-rating"> IMBD Rating: {movies[movie]["rating"]}</div>
                                    <div class="movie-year">{movies[movie]["year"]}</div>
                                </div>
                            </li>""")

        return movie_info


    def _generate_website(self):
        movies = self._storage.list_movies()
        title = " " + self._username + "´s movies"
        full_html = ""

        with open("_static/index_template.html", "r") as template_handle:
            line = template_handle.readline()
            while "<h1>__TEMPLATE_TITLE__</h1>" not in line:
                full_html = full_html + line
                line = template_handle.readline()

            full_html = full_html + f"<h1>{title}</h1>"
            full_html = full_html + "</div>"
            full_html = full_html + "<div>"
            full_html = full_html + '<ol class="movie-grid">'
            for movie in movies:
                full_html = full_html + self.create_li_html_movies(movie)
            full_html = full_html + "</ol>"
            full_html = full_html + "</div>"
            full_html = full_html + "</body>"
            full_html = full_html + "</html>"

        with open("_static/index.html", "w") as handle:
            handle.write(full_html)

        print("Website was generated successfully.")


    def display_menu(self):
        """Prints the menu options on the screen"""
        menu = """Menu:
      0. Exit
      1. List movies
      2. Add movie
      3. Delete movie
      4. Update personal rating
      5. Stats
      6. Random movie
      7. Search movie
      8. Movies sorted by rating
      9. Generate website"""
        return menu


    def menu_selection(self, menu_selection):
        """
        Takes user input menu selection and invokes the function related to the selected option
        """
        if menu_selection == 0:
            print("Bye!")
            quit()
        if menu_selection == 1:
            self._command_list_movies()
        if menu_selection == 2:
            self._storage.add_movie(input("Enter title: "))
        if menu_selection == 3:
            self._storage.delete_movie(input("Enter title to remove: "))
        if menu_selection == 4:
            self._storage.update_movie(input("Enter title to update: "), input("Enter new rating: "))
        if menu_selection == 5:
            self._command_movie_stats()
        if menu_selection == 6:
            self.random_movie()
        if menu_selection == 7:
            self.search_movie()
        if menu_selection == 8:
            self.movies_sorted_by_rating()
        if menu_selection == 9:
            self._generate_website()
        press_enter_to_continue = input("Press enter to continue")
        if press_enter_to_continue == "":
            self.run()


    def run(self):
        # Print menu
        print("********** My Movies Database **********")
        print(self.display_menu())
        # Get use command
        user_selection = int(input("Enter choice (0-8): "))
        self.menu_selection(user_selection)
        # Execute command
