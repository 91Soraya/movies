from movie_app import MovieApp
from storage_json import StorageJson

def main():
    """
    takes a storage file and runs the movie app with the movie data in the storage file
    """
    storage = StorageJson('data.json')
    movie_app = MovieApp(storage, "Soraya")

    movie_app.run()

if __name__ == '__main__':
    main()