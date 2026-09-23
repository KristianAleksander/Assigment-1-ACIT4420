from models import Participant, ReferenceMeasurements, Observation, TrainingSession
from utils import print_session_result
from data_generator import available_scenarios, generate_fitness_data

def run_generated_scenario(scenario):

    profile, generated_observations = generate_fitness_data(
        participant_id="P001",
        scenario=scenario,
        seed=42,
        number_of_windows=10
    )

    reference = ReferenceMeasurements(
        resting_heart_rate=profile["baseline_heart_rate"],
        normal_skin_response=profile["baseline_skin_response"],
        normal_temperature=profile["baseline_temperature"]
    )

    participant = Participant(
        name="Generated participant",
        id=profile["participant_id"],
        age=26,
        reference_measurements=reference
    )

    session = TrainingSession(participant)

    for data in generated_observations:
        observation = Observation(
            timestamp=data["timestamp"],
            heart_rate=data["heart_rate"],
            skin_response=data["skin_response"],
            temperature=data["temperature"],
            activity_level=data["activity_level"],
            signal_quality=data["signal_quality"]
        )

        session.addObservation(observation)

    print_session_result(scenario, session)

def main():
    reference = ReferenceMeasurements(60, 2.5, 33.0)
    participant = Participant(
        name="Ole",
        id=1,
        age=26,
        reference_measurements=reference
    )
    #1. resting session
    resting_session = TrainingSession(participant)

    resting_session.addObservation(
        Observation(1, 65, 2.5, 32.9, 0.10, 0.93)
    )
    resting_session.addObservation(
        Observation(2, 67, 2.4, 33.0, 0.12, 0.95)
    )
    resting_session.addObservation(
        Observation(3, 66, 2.5, 32.9, 0.08, 0.94)
    )
    print_session_result(
        title="Resting session",
        session=resting_session
    )

    # 2. Moderate activity
    moderate_session = TrainingSession(participant)
    moderate_session.addObservation(
        Observation(1, 100, 3.0, 34.0, 0.40, 0.94)
    )

    moderate_session.addObservation(
        Observation(2, 105, 3.2, 34.2, 0.45, 0.95)
    )
    moderate_session.addObservation(
        Observation(3, 110, 3.3, 34.3, 0.50, 0.96)
    )

    print_session_result("Moderate activity", moderate_session)

    # 3. High activity
    high_session = TrainingSession(participant)
    high_session.addObservation(
        Observation(1, 150, 4.0, 35.0, 0.80, 0.95)
    )
    high_session.addObservation(
        Observation(2, 160, 4.2, 35.2, 0.85, 0.94)
    )
    high_session.addObservation(
        Observation(3, 170, 4.4, 35.4, 0.90, 0.93)
    )

    print_session_result("High activity", high_session)

    # 4. Activity followed by recovery
    recovery_session = TrainingSession(participant)
    recovery_session.addObservation(
        Observation(1, 170, 4.5, 35.5, 0.90, 0.95)
    )
    recovery_session.addObservation(
        Observation(2, 145, 4.0, 35.0, 0.65, 0.95)
    )
    recovery_session.addObservation(
        Observation(3, 115, 3.5, 34.5, 0.35, 0.94)
    )

    print_session_result("Recovery session", recovery_session)

    # 5. Invalid sensor data
    invalid_session = TrainingSession(participant)

    invalid_session.addObservation(
        Observation(1, 500, 2.5, 33.0, 0.20, 0.95)
    )
    invalid_session.addObservation(
        Observation(2, 100, 2.5, 60.0, 0.30, 0.95)
    )
    invalid_session.addObservation(
        Observation(3, 100, 2.5, 33.0, 1.50, 0.95)
    )

    print_session_result("Invalid sensor data", invalid_session)

    print("\n=== Generated data ===")

    for scenario in available_scenarios():
        run_generated_scenario(scenario)

if __name__ == "__main__":
    main()