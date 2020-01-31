"""
# Copyright Jiasong Liang, 2016, 2018
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2018
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file. If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from a2_formula_tree import FormulaTree, Leaf, NotTree, AndTree, OrTree

# Do not change any of the class declarations above this comment.

# Add your functions here.

legal_variables = "abcdefghigklmnopqrtuvwxyz"
and_symbol = "*"
or_symbol = "+"
not_symbol = "-"
left_bracket = "("
right_bracket = ")"
valid_character = "abcdefghigklmnopqrtuvwxyz*+-()"
true = "1"
false = "0"
true_int = 1
false_int = 0


def build_tree(formula):
    """(str) -> FormulaTree
    """
    # When there is only one variable in the formula
    return build_subtree(formula, None, 0, 0, 0)


def build_subtree(formula, root, left_count, right_count, symbol_count):
    if len(formula) == 1 and formula in legal_variables:
        root = Leaf(formula)
    elif len(formula) == 1 and formula not in valid_character:
        root = None
    elif formula is right_bracket and len(formula) == 1:
        root = root
        right_count += 1
    else:
        if formula[0] is left_bracket:
            root = build_subtree(formula[1:], root, left_count + 1, right_count, symbol_count)[0]
        elif formula[0] in legal_variables:
            root = build_subtree(formula[1:], Leaf(formula[0]), left_count, right_count, symbol_count)[0]
        elif formula[0] is and_symbol:
            if formula[1] is left_bracket or formula[1] is not_symbol:
                root = AndTree(root, build_subtree(formula[1:], None, left_count, right_count, symbol_count + 1)[0])
            elif formula[1] in legal_variables:
                root = build_subtree(formula[2:], AndTree(root, Leaf(formula[1])), left_count, right_count + 1, symbol_count)[0]
            else:
                root = None
        elif formula[0] is or_symbol:
            if formula[1] is left_bracket or formula[1] is not_symbol:
                root = OrTree(root, build_subtree(formula[1:], None, left_count, right_count, symbol_count + 1)[0])
            elif formula[1] in legal_variables:
                root = build_subtree(formula[2:], OrTree(root, Leaf(formula[1])), left_count, right_count, symbol_count + 1)[0]
            else:
                root = None
        elif formula[0] is not_symbol:
            if formula[1] is left_bracket:
                root = NotTree(build_subtree(formula[1:], root, left_count, right_count, symbol_count)[0])
            elif formula[1] in legal_variables:
                root = NotTree(Leaf(formula[1]))
                if len(formula) > 2:
                    root = build_subtree(formula[2:], root, left_count, right_count, symbol_count)[0]
            elif formula[1] is not_symbol:
                root = NotTree(build_subtree(formula[1:], root, left_count, right_count, symbol_count)[0])
            else:
                root = None
        elif formula[0] is right_bracket:
            root = build_subtree(formula[1:], root, left_count, right_count + 1, symbol_count)[0]
        else:
            root = None
    return root, left_count, right_count, symbol_count


def draw_formula_tree(root):
    result = draw_formula_tree_helper(root, " ", 0)
    return result[1:-1]


def evaluate(root, variables, values):
    result = evaluate_helper(root, variables, values)
    if result is true:
        result = true_int
    elif result is false:
        result = false_int
    else:
        result = None
    return result


def draw_formula_tree_helper(root, result, count_time):
    """(FormulaTree) -> str"""
    if root is not []:
        if result[-1] is not "\n":
            result += root.get_symbol() + " "
        else:
            result += 2 * count_time * " " + root.get_symbol() + " "
        children = root.get_children()
        if len(children) == 2:
            result = draw_formula_tree_helper(children[1], result,
                                              count_time + 1)
            result = result[:-1] + "\n"
            result = draw_formula_tree_helper(children[0], result,
                                              count_time + 1)
        elif len(children) == 1:
            result = draw_formula_tree_helper(children[0], result,
                                              count_time + 1)
        return result


def evaluate_helper(root, variables, values):
    """(FormulaTree, str, str) -> str"""
    symbol = root.get_symbol()
    children = root.get_children()
    if symbol in variables:
        result = values[variables.index(symbol)]
    elif symbol is not_symbol:
        result = negate(evaluate_helper(children[0], variables, values))
    elif symbol is and_symbol:
        left_result = evaluate_helper(children[0], variables, values)
        right_result = evaluate_helper(children[1], variables, values)
        result = and_comparision(left_result, right_result)
    else:
        left_result = evaluate_helper(children[0], variables, values)
        right_result = evaluate_helper(children[1], variables, values)
        result = or_comparision(left_result, right_result)
    return result


def and_comparision(left, right):
    if left is true and right is true:
        result = true
    else:
        result = false
    return result


def or_comparision(left, right):
    if left is false and right is false:
        result = false
    else:
        result = true
    return result


def negate(truth_value):
    if truth_value is true:
        result = false
    else:
        result = true
    return result


def bulid_tree_helper(formula, root):
    # One single character
    if len(formula) == 1 and formula in legal_variables:
        root = Leaf(formula)
    elif len(formula) == 1 and formula not in valid_character:
        root = None
    elif len(formula) == 1 and root is not None:
        root = root
    else:
        if formula[0] is left_bracket:
            root = bulid_tree_helper(formula[1:], None)
        elif formula[0] in legal_variables:
            root = bulid_tree_helper(formula[1:], Leaf(formula[0]))
        elif formula[0] is not_symbol:
            root = bulid_tree_helper(formula[1:], root)
        elif formula[0] is and_symbol:
            root = AndTree(root, bulid_tree_helper(formula[1:], None))
        elif formula[0] is or_symbol:
            root = OrTree(root, bulid_tree_helper(formula[1:], None))
        elif formula[0] is right_bracket:
            root = bulid_tree_helper(formula[1:], root)
        else:
            root = None
    return root

print(build_subtree("((x+y)*(y*z))", None, 0, 0, 0))