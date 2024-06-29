# Truco B0T 🎴🤖

## What is my project? 🤔

Mi Project is a Windows application that allows you to play the popular Argentinian card game, Truco, against a bot. Truco is a zero-sum, imperfect information game that uses a Spanish deck without 8s, 9s, and jokers. It can be played by 2, 4, or 6 players divided into two teams, with the objective of reaching 30 points. For shorter matches, the game can be played until 15 points.

Please find the ruleset for Truco at the following link: [Truco Rules](https://www.pagat.com/put/truco_ar.html).
It is important to note that there are several variants of this game. In this app, we will be playing the “sin-flor” (no-flower) version.

## What did I use to make it? 🛠️

I developed this application using Python and Tkinter along with some other libraries. The libraries utilized in this project include Pillow, Random, Os, and, as previously mentioned, Tkinter.

- **Tkinter** is the primary library used for creating the graphical user interface in my project.
- **Pillow** was used to ensure compatibility of .jpg files with Tkinter, which is not typically possible.
- **Random** is used to make some aspects of the bot's behavior unpredictable.
- **Os** is used to determine the directory path of the script and to resolve any issues related to locating the 'images' folder.

## Why did I make it? 🎯

I chose to create a Truco bot as my final project for three main reasons. Firstly, I enjoy creating games that people can enjoy, and I find Truco to be a fun and challenging game. Secondly, I believe it is a way to showcase a part of the culture of my country, Argentina. Lastly, the idea of creating a Truco bot has been on my mind for over a year, but my lack of experience at coding made it impossible.

## How does it work? ⚙️

When executing the app, the user will be presented with three options and the app title.
- The first option is a button located in the upper-right corner, which displays the United States flag representing the English language. Clicking on it will change the flag to an Argentinian flag representing the Spanish language. This allows the user to choose their preferred language for using the app.
- The second option is a drop-down menu for selecting whether the match will end at reaching 30 or 15 points.
- Finally, clicking the 'play' button will start the match.

Once the match has started, information will be displayed at the top of the screen indicating which player is 'hand', the current 'truco' state, and the scores of the players.

Below that, the bot's comments will appear, such as 'Truco' or 'Falta envido'.
The table where you are playing will be displayed below the comments, and during the hand, each card played will be shown there.
Your cards and announcement options will be displayed below the table, together with other actions: “I want”, “I don’t want”, “Truco”, “Envido”, “Real envido”, “Falta envido” and “Fold”.

After the envido or a hand, a message box will appear showing which player gained points and the amount of points.

## Code design 📝

The code is divided in 4 parts:

1. **Development of the game** 🎮
   - This code section contains two core functions: match and hand. The match function is responsible for the loop and checking if someone wins, while the hand function is more extensive and goes through all the stages of a hand, calling functions from the 'In game logic and functionalities' section when needed.

2. **In game logic and functionalities** 🔄
   - This section is crucial as it includes important functionalities such as user and bot inputs, the envido phase, result checking, and returning to the hand function.

3. **Bot thinking process** 🧠
   - This section required extensive planning to determine the bot's thought process and strategies.
     - Check if I can announce envido
       - If I can, check if my cards are good enough or if I want to lie and announce it
     - Check if I can announce truco
       - If I can, check if my cards are good enough or if I want to lie and announce it
     - Determine in which round I am
       - Depending on the round, process information and decide which card I am going to play
     - One of the most interesting parts of the thought process occurs during the first round when it plays first. The cards are ranked into 17 different categories, each with its own strategies and playstyles.

4. **Gui** 🖼️
   - This section describes two scenes: the main scene, which is the home screen that allows the user to choose between several options and start a match, and the match scene where the game is played.
