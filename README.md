## Genetic Algorithm for Picobot Directions 
This was my final class project for Introduction to Computer Science at Harvey Mudd College.
[Picobot](https://www.cs.hmc.edu/picobot/) is a digital roomba-like robot that wants to cover all tiles of its digital room. 
You can feed Picobot instructions such as "if you hit a wall on your right, turn south". 
I created a genetic algorithm that randomly generates some sets of rules for Picobot to follow. Then this program runs them on a simulated picobot world and calculates the effectiveness (i.e. how much of the room Picobot has covered after many steps). It then selects the most effective sets of rules from this group, mutating and combining them into a new generation of rules. After roughly 9 generations, these rules are 99% effective at covering the entire room.
