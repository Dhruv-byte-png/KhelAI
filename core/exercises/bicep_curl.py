from collections import deque
class BicepCurlAnanlyzer:

    def __init__(self):
        self.extended_threshold = 130
        self.contracted_threshold = 100

        #smoothing
        self.angle_history = deque(maxlen=5)

        #Rep Counting
        self.phase = "UNKNOWN"
        self.reps = 0

    def smooth_angle(self, angle):
        if angle is None:
            return None

        self.angle_history.append(angle)

        return sum(self.angle_history)/ len(self.angle_history)

    def get_state(self, elbow_angle):
        if elbow_angle is None:
            return "UNKNOWN"

        if elbow_angle >= self.extended_threshold:
            return "EXTENDED"

        if elbow_angle <= self.contracted_threshold:
            return "CONTRACTED"

        return "MOVING"

    def update_rep(self, elbow_angle):

        #count a rep when the arm goes: 
        #EXTENDED -> CONTRACTED -> EXTENDED -> +1 rep

        if elbow_angle is None:
            return "UNKOWN" , self.reps

        state = self.get_state(elbow_angle)

        #Start the cycle only when the arm is extended
        if self.phase == "UNKNOWN":
            if state == "EXTENDED":
                self.phase = "EXTENDED"

        #Arm was extended and is now contracted
        elif self.phase == "EXTENDED":
            if state == "CONTRACTED":
                self.phase = "CONTRACTED"

        #Arm was contracted and returned to extended
        elif self.phase == "CONTRACTED":
            if state == "EXTENDED":
                self.reps += 1
                self.phase = "EXTENDED"

        return state, self.reps

if __name__ == "__main__":

    analyzer = BicepCurlAnanlyzer()

    test_angles = [
        150,   #extended
        140,   
        110,   #moving
        90,    #contracted
        80,
        100,
        120,   #moving
        140,    #extended -> rep
        150
    ]

    for angle in test_angles:
        state, reps = analyzer.update_rep(angle)
        print(
            f"Angle: {angle} | "
            f"State: {state} | "
            f"Reps: {reps}"
        )