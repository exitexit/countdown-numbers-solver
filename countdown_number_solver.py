#!/usr/bin/env python3
#
# Copyright 2020 Tao Xie
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


OPTIMIZE = 1

input = []
target = 0
unique_solutions = {}

# Handle input.
# Example: countdown_number_solver.solve([100, 25, 8, 3, 1, 1], 984)

def solve(arg_input, arg_target):
    input.clear()
    for num in arg_input:
        assert num >= 1
        input.append(num)
    # Sort the list so that duplicate numbers are grouped together.
    input.sort(reverse=True)

    global target
    assert arg_target > 0
    target = arg_target

    unique_solutions.clear()
    place_operators()

    for solution_str in unique_solutions:
        print(solution_str)
    print('Total: ' + str(len(unique_solutions)) + ' solutions.')


# Combine permuted numbers with arithmetic operations.
# Only simple binary operators of '+', '-', 'x', and '/' are allowed.

stack = []
record = []
masks = []

def place_operators():
    stack.clear()
    record.clear()

    masks.clear()
    masks.extend([0] * len(input))

    recursive_place_operators(0)

def recursive_place_operators(num_consumed):

    # Check result.
    global target
    if len(stack) == 1 and stack[0] == target:
        solution = contruct_solution_string(record)
        unique_solutions[solution] = num_consumed
        return

    # Push another number on the stack.
    count = len(input)
    if num_consumed < count:
        zero_count = 0
        index = 0
        while index < count:
            if masks[index] != 0:
                index += 1
                continue
            zero_count += 1
            num = input[index]
            next_index = index + 1

            # In case of repeated numbers in the original input, only allow one order.
            if index + 1 < count and num == input[index + 1]:
                for i in range(index + 1, count):
                    if input[i] == num:
                        assert masks[i] == 0
                    else:
                        next_index = i
                        break

            masks[index] = 1
            stack.append(num)
            record.append(num)

            recursive_place_operators(num_consumed + 1)

            stack.pop()
            record.pop()
            masks[index] = 0

            if num_consumed + zero_count == count:
                break
            index = next_index

    # Enumerate operators.
    if len(stack) > 1:
        num1 = stack.pop()
        num2 = stack.pop()

        # Addition
        if num2 >= num1:  # Avoid duplicates for commutative operations.
            stack.append(num2 + num1)
            record.append('+')

            recursive_place_operators(num_consumed)

            stack.pop()
            record.pop()

        # Subtraction
        if num2 > num1:  # Negative numbers are not allowed and
                         # exclude the trivial case of A - A = 0.
            stack.append(num2 - num1)
            record.append('-')

            recursive_place_operators(num_consumed)

            stack.pop()
            record.pop()

        # Multiplication
        if num2 >= num1 and num1 != 1:  # Avoid duplicates for commutative operations and
                                        # exclude the trivial case of A x 1 = A.
            stack.append(num2 * num1)
            record.append('x')

            recursive_place_operators(num_consumed)

            stack.pop()
            record.pop()

        # Division
        if num2 >= num1 and num1 != 1 and num2 % num1 == 0:  # Fractions are not allowed and 
                                                             # exclude the trivial case of A / 1 = A.
            stack.append(int(num2 / num1))
            record.append('/')

            recursive_place_operators(num_consumed)

            stack.pop()
            record.pop()


        stack.append(num2)
        stack.append(num1)



# Optimize operation tree.

class Operation:
    value = 0
    operator = None
    children = None

    negative = False
    reciprocal = False

    expression = None

    def __init__(self, value, operator = None, left = None, right = None):
        self.value = value
        self.operator = operator
        self.children = []

        if left is not None:
            self.children.append(left)
        if right is not None:
            self.children.append(right)

    def __str__(self):
        return self.expression

    def negate(self):
        self.negative = not self.negative

        if self.operator == '+':
            for child in self.children:
                child.negate()
            self.compile_expression()

    def reciprocate(self):
        self.reciprocal = not self.reciprocal

        if self.operator == 'x':
            for child in self.children:
                child.reciprocate()
            self.compile_expression()

    def compile_expression(self):
        if self.operator is None:
            self.expression = str(self.value)
        
        elif self.operator == '+':
            assert len(self.children) > 1
            sort_children(self.children)
            expression = None
            for child in self.children:
                if expression is None:
                    sign = '- ' if child.negative else ''
                    expression = sign + child.expression
                else:
                    sign = ' - ' if child.negative else ' + '
                    expression = expression + sign + child.expression
            self.expression = expression

        elif self.operator == '-':
            assert False

        elif self.operator == 'x':
            assert len(self.children) > 1
            sort_children(self.children)
            expression = None
            for child in self.children:
                child_exp = child.expression
                if child.operator == '+' or child.operator == '-':
                    child_exp = '( ' + child_exp + ' )'
                if expression is None:
                    sign = '/ ' if child.reciprocal else ''
                    expression = sign + child_exp
                else:
                    sign = ' / ' if child.reciprocal else ' x '
                    expression = expression + sign + child_exp
            self.expression = expression

        elif self.operator == '/':
            assert False

        else:
            assert False

def sort_children(children):
    count = len(children)
    for i in range(count):
        for j in range(i + 1, count):
            if compare_operations_less_than(children[i], children[j]):
                temp = children[i]
                children[i] = children[j]
                children[j] = temp

def compare_operations_less_than(op1, op2):
    # positive > negative
    if op1.negative != op2.negative:
        return op1.negative
    # integer > fraction
    if op1.reciprocal != op2.reciprocal:
        return op1.reciprocal
    # multiplication or division > addition or subtraction
    if (op1.operator == 'x' or op1.operator == '/') != (op2.operator == 'x' or op2.operator == '/'):
        return not (op1.operator == 'x' or op1.operator == '/')
    # expression > number
    if (op1.operator is None) != (op2.operator is None):
        return op1.operator is None
    # bigger value > smaller value
    if op1.value != op2.value:
        return op1.value < op2.value
    # longer string > shorter string
    if len(op1.expression) != len(op2.expression):
        return len(op1.expression) < len(op2.expression)
    # text comparison
    return op1.expression < op2.expression



execution = []

def contruct_solution_string(ops_record):
    root = construct_operation_tree(ops_record)

    global OPTIMIZE
    if OPTIMIZE:
        recursive_optimize_operation_tree(root)
    else:
        recursive_print_binary_operation_tree(root)

    return root.expression

def construct_operation_tree(ops_record):
    execution.clear()

    for item in ops_record:
        if isinstance(item, int):
            execution.append(Operation(item))
            continue

        value = 0

        rr = execution.pop()
        ll = execution.pop()

        if item == '+':
            value = ll.value + rr.value
        elif item == '-':
            value = ll.value - rr.value
        elif item == 'x':
            value = ll.value * rr.value
        elif item == '/':
            assert rr.value != 0 and ll.value % rr.value == 0
            value = int(ll.value / rr.value)
        else:
            assert False

        execution.append(Operation(value, item, ll, rr))

    assert len(execution) == 1
    return execution.pop()

def recursive_optimize_operation_tree(node):
    if node.operator is None:
        node.compile_expression()
        return

    # Post order traversal. Visit the parent after visiting the children.
    for child in node.children:
        recursive_optimize_operation_tree(child)

    count = len(node.children)

    if node.operator == '+':
        for i in range(count, 0, -1):
            child = node.children[i - 1]
            # Merge '+' children with the parent.
            if child.operator == '+':
                del node.children[i - 1]
                node.children.extend(child.children)
        node.compile_expression()

    elif node.operator == '-':
        # Convert subtraction to addition and reprocess the node.
        assert count == 2
        node.children[1].negate()
        node.operator = '+'
        recursive_optimize_operation_tree(node)

    elif node.operator == 'x':
        for i in range(count, 0, -1):
            child = node.children[i - 1]
            # Merge 'x' children with the parent.
            if child.operator == 'x':
                del node.children[i - 1]
                node.children.extend(child.children)
        node.compile_expression()

    elif node.operator == '/':
        # Convert division to multiplication and reprocess the node.
        assert count == 2
        node.children[1].reciprocate()
        node.operator = 'x'
        recursive_optimize_operation_tree(node)

    else:
        assert False

def recursive_print_binary_operation_tree(node):
    if node.operator is None:
        node.expression = str(node.value)
        return

    assert len(node.children) == 2
    ll = node.children[0]
    rr = node.children[1]

    # Post order traversal. Visit the parent after visiting the children.
    recursive_print_binary_operation_tree(ll)
    recursive_print_binary_operation_tree(rr)

    ll_str = ll.expression
    rr_str = rr.expression

    if node.operator == '-':
        if rr.operator == '+' or rr.operator == '-':
            rr_str = '( ' + rr_str + ' )'

    elif node.operator == 'x':
        if ll.operator == '+' or ll.operator == '-':
            ll_str = '( ' + ll_str + ' )'
        if rr.operator == '+' or rr.operator == '-':
            rr_str = '( ' + rr_str + ' )'

    elif node.operator == '/':
        if ll.operator == '+' or ll.operator == '-':
            ll_str = '( ' + ll_str + ' )'
        if rr.operator is not None:
            rr_str = '( ' + rr_str + ' )'

    node.expression = ll_str + ' ' + node.operator + ' ' + rr_str
