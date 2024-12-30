# Tetris AI Mini
In December 2024 I developed this project to demonstrate training an AI agent to play a very simple game using [Q-Learning](https://en.wikipedia.org/wiki/Q-learning#:~:text=Q%2Dlearning%20is%20a%20model,being%20in%20a%20particular%20state.), a popular reinforcement learning technique. 

![side by side](https://i.imgur.com/CCDpuFi.gif)

For full detailed breakdown of how I designed and built this, check out [my article on this project on Medium](https://timhanewich.medium.com/how-i-trained-a-neural-network-to-play-tetris-using-reinforcement-learning-ecfa529c767a)!

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