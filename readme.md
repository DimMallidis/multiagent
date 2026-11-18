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

Q3 Notes: The form is similar to minimax. The base case of the recursion where we return evaluation values is the
          same (max depth reached, win state, lose state). The depth and next agent logic is also the same as minimax.

          If its Pacmans (max player) turn, we call the helper on each successor state and check if the max value so far is higher than beta. In that case, since the min player (ghost) above
          the max player (pacman) already has a better (lower) value (beta), we prune the branch we were examining.
          Otherwise we update alpha as we loop through the successor states, when we find better options.
          We generate each successor state one at a time inside the loop, only after the previous one didnt cause a prune,
          so pruned states are never generated.

          The ghosts turn is similar, main difference being we check if the min value returned is lesser than alpha.
          In that case, the nearest max player above (pacman), already has a better option (alpha).
          Otherwise we update beta when we find lower values.
          The fact that we call the helper function during a ghost turn for the next ghost, doesnt create a problem
          because a ghost calling another ghost passes alpha down unchanged.

          Outside of the helper function, we get the legal moves of pacman and call alpha beta for each of the successor states (so the algo starts in the middle of the turns, meaning we call it for the first ghost). GetAction returns the action associated with the maximum value returned, essentially playing out the root of alpha beta.
          After each action, alpha is updated to the best value so far and passed into the next actions calls, so later root branches can prune too.
          The root itself never prunes, since there is no ghost above it.

Q4 Notes: I copied my code from minimax and changed the ghosts logic from returning the minimum of the 
          returns of the helper function to the average.

          The ghosts are expected to move randomly, as mentioned in the exercise text.

          There is no pruning, thats why I copied from minimax.

          On trappedClassic alpha beta loses every time where as expectimax wins about half of the time
          since it correctly doesnt assume that the ghost play optimally.
          That way pacman takes more risks to eat pellets, instead of rushing the ghost.
          With alpha beta, pacman rushes it since death looks certain and to get the highest possible score in that
          scenario, pacman take the fewest steps possible to the ghost.

Q5 Notes: The base of the evaluation is the current game score and the other values adjust it.
          The evaluation function splits the ghosts based on if they are scared or not.
          Scared ghosts are ignored, unless they are very close in which case we attack them by adding a big bonus to the score.
          Ghosts that are not scared are avoided by subtracting a value from the score.
          We move towards food by adding a value as well.
          All three values use the reciprocal of the distance, so the closer something is, the more it affects the score,
          as suggested by the exercise text.