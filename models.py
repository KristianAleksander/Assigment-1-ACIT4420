from utils import calculate_summary, is_number

class Participant:
    def __init__(self,name,id,age, reference_measurements):
        self.name = name
        self.id = id
        self.age = age
        self.reference_measurements = reference_measurements

class ReferenceMeasurements:
    def __init__(self, resting_heart_rate, normal_skin_response,normal_temperature):
        self.resting_heart_rate = resting_heart_rate
        self.normal_skin_response = normal_skin_response
        self.normal_temperature = normal_temperature

class Observation: 
    def __init__(self,timestamp, heart_rate, skin_response, temperature, activity_level, signal_quality):
        self.timestamp = timestamp
        self.heart_rate = heart_rate
        self.skin_response = skin_response
        self.temperature = temperature
        self.activity_level = activity_level
        self.signal_quality = signal_quality

    #Checks if a value is within the accepted range
    @staticmethod
    def valueInRange(value, minimum, maximum):
        return (
            value is not None
            and minimum <= value <= maximum
        )
    #Checks if all observations are valid
    def isValid(self):
        return (
            isinstance(self.timestamp, int)
            and self.timestamp >= 0
            and is_number(self.heart_rate)
            and Observation.valueInRange(self.heart_rate, 35, 205)
            and self.skin_response is not None
            and self.skin_response >= 0
            and Observation.valueInRange(self.temperature, 25, 42)
            and Observation.valueInRange(self.activity_level, 0, 1)
            and Observation.valueInRange(self.signal_quality, 0, 1)
        )

    def __str__(self):
        return (f"Time: {self.timestamp},"
            f"Heart rate: {self.heart_rate}"
            f"Skin response {self.skin_response}"
            f"Temperature {self.temperature}"
            f"Activity: {self.activity_level}"
            f"Signal quality: {self.signal_quality}"
            )
        
class TrainingSession: 
    #Groups and analyses observations belonging to one participant
    def __init__(self, participant):
        self.participant = participant
        self._observations = []

    @property
    def observations(self):
        return self._observations
    #Adds an observation if it contains valid values
    def addObservation(self, observation):
        if(observation.isValid()):
            self._observations.append(observation)
            return True
        return False
    #Calculate average, minimum and maximum heart rate
    def calculateHeartRateSummary(self):
        if len(self._observations) == 0:
            return None

        heartRates = []

        for observation in self._observations: 
            heartRates.append(observation.heart_rate)

        return calculate_summary(heartRates)
    #Calculate average, minimum and maximum activity level
    def calculateActivityLevel(self):
        if(len(self._observations)) == 0:
            return None
        
        activityLevels = []     

        for observation in self._observations:
            activityLevels.append(observation.activity_level)    

        return calculate_summary(activityLevels)
    
    #Calculate average, minimum and maximum temperature  
    def calculateTemperature(self):
        if(len(self._observations)) == 0:
            return None

        temperatures = []

        for observation in self._observations:
            temperatures.append(observation.temperature)

        return calculate_summary(temperatures)

    #Compares the session average with the participant's reference values
    def compareMeasurements(self):
        heartRateSummary = self.calculateHeartRateSummary()
        temperatureSummary = self.calculateTemperature()

        if heartRateSummary is None or temperatureSummary is None:
            return None

        reference = self.participant.reference_measurements

        return { 
            "heart_rate": {
                "average": heartRateSummary["average"],
                "reference": reference.resting_heart_rate,
                "difference": (heartRateSummary["average"] - reference.resting_heart_rate)
            },
            "temperature": {
                "average": temperatureSummary["average"],
                "Reference": reference.normal_temperature,
                "difference": (temperatureSummary["average"] - reference.normal_temperature)
            },
        }
    #Checks if heart rate and activity declines during the session
    def isRecovering(self):
    
        if len(self._observations) < 3:
            return False

    # For a short session, compare the first and last observation.
        if len(self._observations) == 3:
            first = self._observations[0]
            last = self._observations[-1]

            return (
                first.heart_rate - last.heart_rate >= 10
                and first.activity_level - last.activity_level >= 0.1
            )

        # For a longer session, compare the beginning with the end.
        first_three = self._observations[:3]
        last_three = self._observations[-3:]

        starting_heart_rate = sum(observation.heart_rate for observation in first_three) / len(first_three)

        ending_heart_rate = sum(observation.heart_rate for observation in last_three) / len(last_three)

        starting_activity = sum(observation.activity_level for observation in first_three) / len(first_three)

        ending_activity = sum(
            observation.activity_level for observation in last_three) / len(last_three)

        return starting_heart_rate - ending_heart_rate >= 10 and starting_activity - ending_activity >= 0.1
    
    #Classifies the session and returns a structured result
    def classifySession(self):
        usable = len(self._observations)

        if usable < 3:
            return {
                "classification": "insufficient data",
                "usable_observations": usable,
                "explanation": "At least three usable observations are requred"
            }
        if self.isRecovering():
            return {
            "classification": "recovering",
            "usable_observations": usable,
            "explanation": "Heart rate and activity decline near the end"
        }

        heart_rate_summary = self.calculateHeartRateSummary()
        activity_summary = self.calculateActivityLevel()

        average_heart_rate = heart_rate_summary["average"]
        average_activity = activity_summary["average"]
        resting_heart_rate = self.participant.reference_measurements.resting_heart_rate

        if average_activity < 0.2 and average_heart_rate <= resting_heart_rate + 15:
            classification = "resting"
            explanation = "Activity is low and hearrt rate is close to resting heart rate"

        elif(
            average_activity < 0.7 and average_heart_rate <= resting_heart_rate + 70
        ):
            classification = "moderate activity"
            explanation = "Activity and heart rate are moderate"

        else:
            classification = "high activity"
            explanation = "Activity or heart rate is high"

        return {
            "classification": classification,
            "usable_observations": usable, 
            "explanation": explanation
        }
        