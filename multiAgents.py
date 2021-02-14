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
import random
import util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        for ghost in successorGameState.getGhostPositions():    # avoid ghosts if they are nearby
            if (manhattanDistance(newPos, ghost) < 2):
                return float('-inf')

        if action == Directions.STOP:   # avoid stopping
            return float('-inf')

        dots = successorGameState.getFood().asList()
        closestFood = float("inf")
        for dot in dots:
            closestFood = min(closestFood, manhattanDistance(newPos, dot))  # focus on eating the clossest dot

        # closer to a dot the bigger value we return
        return successorGameState.getScore() + 1/closestFood


def scoreEvaluationFunction(currentGameState):
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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
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
        "*** YOUR CODE HERE ***"
        def MinMax(gameState, agentIndex, depth): # the turn will go pacman the first ghosts the second ghost and then again pacman
            legalActions = gameState.getLegalActions(agentIndex)    # take the actions
            numberOfGhosts = gameState.getNumAgents() - 1           # take the number of ghosts
            bestAction = None
            bestValue = None

            if ((depth == self.depth) or gameState.isLose() or gameState.isWin()):
                bestValue = self.evaluationFunction(gameState)
                return bestValue, bestAction

            # here we check who will be the next player turn
            # we start from pacman
            # and then to every ghost
            # and then back to pacman
            if agentIndex == numberOfGhosts:    # if it is the last ghost
                depth += 1                      # increase the depth
                nextTurn = 0                    # and make the turn go to the pacman
            else:
                nextTurn = agentIndex + 1       # make the turn go to the next ghost

            if agentIndex != 0:  # --- minimazing player == ghosts ---

                bestValue = float("inf")  # start with a very big number
                for legalAction in legalActions:  # for every action we have
                    successors = gameState.generateSuccessor(agentIndex, legalAction)  # get the successors
                    newMinValue = MinMax(successors, nextTurn, depth)[0]    # get values of the next ghost or pacman
                    if newMinValue < bestValue:   # change our variables if needed
                        bestValue = newMinValue
                        bestAction = legalAction

            else:               # --- maximazing player == pacman ---

                bestValue = float("-inf")  # start with a very small number
                for legalAction in legalActions:  # for every action we have
                    successorGameState = gameState.generateSuccessor(agentIndex, legalAction)  # get the successors
                    newMaxValue = MinMax(successorGameState, nextTurn, depth)[0]  # get values of the first ghost
                    if newMaxValue > bestValue:    # change our variables if needed
                        bestValue = newMaxValue
                        bestAction = legalAction
            return bestValue, bestAction     # return the best value with the best action

        # depth = 0 and agentIndex = 0 = pacman
        return MinMax(gameState, 0, 0)[1]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # AlphaBeta is the same with MiniMax but we will not check nodes that it doesnt need to be checked beacuse we already have a better option before
        def AlphaBeta(gameState, agentIndex, depth, alpha, beta): # the turn will go pacman the first ghosts the second ghost and then again pacman
            legalActions = gameState.getLegalActions(agentIndex)    # take the actions
            numberOfGhosts = gameState.getNumAgents() - 1           # take the number of ghosts
            bestAction = None
            bestValue = None

            if ((depth == self.depth) or gameState.isLose() or gameState.isWin()):
                bestValue = self.evaluationFunction(gameState)
                return bestValue, bestAction

            # here we check who will be the next player turn
            # we start from pacman
            # and then to every ghost
            # and then back to pacman
            if agentIndex == numberOfGhosts:    # if it is the last ghost
                depth += 1                      # increase the depth
                nextTurn = 0                    # and make the turn go to the pacman
            else:
                nextTurn = agentIndex + 1       # make the turn go to the next ghost

            if agentIndex != 0:  # --- minimazing player == ghosts ---

                bestValue = float("inf")  # start with a very big number
                for legalAction in legalActions:  # for every action we have
                    successors = gameState.generateSuccessor(agentIndex, legalAction)  # get the successors
                    newMinValue = AlphaBeta(successors, nextTurn, depth, alpha, beta)[0]  # get values of the next ghost or pacman
                    if newMinValue < bestValue:   # change our variables if needed
                        bestValue = newMinValue
                        bestAction = legalAction
                    # --- new code added ---
                    if newMinValue < beta:      # change our beta if needed
                        beta = newMinValue
                    if beta < alpha:            # if beta is smaller than alpha means that earlier the parent node had better options so we break
                        break
                    # --- new code added ---
            else:               # --- maximazing player == pacman ---

                bestValue = float("-inf")  # start with a very small number
                for legalAction in legalActions:  # for every action we have
                    successorGameState = gameState.generateSuccessor(agentIndex, legalAction)  # get the successors
                    newMaxValue = AlphaBeta(successorGameState, nextTurn, depth, alpha, beta)[0]  # get values of the first ghost
                    if newMaxValue > bestValue:    # change our variables if needed
                        bestValue = newMaxValue
                        bestAction = legalAction
                    # --- new code added ---
                    if newMaxValue > alpha:      # change our alpha if needed
                        alpha = newMaxValue
                    if beta < alpha:            # if beta is smaller than alpha means that earlier the parent node had better options so we break
                        break
                    # --- new code added ---
            return bestValue, bestAction     # return the best value with the best action

        # depth = 0, agentIndex = 0 = pacman, a = -00, b = +00
        return AlphaBeta(gameState, self.index, 0,float("-inf"), float("inf"))[1]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        # Expectimax is the same with Minimax but min player is not always doing the corrrect decision
        # so there is a probability to choose every option and it doesnt take the min
        def Expectimax(gameState, agentIndex, depth): # the turn will go pacman the first ghosts the second ghost and then again pacman
            legalActions = gameState.getLegalActions(agentIndex)    # take the actions
            numberOfGhosts = gameState.getNumAgents() - 1           # take the number of ghosts
            bestAction = None
            bestValue = None

            if ((depth == self.depth) or gameState.isLose() or gameState.isWin()):
                bestValue = self.evaluationFunction(gameState)
                return bestValue, bestAction

            # here we check who will be the next player turn
            # we start from pacman
            # and then to every ghost
            # and then back to pacman
            if agentIndex == numberOfGhosts:    # if it is the last ghost
                depth += 1                      # increase the depth
                nextTurn = 0                    # and make the turn go to the pacman
            else:
                nextTurn = agentIndex + 1       # make the turn go to the next ghost

            if agentIndex != 0:  # --- minimazing player == ghosts ---

                bestValue = 0  # start with 0
                for legalAction in legalActions:  # for every action we have
                    successors = gameState.generateSuccessor(agentIndex, legalAction)  # get the successors
                    # calculate as if there are equal probabilities for all the actions to be picked: 1/len(legalActions)
                    bestValue = bestValue + Expectimax(successors, nextTurn, depth)[0] / len(legalActions)
                
            else:               # --- maximazing player == pacman ---

                bestValue = float("-inf")  # start with a very small number
                for legalAction in legalActions:  # for every action we have
                    successorGameState = gameState.generateSuccessor(
                        agentIndex, legalAction)  # get the successors
                    newMaxValue = Expectimax(successorGameState, nextTurn, depth)[
                        0]  # get values of the first ghost
                    if newMaxValue > bestValue:    # change our variables if needed
                        bestValue = newMaxValue
                        bestAction = legalAction
            return bestValue, bestAction     # return the best value with the best action

        # depth = 0 and agentIndex = 0 = pacman
        return Expectimax(gameState, 0, 0)[1]


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isWin():    # if we won return something very big to end
        return float("inf")
    if currentGameState.isLose():
        return float("-inf")    # if we lost return something very small to end

    # we will take in consideration many aspects
    # like how many capsules are left
    # how far is the scared ghosts if there are any
    # how many dots are there left to be eaten

    pacmanPosition = currentGameState.getPacmanPosition()
    ghosts = currentGameState.getGhostStates()
    dots = currentGameState.getFood()
    capsules = currentGameState.getCapsules()

    # find the closest dot
    dotsDistanceList = []
    for dot in dots.asList():
        dotsDistanceList += [manhattanDistance(dot, pacmanPosition)]
    minDotDistance = min(dotsDistanceList)

    # from all the ghosts find the closest that is hunting us and the closest that is scared and we can eat
    hunterGhostsDistanceList = []
    scaredGhostsDistanceList = []
    for ghost in ghosts:
        if ghost.scaredTimer == 0:  # if it is not scared we added in the hunting list
            hunterGhostsDistanceList += [manhattanDistance(pacmanPosition, ghost.getPosition())]
        elif ghost.scaredTimer > 0:  # if it is scared we added in the scared list
            scaredGhostsDistanceList += [manhattanDistance(pacmanPosition, ghost.getPosition())]
            
    minHunter = -1
    if len(hunterGhostsDistanceList) > 0:
        minHunter = min(hunterGhostsDistanceList)
    
    minScared = -1
    if len(scaredGhostsDistanceList) > 0:
        minScared = min(scaredGhostsDistanceList)

    # we give more value to the capsules
    # cause when pacman eats a capsule it is safe for some time
    return scoreEvaluationFunction(currentGameState) -1.5*len(ghosts)*(1/minHunter) -len(ghosts)*minScared -150*len(capsules) -1.5*len(dots.asList()) -1.5*minDotDistance


# Abbreviation
better = betterEvaluationFunction
