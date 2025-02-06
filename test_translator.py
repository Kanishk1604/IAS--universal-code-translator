import unittest
from translator import translate_ast_to_language, translate_to_javascript
import ast


class TestTranslator(unittest.TestCase):



    def translate_code(self, code):
        """
        Utility function to parse Python code and pass the AST to the translator.
        """
        tree = ast.parse(code)
        return translate_ast_to_language(tree, "JavaScript")

    def test_nested_if_else(self):
        python_code = """
if x > 0:
    if x > 10:
        print("Large")
    else:
        print("Small")
else:
    print("Negative")
"""
        expected_js = """
if (x > 0) {
    if (x > 10) {
        console.log("Large");
    } else {
        console.log("Small");
    }
} else {
    console.log("Negative");
}
"""
        result = self.translate_code(python_code)
        self.assertEqual(result.strip(), expected_js.strip())




    def test_while_loop_translation(self):
        python_code = """
x = 5
while x > 0:
    x -= 1
"""
        expected_js = """
let x = 5;
while (x > 0) {
    x--;
}
"""
        result = self.translate_code(python_code)
        self.assertEqual(result.strip(), expected_js.strip())

    def test_variable_assignment(self):
        """
        Test translating variable assignments.
        """
        python_code = "x = 10"
        expected_js = "let x = 10;"
        self.assertEqual(self.translate_code(python_code), expected_js)

    def test_binary_operation(self):
        """
        Test translating binary operations (e.g., addition).
        """
        python_code = "x = 5 + 3"
        expected_js = "let x = 5 + 3;"
        self.assertEqual(self.translate_code(python_code), expected_js)

    def test_for_loop_with_range(self):
        """
        Test translating a for loop with range().
        """
        python_code = """
for i in range(3):
    print(i)
"""
        expected_js = (
            "for (let i = 0; i < 3; i++) {\n"
            "    console.log(i);\n"
            "}"
        )
        self.assertEqual(self.translate_code(python_code), expected_js)

    def test_for_loop_with_start_and_stop(self):
        """
        Test translating a for loop with range(start, stop).
        """
        python_code = """
for i in range(1, 5):
    print(i)
"""
        expected_js = (
            "for (let i = 1; i < 5; i++) {\n"
            "    console.log(i);\n"
            "}"
        )
        self.assertEqual(self.translate_code(python_code), expected_js)

    def test_function_call(self):
        """
        Test translating a function call (e.g., print()).
        """
         # Case 1: Default single quotes
        python_code = "print('Hello, World!')"
        expected_js = """console.log("Hello, World!");"""  # Use single quotes here
        result = self.translate_code(python_code)
        self.assertEqual(result.strip(), expected_js.strip())

        # Case 2: String that contains a single quote should use double quotes
        python_code = """print("It's a beautiful day!")"""
        expected_js = """console.log("It's a beautiful day!");"""  # Double quotes because of the apostrophe
        result = self.translate_code(python_code)
        self.assertEqual(result.strip(), expected_js.strip())

        # Case 3: String with both single and double quotes
        python_code = """print('He said, "Hello, World!"')"""
        expected_js = """console.log("He said, "Hello, World!"");"""  # Double quotes with escaped quotes
        result = self.translate_code(python_code)
        self.assertEqual(result.strip(), expected_js.strip())

#     def test_class_translation(self):
#         python_code = """
# class Person:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age

#     def greet(self):
#         print(f"Hello, my name is {self.name} and I am {self.age} years old.")
# """
#         expected_js = """
# class Person {
#     constructor(name, age) {
#         this.name = name;
#         this.age = age;
#     }

#     greet() {
#         console.log(`Hello, my name is ${this.name} and I am ${this.age} years old.`);
#     }
# }
# """
#         result = self.translate_code(python_code)
#         self.assertEqual(result.strip(), expected_js.strip())
if __name__ == "__main__":
    unittest.main()
