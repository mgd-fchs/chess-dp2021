# Design Patterns UE WS2021/22 - Chess

This project is an implementation of a chess game as a python web app created for the course Design Patterns 2021/22.

## Setting up the database
- run `flask db init` - it will create the migrations folder with a version subfolder.
- run `flask db migrate` - it will detect the model changes with an upgrade and downgrade logic set up.
- run `flask db upgrade` - it will apply the model changes you have implemented.
- run `flask db downgrade` - if something goes wrong, you can use this command to unapply changes you have done on your model file.

## Run the app
Run `python app.py` and then open [http://127.0.0.1:5000/](http://127.0.0.1:5000/)