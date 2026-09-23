def calculate_summary(values):
    if len(values) == 0:
        return None
    #returns average, minimun or maximum for a list of values
    return { 
        "average": sum(values) / len(values),
        "minimum": min(values),
        "maximum": max(values)
    }

#checks if a sensor value is a number before calculations
def is_number(value):
    return isinstance(value, (int, float))

#Convers a summary dictionary into readable text
def format_summary(name, summary):
    if summary is None:
        return f"{name}: no usable data"

    return (
        f"{name}: average={summary['average']:.2f}, "
        f"minimum={summary['minimum']}, "
        f"maximum={summary['maximum']}"
    )

#Prints a readable report containing the session classification and summary
def print_session_result(title, session):
    result = session.classifySession()

    print(f"\n--- {title} ---")
    print("Participant:", session.participant.name)
    print("Classification:", result["classification"])
    print("Usable observations:", result["usable_observations"])
    print("Explanation:", result["explanation"])

    heart_rate_summary = session.calculateHeartRateSummary()
    print(format_summary("Heart rate", heart_rate_summary))