Q1 Notes:   My evaluation functions main idea, was to calculate the score of each move
            based on 3 factors:
            - if the move increases the game score (eating food or scared ghost)
            - if pacman is heading towards food (meaning if the manhattan distance to the nearest food decreases)
            - and if pacman is avoiding the nearest threat (meaning if the manhattan distance to nearest ghost increases)

            I added weight variables for the last 2 to change the importance of each factor to suit the circumstance.
            For example, when Pacman is near a not scared ghost, he completely focuses on getting away (food weight is
            zeroed and ghost weight is increased). If the ghost is scared, the ghost weight is zeroed and Pacman just
            focuses on the pellets.

            If the move wins the game, definitely take that action by returning an infinity score,
            since the ghost wont get to move even if its right next to pacman (turn based game).
            If the move leads to the periphery of the ghost definitely avoid it by returning a minus infinity score
            (ghost will move once it gets its turn so dont step into its possible move squares).
            If the move eats a pellet, on that move the food distance difference variable is zeroed, because the sudden
            increase of distance to the next nearest pellet, will make the diff variable negative and big in abs value,
            meaning it might deter Pacman from eating the pellet.

            I ran the different courses multiple times to parameter tune and settled on the ones in the implementation.
            It even fares respectably against 2 ghosts on the normal map.

Q2 Notes: I wrote a helper function: minimax_helper, which holds the agent_index and
          depth parameters so it can be used recursively.

          The recursion base case is either the states where max depth has been reached (no more minimax rounds to go through) or the isWin or isLose states (leaf nodes in our minimax tree).

          If its Pacmans (max player) turn, we get the maximum value out of minimax values for the successor state first ghost agent. Those function calls are done with the agentIndex parameter set to 1 (first ghost) so that our order of the minimax round is secured: pacman -> ghost -> ghost -> and so on.
          
          The ghosts (min player) return the minimum value out of minimax values for the successor state. When at the last ghost, we check if the round is finished (if [(agentIndex + 1) % (number of agents)] == 0) to increment the depth.

          Outside of the helper function, we get the legal moves of pacman and call minimax for each of the successor states (so minimax starts in the middle of the algo, meaning we call it for the first ghost). GetAction returns the action associated with the maximum value returned, essentially playing out the root of minimax.