from translator import translate_to_javascript
import ast

python_code = """
x = 5 + 3
for i in range(3):
    print(x, i)
"""

tree = ast.parse(python_code)
result = translate_to_javascript(tree)
print(result)
