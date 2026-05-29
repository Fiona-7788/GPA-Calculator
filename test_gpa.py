"""
Tests for GPA Calculator Module
================================
Unit tests for letter_to_points() and the Student class methods.
Run with: python -m unittest test_gpa.py
"""

import unittest
from gpa_module import letter_to_points, Student


class TestLetterToPoints(unittest.TestCase):
    """Tests for the letter_to_points() helper function."""

    def test_a_grade(self):
        """Test that 'A' returns 4.0."""
        self.assertEqual(letter_to_points("A"), 4.0)

    def test_a_minus(self):
        """Test that 'A-' returns 3.7."""
        self.assertEqual(letter_to_points("A-"), 3.7)

    def test_b_plus(self):
        """Test that 'B+' returns 3.3."""
        self.assertEqual(letter_to_points("B+"), 3.3)

    def test_f_grade(self):
        """Test that 'F' returns 0.0."""
        self.assertEqual(letter_to_points("F"), 0.0)

    def test_lowercase_input(self):
        """Test that lowercase input is handled correctly."""
        self.assertEqual(letter_to_points("a"), 4.0)

    def test_invalid_grade_raises_error(self):
        """Test that an invalid grade raises a ValueError."""
        with self.assertRaises(ValueError):
            letter_to_points("Z")

    def test_invalid_number_raises_error(self):
        """Test that a number string raises a ValueError."""
        with self.assertRaises(ValueError):
            letter_to_points("4.0")


class TestStudentAddCourse(unittest.TestCase):
    """Tests for the Student.add_course() method."""

    def setUp(self):
        """Set up a fresh Student before each test."""
        self.student = Student("Alex")

    def test_add_one_course(self):
        """Test that adding a course increases course count."""
        self.student.add_course("COGS 18", "A", 4)
        self.assertEqual(len(self.student.courses), 1)

    def test_course_stored_correctly(self):
        """Test that course data is stored correctly."""
        self.student.add_course("COGS 18", "A", 4)
        course = self.student.courses[0]
        self.assertEqual(course["name"], "COGS 18")
        self.assertEqual(course["grade"], "A")
        self.assertEqual(course["points"], 4.0)
        self.assertEqual(course["units"], 4)

    def test_add_multiple_courses(self):
        """Test adding multiple courses."""
        self.student.add_course("COGS 18", "A", 4)
        self.student.add_course("MATH 20A", "B+", 4)
        self.assertEqual(len(self.student.courses), 2)

    def test_invalid_units_raises_error(self):
        """Test that zero or negative units raises ValueError."""
        with self.assertRaises(ValueError):
            self.student.add_course("COGS 18", "A", 0)

    def test_invalid_grade_raises_error(self):
        """Test that an invalid grade raises ValueError."""
        with self.assertRaises(ValueError):
            self.student.add_course("COGS 18", "Z", 4)


class TestStudentGetGPA(unittest.TestCase):
    """Tests for the Student.get_gpa() method."""

    def setUp(self):
        """Set up a fresh Student before each test."""
        self.student = Student("Alex")

    def test_empty_courses_returns_zero(self):
        """Test that GPA is 0.0 when no courses added."""
        self.assertEqual(self.student.get_gpa(), 0.0)

    def test_perfect_gpa(self):
        """Test GPA when all grades are A."""
        self.student.add_course("COGS 18", "A", 4)
        self.student.add_course("MATH 20A", "A", 4)
        self.assertEqual(self.student.get_gpa(), 4.0)

    def test_mixed_gpa(self):
        """Test GPA with mixed grades."""
        self.student.add_course("COGS 18", "A", 4)
        self.student.add_course("MATH 20A", "B+", 4)
        # (4.0*4 + 3.3*4) / 8 = 3.65
        self.assertEqual(self.student.get_gpa(), 3.65)

    def test_weighted_gpa(self):
        """Test that GPA is correctly weighted by units."""
        self.student.add_course("COGS 18", "A", 4)
        self.student.add_course("MATH 20A", "C", 2)
        # (4.0*4 + 2.0*2) / 6 = 20/6 = 3.33
        self.assertEqual(self.student.get_gpa(), 3.33)

    def test_failing_grade(self):
        """Test GPA with an F grade."""
        self.student.add_course("COGS 18", "F", 4)
        self.assertEqual(self.student.get_gpa(), 0.0)


class TestStudentWhatIf(unittest.TestCase):
    """Tests for the Student.what_if() method."""

    def setUp(self):
        """Set up a Student with one course before each test."""
        self.student = Student("Alex")
        self.student.add_course("COGS 18", "A", 4)

    def test_what_if_does_not_add_course(self):
        """Test that what_if does not permanently add a course."""
        self.student.what_if("B", 4)
        self.assertEqual(len(self.student.courses), 1)

    def test_what_if_better_grade_raises_gpa(self):
        """Test that a better hypothetical grade raises GPA."""
        self.student.add_course("MATH 20A", "B", 4)
        current = self.student.get_gpa()
        simulated = self.student.what_if("A", 4)
        self.assertGreater(simulated, current)

    def test_what_if_worse_grade_lowers_gpa(self):
        """Test that a worse hypothetical grade lowers GPA."""
        current = self.student.get_gpa()
        simulated = self.student.what_if("C", 4)
        self.assertLess(simulated, current)

    def test_what_if_same_grade_keeps_gpa(self):
        """Test that the same hypothetical grade keeps GPA stable."""
        current = self.student.get_gpa()
        simulated = self.student.what_if("A", 4)
        self.assertEqual(simulated, current)

    def test_what_if_invalid_units(self):
        """Test that invalid units raises ValueError."""
        with self.assertRaises(ValueError):
            self.student.what_if("A", -1)


class TestStudentSaveLoad(unittest.TestCase):
    """Tests for the Student.save() and Student.load() methods."""

    def setUp(self):
        """Set up a Student with courses before each test."""
        self.student = Student("Alex")
        self.student.add_course("COGS 18", "A", 4)
        self.student.add_course("MATH 20A", "B+", 4)
        self.filename = "test_save.json"

    def tearDown(self):
        """Remove test JSON file after each test."""
        import os
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_save_creates_file(self):
        """Test that save() creates a JSON file."""
        import os
        self.student.save(self.filename)
        self.assertTrue(os.path.exists(self.filename))

    def test_load_restores_name(self):
        """Test that load() restores the student's name."""
        self.student.save(self.filename)
        new_student = Student("")
        new_student.load(self.filename)
        self.assertEqual(new_student.name, "Alex")

    def test_load_restores_courses(self):
        """Test that load() restores all courses."""
        self.student.save(self.filename)
        new_student = Student("")
        new_student.load(self.filename)
        self.assertEqual(len(new_student.courses), 2)

    def test_load_restores_gpa(self):
        """Test that GPA is same after save and load."""
        original_gpa = self.student.get_gpa()
        self.student.save(self.filename)
        new_student = Student("")
        new_student.load(self.filename)
        self.assertEqual(new_student.get_gpa(), original_gpa)

    def test_load_missing_file_raises_error(self):
        """Test that loading a nonexistent file raises FileNotFoundError."""
        new_student = Student("")
        with self.assertRaises(FileNotFoundError):
            new_student.load("nonexistent.json")


if __name__ == "__main__":
    unittest.main()


                 
    