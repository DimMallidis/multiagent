# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** MY CODE HERE ***"
        # initialize food list
        newFoodList = newFood.asList()
        
        # use weight variables to adjust the importance of each factor
        # like food and ghost distances
        food_weight = 1.3
        ghost_weight = 1.0

        # set variables to old info
        oldPos = currentGameState.getPacmanPosition()
        oldFood = currentGameState.getFood()
        oldGhostStates = currentGameState.getGhostStates()

        # check if the action leads to a win and if so, return infinity, meaning definitely take this action
        if len(newFoodList) == 0:
            return float('inf')

        # calculate the distance to the closest ghost for old and new positions
        # return the diff
        closestGhostDistanceBefore = min(manhattanDistance(oldPos, ghost.getPosition()) for ghost in oldGhostStates)
        closestGhostDistanceNow = min(manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates)
        ghostDistanceDiff = closestGhostDistanceBefore - closestGhostDistanceNow

        # check if action leads to ghost immediate periphery, which will lead to losing state
        # return minus infinity if so, meaning definitely avoid this
        if newScaredTimes[0] == 0 and closestGhostDistanceNow <= 1:
            return float('-inf')

        # if ghost isnt scared and is close, avoid it
        if (newScaredTimes[0] == 0) and (closestGhostDistanceNow < 3):
            ghost_weight = 1.5
            score = successorGameState.getScore() - ghost_weight * ghostDistanceDiff
            return score

        # calculate the distance to the closest food for old and new positions
        # return the diff
        closestFoodDistanceBefore = min([manhattanDistance(oldPos, food) for food in oldFood.asList()])
        closestFoodDistanceNow = min([manhattanDistance(newPos, food) for food in newFoodList])
        foodDistanceDiff = closestFoodDistanceBefore - closestFoodDistanceNow

        # if this action is eating a pellet, the food distance will increase suddenly
        # the diff will be negative so set it to 0 so that pacman doesnt avoid eating if the next nearest food is far away
        if len(newFoodList) < len(oldFood.asList()):
            foodDistanceDiff = 0

        # if ghost is scared, ignore it and focus on food
        if newScaredTimes[0] > 0:
            score = successorGameState.getScore() + food_weight * foodDistanceDiff
            return score

        # set score
        score = successorGameState.getScore() + food_weight * foodDistanceDiff - ghost_weight * ghostDistanceDiff
        return score

        "*** MY CODE HERE ***"

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** MY CODE HERE ***"
        # help func used for recursion, keeping depth and agentIndex parameters
        def minimax_helper(state, depth, agentIndex):

            # if at base case, return evaluation values
            if depth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            # else: someone has to move, pacman or ghost
            if agentIndex == 0: # pacman moves

                # get possible successor states and return the max of what the help func returns
                # when called on each successor state, agentIndex set to 1 so that the ghost moves next
                legal_actions = state.getLegalActions(agentIndex)
                successor_states = [state.generateSuccessor(agentIndex, action) for action in legal_actions]
                return max(minimax_helper(successor, depth, 1) for successor in successor_states)

            if agentIndex > 0: # ghost moves

                # get possible successor states and return the min of what the help func returns
                # when called on each successor state, agentIndex set to next ghost or pacman if
                # all ghosts have moved in which case we increment the depth
                legal_actions = state.getLegalActions(agentIndex)
                successor_states = [state.generateSuccessor(agentIndex, action) for action in legal_actions]
                next_agent_index = (agentIndex + 1) % state.getNumAgents()
                next_depth = depth + 1 if next_agent_index == 0 else depth
                return min(minimax_helper(successor, next_depth, next_agent_index) for successor in successor_states)

        # get legal actions for pacman wherever he is when getAction is called
        # call minimax_helper on the successor states
        # return the action that leads to best value
        best_action = None
        best_value = float('-inf')
        for action in gameState.getLegalActions(0):
            successor_state = gameState.generateSuccessor(0, action)

            # pacman here has moved already (in minimax, not in game), so next up is the first ghost, agentIndex = 1
            # a round hasnt been completed yet though, so depth is still 0
            value = minimax_helper(successor_state, 0, 1)

            if value > best_value:
                best_value = value
                best_action = action
        return best_action
        "*** MY CODE HERE ***"

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** MY CODE HERE ***"
        def alpha_beta_helper(state, depth, agentIndex, alpha, beta):

            # base case, return evaluation values
            if depth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            # pacman (max player)
            if agentIndex == 0:

                # set value to minus infinity so that
                # its replaced by the first value returned by the helper func
                value = float('-inf')
                for action in state.getLegalActions(agentIndex):
                    successor_state = state.generateSuccessor(agentIndex, action)
                    value = max(value, alpha_beta_helper(successor_state, depth, 1, alpha, beta))

                    # if value is greater than beta, 
                    # then pacman (max player) when called as a successor state of a ghost (min player)
                    # will never be picked, since the ghost above already has a lower option (beta), so we prune it
                    if value > beta:
                        return value

                    # no prune, so keep checking the remaining children, update alpha to the best value pacman has seen so far
                    alpha = max(alpha, value)
                return value

            # ghost (min player)
            else:
                # next agent is the next ghost, or pacman if all ghosts have moved
                # in which case the round is done and we increment the depth
                next_agent_index = (agentIndex + 1) % state.getNumAgents()
                next_depth = depth + 1 if next_agent_index == 0 else depth

                value = float('inf')
                for action in state.getLegalActions(agentIndex):
                    successor_state = state.generateSuccessor(agentIndex, action)
                    value = min(value, alpha_beta_helper(successor_state, next_depth, next_agent_index, alpha, beta))

                    #if value is less than alpha,
                    # then the nearest pacman (max player) above already has a better option,
                    # so this branch will never be picked to be expanded, so we prune it
                    if value < alpha:
                        return value

                    # no prune, so keep checking the remaining children, update beta to the best value ghost has seen so far
                    beta = min(beta, value)
                return value

        # get legal actions for pacman wherever he is when getAction is called
        # call alpha_beta_helper on the successor states
        # return the action that leads to best value
        # the root never prunes, there is no ghost above it, it only updates alpha
        best_action = None
        alpha = float('-inf')
        beta = float('inf')
        for action in gameState.getLegalActions(0):
            successor_state = gameState.generateSuccessor(0, action)

            # pacman has moved already (in minimax, not in game), so next up is the first ghost, agentIndex = 1
            # a round hasnt been completed yet, so depth is still 0
            value = alpha_beta_helper(successor_state, 0, 1, alpha, beta)

            # update alpha to the best value so far, this picks the best action and also lets the next actions prune
            if value > alpha:
                alpha = value
                best_action = action
        return best_action

        "*** MY CODE HERE ***"

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** MY CODE HERE ***"
        # help func used for recursion, keeping depth and agentIndex parameters
        def expectimax_helper(state, depth, agentIndex):

            # if at base case, return evaluation values
            if depth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            # else: someone has to move, pacman or ghost
            if agentIndex == 0: # pacman moves

                # get possible successor states and return the max of what the help func returns
                # when called on each successor state, agentIndex set to 1 so that the ghost moves next
                legal_actions = state.getLegalActions(agentIndex)
                successor_states = [state.generateSuccessor(agentIndex, action) for action in legal_actions]
                return max(expectimax_helper(successor, depth, 1) for successor in successor_states)

            if agentIndex > 0: # ghost moves

                # get possible successor states and return the average of what the help func returns
                # when called on each successor state, agentIndex set to next ghost or pacman if
                # all ghosts have moved in which case we increment the depth
                legal_actions = state.getLegalActions(agentIndex)
                successor_states = [state.generateSuccessor(agentIndex, action) for action in legal_actions]
                next_agent_index = (agentIndex + 1) % state.getNumAgents()
                next_depth = depth + 1 if next_agent_index == 0 else depth
                return sum(expectimax_helper(successor, next_depth, next_agent_index) for successor in successor_states) / len(successor_states)

        # get legal actions for pacman wherever he is when getAction is called
        # call expectimax_helper on the successor states
        # return the action that leads to best value
        best_action = None
        best_value = float('-inf')
        for action in gameState.getLegalActions(0):
            successor_state = gameState.generateSuccessor(0, action)

            # pacman here has moved already (in expectimax, not in game), so next up is the first ghost, agentIndex = 1
            # a round hasnt been completed yet though, so depth is still 0
            value = expectimax_helper(successor_state, 0, 1)

            if value > best_value:
                best_value = value
                best_action = action
        return best_action
        "*** MY CODE HERE ***"

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
