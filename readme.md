# Tetris AI Mini
Training an AI (neural network) to play a *very* simplified version of 4x4 Tetris using [Q-Learning](https://en.wikipedia.org/wiki/Q-learning#:~:text=Q%2Dlearning%20is%20a%20model,being%20in%20a%20particular%20state.).

![example](https://i.imgur.com/1sBHFrA.gif)

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