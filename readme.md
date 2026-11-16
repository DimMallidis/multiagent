Q1 notes:   My evaluation functions main idea, was to calculate the score of each move
            based on 3 factors: 
            -if the move increases the game score(eating food or scared ghost)
            -if pacman is heading towards food (meaning if the manhattan distance to the nearest food decreases)
            -and if pacman is avoiding the nearest threat (meaning if the manhattan distance to nearest ghost increases)
            I added weight variables for the last 2 to change the importance of each factor to suit the circumstance.
            For example, when Pacman is near a not scared ghost, he completely focuses on getting away (food weight is zeroed and
            ghost weight is increased). If the ghost is scared, the ghost weight is zeroed and Pacman just focuses on the pellets.
            If the move wins the game, definitely take that action by returning an infinity score, 
            since the ghost wont get to move even if its right next to pacman(turn based game).
            If the move leads to the periphery of the ghost definitely avoid it by returning a minus infinity score (ghost will move once it gets its turn so dont step into its possible move squares).
            If the move eats a pellet, on that move the food distance difference variable is zeroed, because the sudden increase of distance
            to the next nearest pellet, will make the diff variable negative and big in abs value, meaning it might deter Pacman from eating
            the pellet.
            I ran the different courses multiple times to parameter tune and settled on the ones in the implementation.
            It even fares respectably against 2 ghosts on the normal map.
