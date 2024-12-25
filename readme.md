# Tetris AI Mini

## Model Checkpoints
|Checkpoint|Commit|Description|
|-|-|-|
|[download](https://github.com/TimHanewich/tetris-ai-mini/releases/download/1/checkpoint16.keras)|`a02de2357791f170b9f9090347a22e72646fde73`|Trained on 85,000 experiences (though this many experiences are likely not required to reach this level of performance - evidence to suggest only 4,500 would have been enough). Trained from the ground up with no knowledge from blank new game state. Plays the game perfectly, filling each row from left to right until all 16 are filled. Log file [here](https://github.com/TimHanewich/tetris-ai-mini/releases/download/1/log.txt).|

## Notable Commits
- `a02de2357791f170b9f9090347a22e72646fde73` - first version to confirm training works! This approach works as the model learned to play the game perfectly.