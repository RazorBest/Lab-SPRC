from flask import Flask
from flask import request, jsonify, Response

app = Flask(__name__)

# MOVIE_LIST = ["Star Wars 1 - Yoda Version", "Man in Black", "Shreck"]
MOVIES = [ ]
ID = 1

@app.route("/movies", methods=["GET"])
def get_movies():
    return jsonify(MOVIES), 200

@app.route("/movies", methods=["POST"])
def post_movies():
    global ID

    payload = request.get_json(silent=True)
    if not payload:
        return Response(status=400)

    if not isinstance(payload, dict) or "nume" not in payload:
        return Response(status=400)

    MOVIES.append({"id": ID, "nume": payload["nume"]})
    ID += 1
    
    return Response(status=201)

@app.route("/movie/<int:id>", methods=["PUT"])
def put_movie_id(id):
    payload = request.get_json(silent=True)
    if not payload:
        return Response(status=400)

    if not isinstance(payload, dict) or "nume" not in payload:
        return Response(status=400)

    for movie in MOVIES:
        if movie["id"] == id: 
            movie["nume"] = payload["nume"]
            return Response(status=200)
    
    return Response(status=404)

@app.route("/movie/<int:id>", methods=["GET"])
def get_movie_id(id):
    for movie in MOVIES:
        if movie["id"] == id:
            return jsonify(movie), 200
    return Response(status=404)

@app.route("/movie/<int:id>", methods=["DELETE"])
def delete_movie_id(id):
    for movie in MOVIES:
        if movie["id"] == id:
            MOVIES.remove(movie)
            return Response(status=200)

    return Response(status=404)

@app.route("/reset", methods=["DELETE"])
def delete_reset():
    global MOVIES
    global ID

    MOVIES = []
    ID = 1

    return Response(status=200)


def main():
    app.run('0.0.0.0', debug=True)


if __name__ == '__main__':
    main()
