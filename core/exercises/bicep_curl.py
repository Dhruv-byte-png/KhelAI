class BicepCurlAnanlyzer:

    def __init__(self):
        self.extended_threshold = 160
        self.contracted_threshold = 90

        self.previous_state = "UNKNOWN"
        self.reps = 0

    def get_state(self, elbow_angle):
        if elbow_angle is None:
            return "UNKNOWN"

        print("Elbow angle:", elbow_angle)

        if elbow_angle >= self.extended_threshold:
            return "EXTENDED"

        if elbow_angle <= self.contracted_threshold:
            return "CONTRACTED"

        return "MOVING"

    def update(self, elbow_angle):
        current_state = self.get_state(elbow_angle)

        #count a rep when the arm goes: 
        #EXTENDED -> CONTRACTED -> EXTENDED

        if(
            self.previous_state == "CONTRACTED"
            and current_state == "EXTENDED"
        ):
            self.reps += 1

        if current_state != "UNKNOWN":
            self.previous_state = current_state

        return current_state, self.reps

if __name__ == "__main__":

    analyzer = BicepCurlAnanlyzer()

    test_angles = [
        140,   #extended
        120,   #moving
        90,    #contracted
        100,   #moving
        140    #extended -> 1 rep
    ]

    for angle in test_angles:
        state, reps = analyzer.update(angle)
        print(
            f"Angle: {angle} | "
            f"State: {state} | "
            f"Reps: {reps}"
        )