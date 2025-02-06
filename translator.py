import ast
import openai

def normalize_ast(ast_tree):
    """
    Normalizes the AST to a universal representation.
    For now, this function will simply return the original AST.
    """
    return ast_tree


def translate_ast_to_language(ast_tree, target_language):
    """
    Translates the normalized AST into a specific target language.
    """
    if target_language == "JavaScript":
        return translate_to_javascript(ast_tree)
    # else if target_language == "C++":
    #     return f"// Translation to {target_language} is not implemented yet."
    # else if target_language == "Java":
    #     return f"// Translation to {target_language} is not implemented yet."
    else:
        return f"// Translation to {target_language} is not implemented yet."



def translate_to_javascript(ast_tree):
    """
    Translate the AST to JavaScript code.
    """
    javascript_code = []

    # Traverse the AST and handle specific node types
    for node in ast_tree.body:
        if isinstance(node, ast.Assign):
            # Handle variable assignment
            target = node.targets[0].id  # Variable name
            value = translate_expr(node.value)  # Translate the value
            javascript_code.append(f"let {target} = {value};")
        
        elif isinstance(node, ast.ClassDef):  # Handle class definitions
            class_name = node.name
            javascript_code.append(f"class {class_name} {{")  # Start JavaScript class
            constructor_found = False  # Track if an `__init__` method is found

            for class_body_node in node.body:
                if isinstance(class_body_node, ast.FunctionDef):
                    method_name = class_body_node.name
                    params = ", ".join(arg.arg for arg in class_body_node.args.args if arg.arg != "self")

                    # Convert __init__ to a JavaScript constructor
                    if method_name == "__init__":
                        method_name = "constructor"
                        constructor_found = True
                    
                    # Convert Python method to JavaScript method
                    javascript_code.append(f"    {method_name}({params}) {{")
                    
                    for stmt in class_body_node.body:
                        javascript_code.append(f"        {translate_stmt(stmt)}")  # Indent method body
                    
                    javascript_code.append("    }")  # Close method

            if not constructor_found:
                javascript_code.append("    constructor() {}")  # Add an empty constructor if none exists
            
            javascript_code.append("}")  # Close class definition

        elif isinstance(node, ast.For):  # Handle Nested For Loops
            target = node.target.id
            iter_func = node.iter.func.id if isinstance(node.iter, ast.Call) else None
            iter_args = [translate_expr(arg) for arg in node.iter.args] if iter_func else []
            if iter_func == "range":
                start = iter_args[0] if len(iter_args) > 1 else "0"
                stop = iter_args[1] if len(iter_args) > 1 else iter_args[0]
                javascript_code.append(f"for (let {target} = {start}; {target} < {stop}; {target}++) {{")
                for body_node in node.body:
                    body_code = translate_stmt(body_node)
                    if not body_code.endswith(";"):  # Ensure correct semicolon usage
                        body_code += ";"
                    javascript_code.append("    " + body_code)
                javascript_code.append("}")

        elif isinstance(node, ast.Expr):
            # Handle expression (e.g., function call)
            expr_code = translate_expr(node.value)
            if expr_code and not expr_code.endswith(";"):  # Ensure only one semicolon
                expr_code += ";"
            javascript_code.append(expr_code)

        elif isinstance(node, ast.If):  # Handle Nested If-Else
            javascript_code.append(translate_if_else(node, 0))

        elif isinstance(node, ast.While):
            # Translate the condition
            test = translate_expr(node.test)
            javascript_code.append(f"while ({test}) {{")

            # Translate the loop body
            for body_node in node.body:
                if isinstance(body_node, ast.Expr):
                    javascript_code.append("    " + translate_expr(body_node.value) + ";")
                elif isinstance(body_node, ast.Assign):
                    target = body_node.targets[0].id
                    value = translate_expr(body_node.value)
                    javascript_code.append(f"    {target} = {value};")
                elif isinstance(body_node, ast.AugAssign):  # Handle x -= 1 as x--
                    target = body_node.target.id
                    op = translate_operator(body_node.op)
                    value = translate_expr(body_node.value)
                    if value == "1" and op == "-":  # If it's x -= 1, convert to x--
                        javascript_code.append(f"    {target}--;")
                    elif value == "1" and op == "+":  # If it's x += 1, convert to x++
                        javascript_code.append(f"    {target}++;")
                    else:
                        javascript_code.append(f"    {target} {op}= {value};")

            javascript_code.append("}")

        elif isinstance(node, ast.FunctionDef):
            # Handle function definitions
            func_name = node.name
            args = ", ".join(arg.arg for arg in node.args.args)  # Get function arguments
            javascript_code.append(f"function {func_name}({args}) {{")
            for body_node in node.body:
                javascript_code.append("    " + translate_expr(body_node.value))
            javascript_code.append("}")

    return "\n".join(javascript_code)


def translate_expr(node):
    """
    Translate a Python AST expression node to JavaScript.
    """
    if isinstance(node, ast.BinOp):
        # Handle binary operations (e.g., 5 + 3)
        left = translate_expr(node.left)
        right = translate_expr(node.right)
        op = translate_operator(node.op)
        return f"{left} {op} {right}"
    
    elif isinstance(node, ast.List):  # Lists
        elements = ", ".join(translate_expr(el) for el in node.elts)
        return f"[{elements}]"

    elif isinstance(node, ast.Dict):  # Dictionaries
        pairs = ", ".join(f"{translate_expr(k)}: {translate_expr(v)}" for k, v in zip(node.keys, node.values))
        return f"{{{pairs}}}"
    
    elif isinstance(node, ast.Compare):
        left = translate_expr(node.left)
        comparators = [translate_expr(comp) for comp in node.comparators]
        operator = translate_operator(node.ops[0])  # Handle comparison operator
        return f"{left} {operator} {comparators[0]}"
    
    elif isinstance(node, ast.Constant):  # Handle numbers, strings, booleans
        if isinstance(node.value, str):
            # Case 1: If both single and double quotes exist, use double quotes and escape existing double quotes
            if "'" in node.value and '"' in node.value:
                return '"' + node.value.replace('"', '\\"') + '"'

            # Case 2: If the original string was wrapped in single quotes, use single quotes
            elif node.value.startswith("'") and node.value.endswith("'"):
                return f"'{node.value}'"

            # Case 3: If the original string was wrapped in double quotes, use double quotes
            else:
                return f'"{node.value}"'
        
        return repr(node.value)
        
    
    elif isinstance(node, ast.Name):
        # Handle variable names
        return node.id
    
    elif isinstance(node, ast.Call):
        # Handle function calls
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            args = ", ".join(translate_expr(arg) for arg in node.args)
            return f"console.log({args})"
    

    return "// Unsupported expression"


def translate_operator(op):
    """
    Translate Python operators to JavaScript.
    """
    if isinstance(op, ast.Add):
        return "+"
    elif isinstance(op, ast.Sub):
        return "-"
    elif isinstance(op, ast.Mult):
        return "*"
    elif isinstance(op, ast.Div):
        return "/"
    elif isinstance(op, ast.Gt):
        return ">"
    elif isinstance(op, ast.Lt):
        return "<"
    elif isinstance(op, ast.Eq):
        return "=="
    elif isinstance(op, ast.NotEq):
        return "!="
    elif isinstance(op, ast.GtE):
        return ">="
    elif isinstance(op, ast.LtE):
        return "<="
    elif isinstance(op, ast.And):
        return "&&"
    elif isinstance(op, ast.Or):
        return "||"
    elif isinstance(op, ast.AugAssign):  # Handle +=, -=, *=, /=
        return op.__class__.__name__.replace("Assign", "")
    return "// Unsupported operator"

#handling nested if-else blocks
def translate_if_else(node, indent_level=0):
    """
    Recursively translate nested if-else statements with proper indentation.
    """
    indent = "    " * indent_level  # Ensure consistent indentation
    js_code = [f"{indent}if ({translate_expr(node.test)}) {{"]

    # Translate the if-block
    for body_node in node.body:
        if isinstance(body_node, ast.If):  # Handle nested if
            js_code.append(translate_if_else(body_node, indent_level + 1))
        else:
            js_code.append(f"{indent}    {translate_stmt(body_node)}")  # Proper indentation

    if node.orelse:
        js_code.append(f"{indent}}} else {{")  # Ensure correct closing and indentation
        for orelse_node in node.orelse:
            if isinstance(orelse_node, ast.If):  # Handle nested elif
                js_code.append(translate_if_else(orelse_node, indent_level + 1))
            else:
                js_code.append(f"{indent}    {translate_stmt(orelse_node)}")

    js_code.append(f"{indent}}}")  # Close the if-else block
    return "\n".join(js_code)


def translate_stmt(node):
    """
    Translate statements inside loops and if-else blocks.
    """
    if isinstance(node, ast.Assign):
        target = translate_expr(node.targets[0])
        value = translate_expr(node.value)
        return f"let {target} = {value};"
    
    elif isinstance(node, ast.Expr):
        return translate_expr(node.value) + ";"
    
    elif isinstance(node, ast.AugAssign):  # Handle +=, -= inside loops
        target = node.target.id
        op = translate_operator(node.op)
        value = translate_expr(node.value)
        if value == "1" and op == "-":
            return f"{target}--;"
        elif value == "1" and op == "+":
            return f"{target}++;"
        else:
            return f"{target} {op}= {value};"
        
    elif isinstance(node, ast.If):  # Fix for nested if inside loops
        return translate_if_else(node, 1)
    
    elif isinstance(node, ast.Return):
        return f"return {translate_expr(node.value)};"

    elif isinstance(node, ast.Attribute):  # Handle self.attribute in classes
        if isinstance(node.value, ast.Name) and node.value.id == "self":
            return f"this.{node.attr}"  # Convert `self.attr` to `this.attr`
        return f"{translate_expr(node.value)}.{node.attr}"

    elif isinstance(node, ast.FunctionDef):
        return f"function {node.name}() {{}}"
    
    return "// Unsupported statement"
