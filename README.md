Program to create your own movie database website.
The database can be stored in a .json file, or a .txt file (with a csv format) for easy use. 

The main function requires:
    * storage choosing between StorageJson for a .json database or StorageCsv for a .txt file in csv format, with the argument of the filename, including the extension.
    * if the database does not yet exist, a new file will be created with the given name.
    * movie_app takes the argument storage, and a string with a name (which will be displayed on the website)

When the app is running, it allows the user to:
      0. Exit
      1. List movies
      2. Add movie
      3. Delete movie
      4. Update personal rating
      5. Stats
      6. Random movie
      7. Search movie
      8. Movies sorted by rating
      9. Generate website
