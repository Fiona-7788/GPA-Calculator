"""
GPA Calculator Module
=====================
This module provides tools for calculating and tracking GPA.
It includes a helper function for grade conversion and a Student
class for managing course records, computing GPA, simulating
future grades, visualizing grades, and saving/loading data.
"""

import json
import matplotlib.pyplot as plt

# Grade scale lookup dictionary
GRADE_SCALE = {
    "A+": 4.0, "A": 4.0, "A-": 3.7,
    "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7,
    "D+": 1.3, "D": 1.0, "D-": 0.7,
    "F": 0.0
}

def letter_to_points(letter):
    """
    Convert a letter grade to grade points.

    Parameters
    ----------
    letter : str
        A letter grade string (e.g. 'A', 'B+', 'C-').

    Returns
    -------
    float
        The corresponding grade point value.

    Raises
    ------
    ValueError
        If the letter grade is not recognized.

    Examples
    --------
    >>> letter_to_points('A')
    4.0
    >>> letter_to_points('B+')
    3.3
    """
    # Convert to uppercase to handle lowercase input
    letter = letter.strip().upper()

    if letter not in GRADE_SCALE:
        raise ValueError(
            f"'{letter}' is not a valid grade. "
            f"Valid grades: {list(GRADE_SCALE.keys())}"
        )

    return GRADE_SCALE[letter]

class Student:
    """
    Represents a student with a record of courses and grades.

    Attributes
    ----------
    name : str
        The student's name.
    courses : list of dict
        A list of course records, each containing course name,
        letter grade, grade points, and units.

    Examples
    --------
    >>> s = Student('Alex')
    >>> s.add_course('COGS 18', 'A', 4)
    >>> s.get_gpa()
    4.0
    """

    def __init__(self, name):
        """
        Initialize a Student with a name and empty course list.

        Parameters
        ----------
        name : str
            The student's name.
        """
        self.name = name
        self.courses = []

    def add_course(self, course_name, letter_grade, units):
        """
        Add a course to the student's record.

        Parameters
        ----------
        course_name : str
            The name of the course (e.g. 'COGS 18').
        letter_grade : str
            The letter grade received (e.g. 'A-', 'B+').
        units : int
            The number of credit units for the course.

        Raises
        ------
        ValueError
            If the letter grade is invalid or units is not positive.

        Examples
        --------
        >>> s = Student('Alex')
        >>> s.add_course('COGS 18', 'A', 4)
        >>> len(s.courses)
        1
        """
        if units <= 0:
            raise ValueError("Units must be a positive number.")

        # Convert letter grade to points (raises ValueError if invalid)
        points = letter_to_points(letter_grade)

        course = {
            "name": course_name,
            "grade": letter_grade.strip().upper(),
            "points": points,
            "units": units
        }

        self.courses.append(course)

    def get_gpa(self):
        """
        Calculate and return the student's cumulative GPA.

        Uses weighted average: sum(points * units) / sum(units).

        Returns
        -------
        float
            The cumulative GPA rounded to 2 decimal places.
            Returns 0.0 if no courses have been added.

        Examples
        --------
        >>> s = Student('Alex')
        >>> s.add_course('COGS 18', 'A', 4)
        >>> s.add_course('MATH 20A', 'B+', 4)
        >>> s.get_gpa()
        3.65
        """
        if not self.courses:
            return 0.0

        total_points = sum(c["points"] * c["units"] for c in self.courses)
        total_units = sum(c["units"] for c in self.courses)

        return round(total_points / total_units, 2)

    def what_if(self, letter_grade, units):
        """
        Simulate GPA if a hypothetical future course were added.

        Does NOT permanently add the course to the student's record.

        Parameters
        ----------
        letter_grade : str
            The hypothetical letter grade (e.g. 'A', 'B-').
        units : int
            The number of credit units for the hypothetical course.

        Returns
        -------
        float
            The simulated GPA rounded to 2 decimal places.

        Raises
        ------
        ValueError
            If the letter grade is invalid or units is not positive.

        Examples
        --------
        >>> s = Student('Alex')
        >>> s.add_course('COGS 18', 'A', 4)
        >>> s.what_if('B', 4)
        3.5
        """
        if units <= 0:
            raise ValueError("Units must be a positive number.")

        new_points = letter_to_points(letter_grade)

        # Include existing courses in the simulation
        total_points = sum(c["points"] * c["units"] for c in self.courses)
        total_points += new_points * units

        total_units = sum(c["units"] for c in self.courses) + units

        return round(total_points / total_units, 2)

    def display_transcript(self):
        """
        Print a formatted transcript of all courses and current GPA.

        Displays course name, letter grade, and units for each course,
        followed by the cumulative GPA.

        Examples
        --------
        >>> s = Student('Alex')
        >>> s.add_course('COGS 18', 'A', 4)
        >>> s.display_transcript()
        Student: Alex
        ----------------------------------------
        Course               Grade    Units
        ----------------------------------------
        COGS 18              A        4
        ----------------------------------------
        Cumulative GPA: 4.0
        """
        print(f"Student: {self.name}")
        print("-" * 40)
        print(f"{'Course':<20} {'Grade':<8} {'Units'}")
        print("-" * 40)

        for course in self.courses:
            print(
                f"{course['name']:<20} "
                f"{course['grade']:<8} "
                f"{course['units']}"
            )

        print("-" * 40)
        print(f"Cumulative GPA: {self.get_gpa()}")

    def plot_grades(self):
        """
        Display a bar chart of grade points per course with a GPA line.

        Uses matplotlib to create a bar chart where each bar represents
        a course's grade points. A horizontal dashed red line marks the
        student's current cumulative GPA.

        Notes
        -----
        Requires matplotlib to be installed.
        Will display nothing if no courses have been added.

        Examples
        --------
        >>> s = Student('Alex')
        >>> s.add_course('COGS 18', 'A', 4)
        >>> s.plot_grades()
        """
        if not self.courses:
            print("No courses to plot.")
            return

        course_names = [c["name"] for c in self.courses]
        grade_points = [c["points"] for c in self.courses]
        gpa = self.get_gpa()

        fig, ax = plt.subplots(figsize=(8, 5))

        # Plot bars
        bars = ax.bar(
            course_names,
            grade_points,
            color="steelblue",
            edgecolor="white",
            width=0.5
        )

        # Add GPA reference line
        ax.axhline(
            y=gpa,
            color="red",
            linestyle="--",
            linewidth=1.5,
            label=f"GPA: {gpa}"
        )

        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + 0.05,
                str(height),
                ha="center",
                va="bottom",
                fontsize=10
            )

        ax.set_ylim(0, 4.5)
        ax.set_xlabel("Course")
        ax.set_ylabel("Grade Points")
        ax.set_title(f"{self.name}'s Grade Chart")
        ax.legend()

        plt.tight_layout()
        plt.show()

    def save(self, filename):
        """
        Save the student's data to a JSON file.

        Parameters
        ----------
        filename : str
            The path/name of the file to save to (e.g. 'alex.json').

        Examples
        --------
        >>> s = Student('Alex')
        >>> s.add_course('COGS 18', 'A', 4)
        >>> s.save('alex.json')
        Saved to alex.json
        """
        data = {
            "name": self.name,
            "courses": self.courses
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Saved to {filename}")

    def load(self, filename):
        """
        Load student data from a JSON file.

        Replaces the current name and courses with data from the file.

        Parameters
        ----------
        filename : str
            The path/name of the JSON file to load from.

        Raises
        ------
        FileNotFoundError
            If the specified file does not exist.

        Examples
        --------
        >>> s = Student('')
        >>> s.load('alex.json')
        Loaded from alex.json
        """
        with open(filename, "r") as f:
            data = json.load(f)

        self.name = data["name"]
        self.courses = data["courses"]

        print(f"Loaded from {filename}")