import ast
from translator import normalize_ast, translate_ast_to_language
from generator import generate_code_from_ast


def translate_code(code, target_language):
    """
    Translates Python code into a specified target language.
    """
    try:
        # Step 1: Parse the code into an AST
        tree = ast.parse(code)

        # Step 2: Normalize the AST
        normalized_ast = normalize_ast(tree)

        # Step 3: Translate the normalized AST
        translated_code = translate_ast_to_language(normalized_ast, target_language)

        # # Step 4: Generate target code
        # generated_code = generate_code_from_ast(translated_code, target_language)

        # return generated_code
        return translated_code

    except SyntaxError as e:
        return f"Syntax Error in the source code: {e}"


if __name__ == "__main__":
    # Example Python code to translate
    python_code = """
x = 5 + 3
for i in range(3):
    print(x, i)
"""

    # Translate to JavaScript
    target_lang = "JavaScript"
    result = translate_code(python_code, target_lang)

    print(f"\nTranslated Code to {target_lang}:\n")
    print(result)
