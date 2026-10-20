"""
A small named Lambda Calculus interpreter with a complete beta-reduction trace.

Syntax:
    x                 variable
    \\x.M or λx.M      abstraction
    M N               application (left associative)

Examples:
    (\\x.x) y
    (\\x.\\y.x) y
    (\\x.x x) (\\y.y)
    ((\\x.\\y.x) a) b
"""

from dataclasses import dataclass
import re


# ---------- Expression data types ----------

@dataclass(frozen=True)
class Var:
    name: str


@dataclass(frozen=True)
class Abs:
    param: str
    body: object


@dataclass(frozen=True)
class App:
    func: object
    arg: object


# ---------- Parser ----------

TOKEN_PATTERN = re.compile(
    r"\s*(λ|\\|\.|\(|\)|[A-Za-z_][A-Za-z0-9_']*)"
)


class ParseError(ValueError):
    pass


def tokenize(source):
    tokens = []
    pos = 0

    while pos < len(source):
        match = TOKEN_PATTERN.match(source, pos)

        if not match:
            if source[pos:].strip() == "":
                break

            raise ParseError(
                f"無法解析位置 {pos + 1} 附近的字元："
                f"{source[pos:pos + 12]!r}"
            )

        tokens.append(match.group(1))
        pos = match.end()

    return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, expected=None):
        token = self.peek()

        if token is None:
            raise ParseError("公式不完整，遇到輸入結尾。")

        if expected is not None and token != expected:
            raise ParseError(
                f"預期 {expected!r}，但讀到 {token!r}。"
            )

        self.pos += 1
        return token

    def parse(self):
        if not self.tokens:
            raise ParseError(
                "請輸入 Lambda Calculus 表達式。"
            )

        expr = self.parse_expr()

        if self.peek() is not None:
            raise ParseError(
                f"多餘的 token：{self.peek()!r}。"
                "請檢查括號或空白。"
            )

        return expr

    def parse_expr(self):
        if self.peek() in ("\\", "λ"):
            self.consume()

            param = self.consume()

            if param in (".", "(", ")", "\\", "λ"):
                raise ParseError(
                    "抽象式需要一個變數名稱，例如 \\x.x"
                )

            self.consume(".")
            body = self.parse_expr()

            return Abs(param, body)

        return self.parse_application()

    def parse_application(self):
        expr = self.parse_atom()

        while (
            self.peek() is not None
            and self.peek() not in (")", ".")
        ):
            if self.peek() in ("\\", "λ"):
                # An abstraction used as an argument
                # must be parenthesized.
                break

            expr = App(expr, self.parse_atom())

        return expr

    def parse_atom(self):
        token = self.peek()

        if token is None:
            raise ParseError("缺少表達式。")

        if token == "(":
            self.consume("(")
            expr = self.parse_expr()
            self.consume(")")
            return expr

        if token in (")", ".", "\\", "λ"):
            raise ParseError(
                f"此處不應出現 {token!r}。"
            )

        self.consume()
        return Var(token)


def parse(source):
    return Parser(tokenize(source)).parse()


# ---------- Pretty-printing and variables ----------

def pretty(expr, context=0):
    """Print an expression with parentheses only where needed."""
    if isinstance(expr, Var):
        return expr.name

    if isinstance(expr, Abs):
        text = f"λ{expr.param}.{pretty(expr.body)}"
        return f"({text})" if context > 0 else text

    if isinstance(expr, App):
        text = (
            f"{pretty(expr.func, 1)} "
            f"{pretty(expr.arg, 2)}"
        )
        return f"({text})" if context > 1 else text

    raise TypeError(
        f"未知的表達式節點：{expr!r}"
    )


def free_vars(expr):
    """Return all free variables in an expression."""
    if isinstance(expr, Var):
        return {expr.name}

    if isinstance(expr, Abs):
        return free_vars(expr.body) - {expr.param}

    if isinstance(expr, App):
        return (
            free_vars(expr.func)
            | free_vars(expr.arg)
        )

    raise TypeError("未知的表達式節點")


def all_vars(expr):
    """Return all variable names, both bound and free."""
    if isinstance(expr, Var):
        return {expr.name}

    if isinstance(expr, Abs):
        return {expr.param} | all_vars(expr.body)

    if isinstance(expr, App):
        return (
            all_vars(expr.func)
            | all_vars(expr.arg)
        )

    raise TypeError("未知的表達式節點")


def fresh_name(base, forbidden):
    """Generate a variable name that is not already used."""
    index = 1
    candidate = f"{base}_{index}"

    while candidate in forbidden:
        index += 1
        candidate = f"{base}_{index}"

    return candidate


# ---------- Capture-avoiding substitution ----------

def substitute(expr, variable, replacement, alpha_events):
    """
    Substitute replacement for free occurrences of variable.

    alpha_events records alpha-renaming steps needed
    to prevent variable capture.
    """
    if isinstance(expr, Var):
        if expr.name == variable:
            return replacement

        return expr

    if isinstance(expr, App):
        return App(
            substitute(
                expr.func,
                variable,
                replacement,
                alpha_events
            ),
            substitute(
                expr.arg,
                variable,
                replacement,
                alpha_events
            ),
        )

    if isinstance(expr, Abs):
        # The abstraction binds this variable,
        # so substitution must stop here.
        if expr.param == variable:
            return expr

        replacement_free = free_vars(replacement)

        # No capture can occur if the bound variable
        # does not appear free in the replacement.
        if expr.param not in replacement_free:
            return Abs(
                expr.param,
                substitute(
                    expr.body,
                    variable,
                    replacement,
                    alpha_events
                ),
            )

        # Rename the bound variable to avoid capture.
        forbidden = (
            all_vars(expr.body)
            | all_vars(replacement)
            | {variable, expr.param}
        )

        new_param = fresh_name(
            expr.param,
            forbidden
        )

        alpha_events.append(
            f"α-改名：將繫結變數 {expr.param} "
            f"改成 {new_param}，"
            "避免捕獲代入式中的自由變數。"
        )

        renamed_body = substitute(
            expr.body,
            expr.param,
            Var(new_param),
            alpha_events
        )

        return Abs(
            new_param,
            substitute(
                renamed_body,
                variable,
                replacement,
                alpha_events
            ),
        )

    raise TypeError("未知的表達式節點")


# ---------- One normal-order beta-reduction step ----------

def beta_step(expr):
    """
    Return (new_expr, description, alpha_events),
    or None if no redex remains.

    Uses leftmost-outermost (normal-order) reduction,
    including reduction under lambda abstractions.
    """
    if isinstance(expr, Var):
        return None

    if isinstance(expr, Abs):
        body_step = beta_step(expr.body)

        if body_step is None:
            return None

        new_body, description, alpha_events = body_step

        return (
            Abs(expr.param, new_body),
            f"在 λ{expr.param} 的函式本體內："
            f"{description}",
            alpha_events
        )

    if isinstance(expr, App):
        # Reduce the outermost redex first.
        if isinstance(expr.func, Abs):
            abstraction = expr.func
            alpha_events = []

            new_expr = substitute(
                abstraction.body,
                abstraction.param,
                expr.arg,
                alpha_events
            )

            description = (
                f"β-reduction：把 {pretty(expr.arg)} "
                f"代入 λ{abstraction.param}."
                f"{pretty(abstraction.body)} 中變數 "
                f"{abstraction.param} 的自由位置。"
            )

            return (
                new_expr,
                description,
                alpha_events
            )

        # Try reducing the function part first.
        func_step = beta_step(expr.func)

        if func_step is not None:
            new_func, description, alpha_events = func_step

            return (
                App(new_func, expr.arg),
                f"先化簡函式部分：{description}",
                alpha_events
            )

        # If necessary, reduce the argument.
        arg_step = beta_step(expr.arg)

        if arg_step is not None:
            new_arg, description, alpha_events = arg_step

            return (
                App(expr.func, new_arg),
                f"再化簡引數部分：{description}",
                alpha_events
            )

        return None

    raise TypeError("未知的表達式節點")


# ---------- Interpreter and trace ----------

def reduce_with_trace(expr, max_steps=100):
    current = expr

    print(
        "\n完整計算過程"
        "（normal-order β-reduction）："
    )
    print(f"Step 0: {pretty(current)}")

    step_number = 0

    while step_number < max_steps:
        result = beta_step(current)

        if result is None:
            print("\n完成：已到達 β-正規形。")
            print(f"最終結果：{pretty(current)}")
            print(f"β-reduction 次數：{step_number}")
            return current

        new_expr, description, alpha_events = result

        for event in alpha_events:
            print(f"  {event}")

        print(f"  步驟說明：{description}")

        current = new_expr
        step_number += 1

        print(f"Step {step_number}: {pretty(current)}")

    print(
        f"\n停止：已達最大步數 {max_steps}，"
        "公式可能不會終止或需要更多步數。"
    )
    print(f"目前結果：{pretty(current)}")

    return current


# ---------- Built-in examples ----------

EXAMPLES = {
    "1": (
        "Identity：把 x 原樣回傳",
        r"(\x.x) y"
    ),
    "2": (
        "避免變數捕獲：展示 α-改名",
        r"(\x.\y.x) y"
    ),
    "3": (
        "多步計算：自我套用 Identity",
        r"(\x.x x) (\y.y)"
    ),
    "4": (
        "Church Boolean：選出第一個參數",
        r"((\x.\y.x) a) b"
    ),
}


def main():
    print(
        "Lambda Calculus 解譯器"
        "（具完整 β-reduction 計算過程）"
    )

    print(
        "語法：變數 x；抽象式 \\x.M 或 λx.M；"
        "應用式 M N。"
    )

    print("抽象式若放在應用式內，請加括號。")

    print("\n內建範例：")

    for key, (description, source) in EXAMPLES.items():
        print(f"  {key}. {description}: {source}")

    print(
        "輸入範例編號，或直接輸入自己的 "
        "Lambda Calculus 表達式。"
    )

    user_input = input(
        "請輸入（直接按 Enter 使用範例 2）："
    ).strip()

    if not user_input:
        user_input = "2"

    if user_input in EXAMPLES:
        description, source = EXAMPLES[user_input]

        print(f"\n選擇範例：{description}")
        print(f"原始輸入：{source}")
    else:
        source = user_input

    try:
        expression = parse(source)

    except (ParseError, ValueError) as error:
        print(f"輸入錯誤：{error}")
        return

    print(f"解析結果：{pretty(expression)}")

    reduce_with_trace(
        expression,
        max_steps=100
    )


if __name__ == "__main__":
    main()
