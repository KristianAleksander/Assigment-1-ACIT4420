# Python OOP Assignment Starter Files

This package contains starter data generators for both assignment choices.

- `option_a_fitness/`: Smart Fitness Session Analyzer
- `option_b_podcast/`: Podcast Voice and Recording Analyzer

Students should copy only the folder corresponding to their selected option into
their own GitHub repository. The supplied generator returns ordinary Python
dictionaries and lists. It does not perform the required analysis.

Run an example from the package root:

```bash
python3 option_a_fitness/example_usage.py
python3 option_b_podcast/example_usage.py
```

The generator files may be treated as instructor-supplied code. Students should
not modify them unless the assignment explicitly permits modification.

## Option A – Design choices

The application uses composition instead of inheritance because the classes
represent different objects rather than specialized versions of the same object.

A `Participant` has `ReferenceMeasurements`, and a `TrainingSession` has a
`Participant` and a list of `Observation` objects. These are “has-a”
relationships, so composition is more suitable than inheritance.