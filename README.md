# KingChessBot
The bot made for grey-meter uni-commerce hackathon. It won the 1st price with a great lead.

## Rules of the Game
 1. There is a board game played between two players. The board has nXn equal squares, where 8 <= n <= 15  (similar to a chess board).
 2. Only two kings will be placed on the board at the starting of the game (one at 1,1 and second at n,n position).
 3. The kings can move one square in any direction - up, down, to the sides, and diagonally, just like chess.
 4. Each square can be visited at-most once by either of the kings.
 5. The king who gets killed, or is out of moves loses the game.

## What we had to do
 1. You need to write a bot, which can play the game on your behalf. And expose this bot as a webservice.
 2. Your webservice should run on port 8080 and expose three APIs:

|URL   | Type | Parameter | Sample Response | Purpose |
|------|------|-----------|-----------------|-----------|
|/ping |  GET | --        | {ok: true}      | To let us know that your bot server is alive |
|/start|  GET | y,o,g     | {ok: true}      | For you to initialize the round. Here **y** would indicate position of your king (eg: 1\|1), **o** indicates position of opponent’s king (eg: n\|n), and **g** indicates size of the grid. |
|/play |  GET | m         | {m:"1\|2"}      | **m** : Move made by your opponent. Your response would convey your next move.|

*Note: By convention all positions are represented as x\|y where x and y are respective coordinates on the board. Bottom left board is 1\|1.*



## Our Algorithm
The bot picks up a strategy of being offensive while making sure that its next move will not lead to it's death or to a deadend.
It first assigns ranks to all the neighboring 8 nodes, one by one, with the following rules:<br/>
 1. If the opponent bot is present on the node - it assignes the rank 0, meaning the best position.
 2. If the opponent is 1 place from the next node, then it assigns the rank of 999, i.e. INF, meaning the losing or worst position.
 3. if any of the 2 conditions is not satisfied, it then counts the no of exit points from the node and assigns it to a variable say no_of_exits. And checks on that variable.
  1. If no_of_exits >= 3, it assigns rank 1.
  2. If no_of_exits == 2, it assigns rank 2.
  3. If no_of_exits == 1, it assigns rank 3.
  4. If no_of_exits == 0, it assigns rank 9999999, meaning the forbidden position i.e. out of bounds or already visited. <br\>*Note: that it is greater than the losing position, so that it does not choose wall on defeat and accepts it's defeat.*

The bot then sorts all the neighboring nodes on the basis of its direction from the opponent. Taking an example:
If we are at 2,2 , and the opponent is at say 10,10 the sorted list would be:<br/>
**[ [3,3], [2,3], [3,2], [1,3], [3,1], [1,2], [2,1], [1,1] ]** <br/>
It then chooses the first node with the lowest rank to be the optimal node for the next move. This ensures that it is going towards the opponent seeming that it would play offensive by following it where ever it goes but would wait for the opponent to make a mistake, rather than attacking it, and would easily back-off when it feels its in danger, or an odd distance is not maintained with the opponent. <br\>
##The code
The main algorithm code is in */bot server/bot/views.py*, and is enclosed with marking comments.
