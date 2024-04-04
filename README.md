## Genetic Algorithm for Picobot Directions 
This was my final class project for Introduction to Computer Science at Harvey Mudd College.

[Picobot](https://www.cs.hmc.edu/picobot/) is a digital roomba-like robot that wants to cover all tiles of its digital room. 

You can feed Picobot instructions such as "if you hit a wall on your right, turn south". 

I created a genetic algorithm that randomly generates some sets of rules for Picobot to follow. Then each set of rules is applied to Picobot in my simulated Picobot world and calculates the effectiveness (i.e. how much of the room Picobot has covered after many steps). We select the most effective sets of rules from this group, and mutate and combine them into a new generation of sets of rules. After roughly 9 generations, all sets of rules are 99% effective at covering the entire room.
