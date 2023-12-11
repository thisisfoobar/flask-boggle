class Boggle_Game {
  //make new game at specific ID
  constructor(boardId, secs = 60) {
    this.secs = secs;
    this.showTimer();

    this.score = 0;
    this.words = new Set();
    this.board = $("#" + boardId);

    this.timer = setInterval(this.tick.bind(this), 1000);

    $(".submit-word", this.board).on("submit", this.handleSubmit.bind(this));
  }

  // Display word guessed
  showWord(word) {
    $(".words", this.board).append($("<li>", { text: word }));
  }

  // Display score
  showScore() {
    $(".score", this.board).text(this.score);
  }

  // Display status message for guess
  showMessage(msg, cls) {
    $(".msg", this.board).text(msg).removeClass().addClass(`msg ${cls}`);
  }

  async handleSubmit(evt) {
    evt.preventDefault();
    const $word = $(".word", this.board);
    let word = $word.val();

    if (!word) return;

    if (this.words.has(word)) {
      this.showMessage(`${word} has already been found`, "err");
      $word.val("").focus;
      return;
    }

    const resp = await axios.get("/check-word", { params: { word: word } });
    if (resp.data.result === "not-a-word") {
      this.showMessage(`${word} is not a word`, "err");
    } else if (resp.data.result === "not-on-board") {
      this.showMessage(`${word} is not on the board`, "err");
    } else {
      this.showWord(word);
      this.score += word.length;
      this.showScore();
      this.words.add(word);
      this.showMessage("Valid word", "valid");
    }

    $word.val("").focus;
  }

  // Display timer
  showTimer() {
    $(".timer", this.board).text(this.secs);
  }

  // Countdown timer and check for 0 time left
  async tick() {
    this.secs -= 1;
    this.showTimer();

    if (this.secs === 0) {
      clearInterval(this.timer);
      await this.scoreGame();
    }
  }

  // Post final score of game a prevent more guessing
  async scoreGame() {
    $(".submit-word", this.board).hide();
    $(".msg", this.board).text("")
    const resp = await axios.post("/post-score", { score: this.score });
    if (resp.data.brokeRecord) {
      this.showMessage(`New record: ${this.score}`, "score");
    } else {
      this.showMessage(`Final score: ${this.score}`, "score");
    }
  }
}
