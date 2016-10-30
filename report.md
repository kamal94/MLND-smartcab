Kamal Kamalaldin
10/29/2016
Udacity MLND program
Smartcab project

###Project Report
This report is provided to answer all questions that are posed by the smartcab implementation. The questions are listed in order of implementation, and the answer is provided after each question.

# Question 1
#### Observe what you see with the agent's behavior as it takes random actions. Does the smartcab eventually make it to the destination? Are there any other interesting observations to note?
With the random choice implementation, the smartcab takes a very long time to reach the destination, and has no particular strategy as to how to reach it. The smartcab seems to go opposite to the direction of the waypoint at times, which is not an optimal behavior.

#Question 2
#### What states have you identified that are appropriate for modeling the smartcab and environment? Why do you believe each of these states to be appropriate for this problem?
I identified the following the be important aspects of the state, and added reasons for why so:
1. Oncoming: This part of the state tells the cab if there are oncoming cars in traffic. This state variabel could inform the car's decision when facing a trafic light that has an oncoming car. If a car is oncoming, then the car should make a different decision from when there is no oncoming car.

2. 
        self.state = {'deadline': deadline, 'oncoming': inputs['oncoming'], \
        'light': inputs['light'], 'right':inputs['right'], 'left':inputs['left']}