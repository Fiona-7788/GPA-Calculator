"""Script to run the GPA Calculator."""

# Imports
from gpa_module import Student, letter_to_points

# Create a student object
student = Student("Alex")

# Add courses
student.add_course("COGS 18", "A", 4)
student.add_course("MATH 20A", "B+", 4)
student.add_course("WCWP 10A", "A-", 4)
student.add_course("COGS 9", "B+", 4)

# Display transcript and GPA
student.display_transcript()

# Run what-if simulations
print(f"What if I get an A in a 4-unit course? GPA: {student.what_if('A', 4)}")
print(f"What if I get a C in a 4-unit course? GPA: {student.what_if('C', 4)}")

# Plot grades
student.plot_grades()

# Save to file
student.save("alex.json")