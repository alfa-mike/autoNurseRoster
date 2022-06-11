`# autoNurseRoster`

## Automatic nurse rostering system 

Designed a model to automate the nurse scheduling problem (hospital that requires a timetable specifying the work shifts for nurses over a specified period of time) 
Formulated the given problem into CSP and implemented a model for automatically generating rosters, meeting the given requirements of hospital and preferences of nurses, using constraint-satisfaction techniques.
Additionally, extended the above model to facilitate the meeting of soft constraint like preference of nurses.


## Implementatation
* `variables` = V_\{i,j} (this refers to nurse no. i on day j)
* `value domain` = {M,E,A,R}  ( morning shift, evening shift, afternoon shift and rest respectively). /
Used recursive backtracking in this assignment to find out the correct assignment of values to the variables.

##### function `Rec_backtrack()` 
This functions recursively assigns values to variables and checks for consistency in the 1st part of the assignment. Whenever, it finds inconsistency, it backtracks and assigns different values to the variables which don’t fall consistent with the constraints. When it finds a assignment which follows all constraints, it returns the assignment.

##### function `Rec_backtrack2()`
This function is analogous to the previous functions and is used in the optimization part of the assignment. The only difference between the two is that rec_backtrack2 does not return the immediate assignment it finds. It stores all the assignments and returns the best assignment that has more weightage.


## Optimization
In this part, optimized the solution in order to get the best possible solution. optimization techniques are:

##### function `select_UV()`
This function decides which unassigned variables is to be selected next and given a value prior to other variables. In this, we have chosen the nurse with smallest “j” (here j refers to the day number). By doing this, we can schedule the nurse day by day which would increase the efficiency of our solution.

##### function `select_VAL()`
This function assign the values to the unassigned variables. So, to assign, firstly give highest priority to “R” if “R” is not assigned to that variable on that week. Then if “R” is already assigned in that week, give highest priority according to the order {“M”, “A”, “E”} which ever is not assigned in that order.

##### function `select_VAL2()`
This functions assigns the values to variables in the optimization part of the assignment. This function is quite similar to the previous one. Only change that occurs here is that if the nurse is a special nurse, then the domains “M” and “E” are given more priority than the other domains.
