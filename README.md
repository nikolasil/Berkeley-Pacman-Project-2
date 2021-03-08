# This project was made during my studies in UOA University and especially for the course Artificial Intelligence 1.

---

[Project 2: Multi-Agent Search](https://inst.eecs.berkeley.edu/~cs188/sp19/project2.html)

> **Run command:** python ./autograder.py
> There are comments all over my code if there is something that i didn't covered here.

## Question 1 - Reflex Agent

The logic is:
- avoid all ghosts
- not to stop moving because it wastes time unnecessarily
- and finally be rewarded with what a greater return if it is close to
food

---

## Question 2 – Minimax

I have constructed a function inside getAction (self, gameState) named MINMAX (gameState, agentIndex, depth) so I can
call only through getAction.
Because we don't just have 1 ghost for the MIN but
many, the turns will like like these [pacman-> ghost1-> ghost2… -> ghostn-> pacman]
Where all the ghosts are MIN, pacman MAX and playing first.

The algorithm is:
- every time we enter the function we check to
find out who the next player will be, a ghost or a pacman
- call MINMAX for his kids [just do +1 at Index of unless we are the last ghost we want to call
pacman with index 0.]

About Minimax:
- MIN: Just for each children node we call the function recursively
to get their price [after we return it to the last level
evaluation function] and we get the min of the children.

- MAX: Same as MIN but we get the children's max.

---

## Question 3 – AlphaBeta Pruning

The algorithm is the same as Minimax in question 2. But AlphaBeta
is more efficient because it does not checks all Nodes.
Our function is called AlphaBeta (gameState, agentIndex, depth, alpha, beta).
And every time we check for each child of a node we look to see if the
parent node had a better choice before. If it did, it means it will prune.
We achieve this with the variables alpha, beta.
Alpha holds the highest value and beta the lowest.

Example: When we are the MIN and we look at our children nodes we check with alpha
made by the father.

---

## Question 4 – Expectimax

The algorithm is the same as Minimax in question 2. Only Expectimax
is not with optimal MIN.
Our function is called Expectimax (gameState, agentIndex, depth).
Here our MIN does not always choose the best option for him, that is
min. But it can choose any option whether it is bad or good.
So we can say that there is an equal chance to choose any
from its options so the value of this node will be equal to the sum
of children's prices on the probability of choosing it.
[probability = 1 / number of children]

---

## Question 5 – Evaluation Function

Here like question 1 we try to make the pacman win but
without knowing the action he will take.
We will use many factors help pacman go well.
The most important I think are the capsules because for some time
ghosts do not threaten us and pacman can eat dots undisturbed
[for this the remaining capsules have a weight of 150].
Other than that we care about the closest dot, the closest scared ghost
but also hunter ghost and of course how many dots we have left to win.
