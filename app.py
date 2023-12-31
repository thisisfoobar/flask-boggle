from boggle import Boggle
from flask import session,Flask,request,render_template,redirect,jsonify,flash
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "teehee-secretzzz"
debug = DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

boggle_game = Boggle()

@app.route("/")
def start_game():
    """Home page with start game button"""
    session["highscore"] = 0
    session["plays"] = 0
    session["board"] = []
    session["guesses"] = []
    return render_template("start-game.html",highscore = session["highscore"])

@app.route("/reset-game", methods=["POST"])
def reset_game():
    """Reset board and guesses sessions"""
    session["board"] = []
    session["guesses"] = []

    new_board = boggle_game.make_board()
    session["board"] = new_board

    return redirect("boggle-game")

@app.route("/boggle-game",methods=["POST","GET"])
def boggle_game_board():
    """Display board for new game"""

    return render_template("boggle-game.html", plays = session["plays"], highscore = session["highscore"], board = session["board"], guesses = session["guesses"])

@app.route("/check-word")
def check_word():
    """check if word is valid and on board"""
    
    word = request.args["word"]
    board = session["board"]

    response = boggle_game.check_valid_word(board,word)

    return jsonify({'result': response})

@app.route("/post-score",methods=["POST"])
def post_score():
    """post final score and update high score"""
    score = request.json["score"]
    highscore = session["highscore"]
    plays = session["plays"]

    session["plays"] = plays + 1
    session["highscore"] = max(score, highscore)

    return jsonify(brokeRecord = score > highscore)