from typing import Tuple
import ast


def insert(chars: str, start: int = 0, *args) -> Tuple[str, int]:
    input_str = args[0]
    output = chars[:start] + input_str + chars[start:]
    end_pos = start + len(input_str)
    return output, end_pos


def delete(chars: str, start: int = 0, *args) -> Tuple[str, int]:
    count = args[0]
    count_pos = start + count
    output = chars[:start] + chars[count_pos:]
    return output, start


def skip(chars: str, start: int = 0, *args) -> Tuple[str, int]:
    count = start + args[0]
    if count > len(chars):
        return "", 0
    return chars, count


def is_valid(stale: str, latest: str, ot_json: str) -> bool:
    ot_json = ast.literal_eval(ot_json)  # This converts input string with array into array i.e list in python
    chars = stale
    start = 0
    for ot in ot_json:
        chars, start = transform(chars, ot, start)
    if chars == latest:
        return True
    else:
        return False


ot_mapping = {
    "skip": [skip, "count"],
    "insert": [insert, "chars"],
    "delete": [delete, "count"]

}


def transform(input_txt: str, op_json: dict, start_pos: int = 0) -> Tuple[str, int]:
    op = op_json.get("op", None)
    start = op_json.get("start", start_pos)
    if op:
        operate = ot_mapping.get(op)
        operation, extra_arg = operate[0], operate[1]
        if extra_arg == "count":
            arg = op_json.get(extra_arg, 0)
        elif extra_arg == "chars":
            arg = op_json.get(extra_arg, "")
        else:
            raise Exception("chars or count argument required")
        output, start = operation(input_txt, start, arg)
        return output, start


def main():
    a = is_valid(
        'Repl.it uses operational transformations to keep everyone in a multiplayer repl in sync.',
        'Repl.it uses operational transformations to keep everyone in a multiplayer repl in sync.',
        '[]'
    )
    b = is_valid(
        'Repl.it uses operational transformations to keep everyone in a multiplayer repl in sync.',
        'Repl.it uses operational transformations.',
        '[{"op": "skip", "count": 45}, {"op": "delete", "count": 47}]'
    )
    c = is_valid(
        'Repl.it uses operational transformations to keep everyone in a multiplayer repl in sync.',
        'Repl.it uses operational transformations.',
        '[{"op": "skip", "count": 40}, {"op": "delete", "count": 47}]'
    )
    t = is_valid(
        'Repl.it uses operational transformations to keep everyone in a multiplayer repl in sync.',
        'Repl.it uses operational transformations.',
        '[{"op": "skip", "count": 40}, {"op": "delete", "count": 47}, {"op": "skip", "count": 2}]'
    )
    u = is_valid(
        'Repl.it uses operational transformations to keep everyone in a multiplayer repl in sync.',
  'We use operational transformations to keep everyone in a multiplayer repl in sync.',
  '[{"op": "delete", "count": 7}, {"op": "insert", "chars": "We"}, {"op": "skip", "count": 4}, {"op": "delete", "count": 1}]'
    )

    print(a)
    print(b)
    print(c)
    print(t)
    print(u)


if __name__ == '__main__':
    main()
