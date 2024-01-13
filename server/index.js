const express = require("express");
const port = 5000;
const app = express();
app.use(express.json());

app.post("/twitch", (req, res) => {
    const twitchMessage = req.body;
    console.log(twitchMessage);
  
    if (twitchMessage && twitchMessage.displayName && twitchMessage.content) {
      res.sendStatus(200);
    } else {
      res.status(400).send("Invalid Twitch message format");
    }
});

app.listen(port, () => {
  console.log(`Discord bridge listening at http://localhost:${port}`);
});