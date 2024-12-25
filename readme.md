# Tetris AI Mini
In December 2024 I developed this project to demonstrate training an AI agent to play a very simple game using [Q-Learning](https://en.wikipedia.org/wiki/Q-learning#:~:text=Q%2Dlearning%20is%20a%20model,being%20in%20a%20particular%20state.), a popular reinforcement learning technique. 

![side by side](https://i.imgur.com/CCDpuFi.gif)

## Project Description
In the sections below, I'll explain various facets of this project and how they all came together:

### The Game
The game the agent will play is a *very* simplified version of the game Tetris. The "board" is 4 rows by 4 columns, a 4x4 matrix. The game is very simple: the AI agent must choose which of the 4 columns to "drop" a single box into, one-by-one, with the goal of eventually filling all 16 squares of the board.

Despite this game seeming extremely easy and obvious to play at first glance, there is actually a lot that can go wrong. If the AI is not capable of learning the nature of the game, it will continuously play random moves, eventually playing a move that is illegal.

For example, consider the position below:

![pos](https://i.imgur.com/5AFmsZe.png)

If the model doesn't understand the game and is essentially playing at random, there is a 25% chance it will choose to drop a square into column 4 (the column on the far right). This would be an *illegal* move, invalidating the game. 

My goal in training this model is for the model to play the game effectively and productively, avoiding illegal moves.

### The Method
To train an AI to play this simplified game of Tetris, we will use [Q-Learning](https://en.wikipedia.org/wiki/Q-learning#:~:text=Q%2Dlearning%20is%20a%20model,being%20in%20a%20particular%20state.). Q-Learning is a type of reinforcement learning algorithm in machine learning. The goal of Q-Learning is to find the optimal action-selection policy for any potential game state. What does that mean? Let's take a closer look...

When we set up a model to train via Q-Learning, we are repeatedly allowing the model to encounter, act, and observe through self-play. In other words, through each "step" of a game, the current situation of the game (that the model has to make a decision against) is called **the state**. The model sees the state and then makes a decision on what the next move should be; this move is called **the action**. After the selected move (action) is executed against the game, the model observes *what happened* - did the move make the situation better? Worse? This is called **the reward**.

The model plays the game by itself over and over and over and over... many thousands of times! Eventually, the model has collected so many state, action, reward pairs (called "experiences"), that it can **learn from these experiences and develop a decent understanding of which moves in which states lead to the highest rewards (most success).

I'll go into further detail on Q-Learning and how this mini Tetris AI specifically uses it in a future writing, but for now, just know the collection of **state, action, reward** pairs is key!

### The Model
A [TensorFlow](https://www.tensorflow.org/) sequential neural network will be used to estimate the estimated rewards for each potential move in a given position described above. I used the [Keras](https://keras.io/) API to make the high-level manipulation of the neural network easier.

As mentioned above, every time the model is asked to make the decision of what move to play next, it is presented with a current "state" of the game. This is a simple representation of the entire situation of the game, including all criteria that the model should consider when deciding what to do next.

In the case of this mini Tetris game, the "state" is quite simple: with a 4x4 board of 16 squares, that leaves 16 unique inputs. Each of the 16 inputs will be represented and "shown" to the model as a `1` or `0`; if the particular square is occupied, that square's position will be expressed as a `1`, if it is empty, a `0`.

For example, consider the following board state:

![board_state](https://i.imgur.com/8ZVAC50.png)

The board state in the image above can be represented as the following array of integers, with each square being expressed as a `0` or `1`, with each square's position in the array labeled in the image above:

```
[0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1]
```

So, our neural network will consider **16 inputs** when evaluating a position and what move to play next. What about outputs? In Q-Learning, the neural network is designed to predict the "Q-Value", or estiamted current/future rewards, for every possible move in any given state. Since the game we are playing has **4 potential moves** (drop a square in column 1, 2, 3, or 4), our neural network will have **4 outputs**.

Our neural network will also have several **hidden layers**, which are mathematical layers of neurons that are connected between the input and output layers. These hidden layers serve as "the brain" of the neural network, constantly adjusting through training to "learn" the nature of the game and relationship between states, moves, and their associated reward.

Below is the code used to construct the entire model:

```
# build layers
input_board = keras.layers.Input(shape=(16,), name="input_board")
carry = keras.layers.Dense(64, "relu", name="layer1")(input_board)
carry = keras.layers.Dense(64, "relu", name="layer2")(carry)
carry = keras.layers.Dense(32, "relu", name="layer3")(carry)
output = keras.layers.Dense(4, "linear", name="output")(carry)

# construct the model
self.model = keras.Model(inputs=input_board, outputs=output)
self.model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.003), loss="mse")
```

### The Reward Function
As mentioned above, the neural network is designed to approximate the **Q-Value** of each potential move from any given state of the game. "Q-Value" is just a fancy term for a blend of current and future rewards (i.e. "in the immediate term and long term, how well will this move serve me?"). If the model is able to approximate the reward for all four possible moves from any state, the model can simply pick the move that it thinks will return the greatest reward as the **suggested next optimal move**.

But, how will the model intrinsically know which moves are "good", which are "not so good", and which are "bad"? That is where we, as the human designing this process, need to give the AI agent a bit of guidance. This guidance is called *the reward function*.

In short, the reward function is just a simple fuction we will write to mathematically calculate *how good* any potential move is. Remember, for each move the AI makes, it observers what **reward** it got for making that move. We are the ones that define a high-level function that can roughly calculate if the move was good or bad. 

The reward function I used for this mini Tetris AI is quite simple and can be found in the `score_plus()` function in the `GameState` class in the [`tetris` module](src/tetris.py):


```
def score_plus(self) -> float:
        
    # start at score
    ToReturn:float = float(self.score())

    # penalize for standard deviation
    stdev:float = statistics.pstdev(self.column_depths())
    ToReturn = ToReturn - (stdev * 2)

    return ToReturn
```

Firstly, I've set up my system to determine **the reward** based simply upon the difference between this "score_plus" *after* the move and *before* the move. In other words, the model observes the `score_plus` before the move is made, makes the move, and then again observes the `score_plus`, with the difference (increase) being the reward.

My reward function is quite simple. Firstly, the `score` of the game is tallied up - this is just the number of squares of the board that are occupied. After this, I'm using a simple standard deviation function to calculate the deviation in "column depth", or how many squares of each column are not occupied. 

A greater amount of standard deviation means the board is being developed in a very unbalanced manner - i.e. one side is very tall while the other is not; this is not good for a game of Tetris. A very "level" board will instead equate to a small standard deviation. By **subtracting** the column depth standard deviation from the total score, we can **penalize** the model from building uneven, unbalanced boards, incentivizing the construction of balanced boards.

### The Training Process
With our underlying model built and reward function established, it is now time to train the model! As mentioned previously, the model will be left to its own devices, playing the game over-and-over on its own. It will start with **zero** knowledge on how to play the game - just the ability to observe the game, make a decision, and see what reward it got for that decision. 

By repeating this over and over through self-play and **training** on these results, the neural network eventually forms the relationship between the current state of the board, a potential decision that could be made, and the typical reward for such a decision. And once this understanding is cemented, playing a game as best-as-possible is simple; all we have to do is always select the move (action) that the model anticipates will reap the greatest reward!

More specifically, the following is the boiled-down training process. The full training script can be found in [train.py](./src/train.py).
1. Initialize a new neural network.
2. Collect a few hundred **state, action, reward** experiences through a combination of selecting the moves the model *thinks are best* (
    1. Convert the state of the current game to a list of integers.
    2. Select a move to play based on what the model *thinks* is best but is probably not because the model doesn't know anything yet!)  or a random move. A random move is occasionally selected to encourage **exploration**. Read more about exploratation vs. exploration [here](https://en.wikipedia.org/wiki/Exploration-exploitation_dilemma).
    3. Execute (play) the move and observe the reward that was given for that move.
    4. Store this **state, action, reward** "experience" into a collection.
3. Loop through all of these collected **state, action, reward** experiences, one by one, each time training on the experience (updating the neural networks weights) to better approximate the correct reward given a state and action.
    1. Calculate what the Q-Value (immediate/future reward) *should be* (a blending of immediate/future rewards that represents the total reward of this decision).
    2. Ask the model to predict what it *thinks* the reward (Q-Value) *would be*.
    3. The model's prediction is probably incorrect because it doesn't know anything yet. 
    4. "Correct" the model by training it against the **correct Q-Value** calculated above in step 1.
    5. Do this over and over for every experience.
4. Repeat the above steps repeatedly until the model learns how to play the game effectively and legally!

### The Results
After setting up the training process described above in the [train.py](./src/train.py) module, I let this run for ~4 hours. After training on 85,000 **state, action, reward** experiences over these 4 hours, my model successfully learned to play the game **perfectly**. The model plays the game pefectly from **any state** - from a new game position (blank board) or even a "randomized" position. Every time the game plays, it always scores 16 (perfect score) for each "game" and never makes an illegal move.

My model trained on 85,000 experiences (moves), but I don't think this many was necessary. As it appears in the training log file, optimal performance seemed to be achieved around the 4,500 experience (move) mark.

You can download my trained model from the **Model Checkpoints** section below and run it in the [evaluate.py](./src/evaluate.py) script.

![example](https://i.imgur.com/1sBHFrA.gif)

## Exaplanation of Code Files
All code is available in the [src folder](./src/):
- [tetris.py](./src/tetris.py) - The core Tetris game engine. Capable of representing the game board, "dropping" squares into columns, and determining rewards for specific moves.
- [play.py](./src/play.py) - If you want to try playing the game of Tetris yourself with your keyboard, run this!
- [representation.py](./src/representation.py) - Specialized in converting the core Tetris game board (`GameState`) to a flattened list of integers that can be inputted into a neural network (a numeric representation of the game board).
- [intellience.py](./src/intelligence.py) - Contains the `TetrisAI` class, a higher-level class focused on creating, manipulating, and training the custom-build neural network.
- [train.py](./src/train.py) - The training script. Applies Q-Learning to train the Tetris AI to play the game through reinforcement learning. 
- [evaluate.py](./src/evaluate.py) - After you train and save a model via the [train.py](./src/train.py) script, load the model into [evaluate.py](./src/evaluate.py) to observe it playing move by move.
- [visuals.py](./src/visuals.py) - Simple functions I wrote to generate a graphical representation of the board at any state in the game.
- [visgen.py](./src/visgen.py) - Uses the [visuals.py](./src/visuals.py) to generate a series of frames of the AI playing that can be stitched together via FFMPEG.
- [tools.py](./src/tools.py) - Simple tools used throughout this project.

## Model Checkpoints
|Checkpoint|Commit|Description|
|-|-|-|
|[download](https://github.com/TimHanewich/tetris-ai-mini/releases/download/1/checkpoint16.keras)|`a02de2357791f170b9f9090347a22e72646fde73`|Trained on 85,000 experiences (though this many experiences are likely not required to reach this level of performance - evidence to suggest only 4,500 would have been enough). Trained from the ground up with no knowledge from blank new game state. Plays the game perfectly, filling each row from left to right until all 16 are filled. In addition to a blank starting state, this model has also proven to play perfectly **even at random, uneven starting positions**. Training log file [here](https://github.com/TimHanewich/tetris-ai-mini/releases/download/1/log.txt).|

## Notable Commits
- `a02de2357791f170b9f9090347a22e72646fde73` - first version to confirm training works! This approach works as the model learned to play the game perfectly.

## Use FFMPEG to stitch images into video
To export to MP4 video:
```
ffmpeg -i %06d.png -r 15 output.mp4
```

You can also export to a GIF
```
ffmpeg -i %06d.png -r 15 output.gif
```

## Other Misc. Resources
- The 4x4 grid used in the visuals was designe in PowerPoint. Deck [here](https://github.com/TimHanewich/tetris-ai-mini/releases/download/2/grid.pptx).