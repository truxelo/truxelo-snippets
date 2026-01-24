import re
from enum import Enum
from typing import Callable


class Case(Enum):
    """Possible string cases"""

    SNAKE = "snake"
    CAMEL = "camel"
    KEBAB = "kebab"
    PASCAL = "pascal"


class CaseValidator:
    """Expose method validating string's cases"""

    @classmethod
    def get_validator(cls, case: Case) -> Callable[[str], bool]:
        """Get the validator for the given case"""
        validator_name = f"is_{case.value}"
        if not hasattr(cls, validator_name):
            raise NotImplementedError(f"CaseValidator.{validator_name}")
        return getattr(cls, validator_name)

    @staticmethod
    def is_camel(string: str) -> bool:
        """Check if the string is in camel case.

        Examples:
            >>> assert CaseValidator.is_camel('myVariableName')
            >>> assert not CaseValidator.is_camel('MyVariableName')
        """
        return bool(re.match("^[a-z]+([A-Z]+[a-z]+)*$", string))

    @staticmethod
    def is_snake(string: str) -> bool:
        """Check if the string is in snake case.

        Examples:
            >>> assert CaseValidator.is_snake('my_variable_name')
            >>> assert not CaseValidator.is_snake('myVariableName')
        """
        return bool(re.match("^[a-z]+(_[a-z]+)*$", string))

    @staticmethod
    def is_kebab(string: str) -> bool:
        """Check if the string is in kebab case.

        Examples:
            >>> assert CaseValidator.is_kebab('my-variable-name')
            >>> assert not CaseValidator.is_kebab('myVariableName')
        """
        return bool(re.match("^[a-z]+(-[a-z]+)*$", string))

    @staticmethod
    def is_pascal(string: str) -> bool:
        """Check if the string is in pascal case.

        Examples:
            >>> assert CaseValidator.is_pascal('MyVariableName')
            >>> assert not CaseValidator.is_pascal('myVariableName')
        """
        return bool(re.match("^([A-Z]+[a-z]+)+$", string))


class CaseEnforcer:
    """Expose method enforcing a string's case"""

    @classmethod
    def get_enforcer(cls, case: Case) -> Callable[[str], str]:
        """Get the enforcer for the given case"""
        enforcer_name = f"to_{case.value}"
        if not hasattr(cls, enforcer_name):
            raise NotImplementedError(f"CaseValidator.{enforcer_name}")
        return getattr(cls, enforcer_name)

    @staticmethod
    def get_components(string: str) -> list[str]:
        """Extract components from any case string.

        This method normalizes a string by replacing underscores, hyphens,
        and spaces with a single space, and then splitting the string into
        its lowercase components based on case transitions or delimiters.

        Examples:
            >>> CaseEnforcer.get_components('myVariableName')
            ['my', 'variable', 'name']

            >>> CaseEnforcer.get_components('my_variable_name')
            ['my', 'variable', 'name']

            >>> CaseEnforcer.get_components('my-variable-name')
            ['my', 'variable', 'name']

            >>> CaseEnforcer.get_components('MyVariableName')
            ['my', 'variable', 'name']

            >>> CaseEnforcer.get_components("My'Variable_name")
            ['my', 'variable', 'name']

            >>> CaseEnforcer.get_components('my variable name')
            ['my', 'variable', 'name']
        """
        components_str = re.sub(r"(_|-)+", " ", string)
        components_str = re.sub(r"([A-Z])", r" \g<1>", components_str)
        components_str = components_str.lower()
        components_str = components_str.replace("'", " ")
        components_str = components_str.replace('"', " ")
        components_str = components_str.strip()
        components = components_str.split(" ")
        return [component for component in components if component]

    @classmethod
    def to_camel(cls, string: str) -> str:
        """Force the string to camel case.

        Examples:
            >>> CaseEnforcer.to_camel('my_variable_name')
            'myVariableName'
        """
        components = cls.get_components(string)
        return components[0] + "".join(x.title() for x in components[1:])

    @classmethod
    def to_snake(cls, string: str) -> str:
        """Force the string to snake case.

        Examples:
            >>> CaseEnforcer.to_snake('myVariableName')
            'my_variable_name'
        """
        return "_".join(cls.get_components(string))

    @classmethod
    def to_kebab(cls, string: str) -> str:
        """Force the string to kebab case.

        Examples:
            >>> CaseEnforcer.to_kebab('myVariableName')
            'my-variable-name'
        """
        return "-".join(cls.get_components(string))

    @classmethod
    def to_pascal(cls, string: str) -> str:
        """Force the string to pascal case.

        Examples:
            >>> CaseEnforcer.to_pascal('my_variable_name')
            'MyVariableName'
        """
        components = cls.get_components(string)
        return "".join(x.title() for x in components)


class CaseConverter:
    """Expose methods transforming string from one case to others.

    Warning:
        If the input string does not conform to the expected case format,
        the output will be gibberish.
    """

    @classmethod
    def get_converter(cls, from_case: Case, to_case: Case) -> Callable[[str], str]:
        """Get the converter from one case to another."""
        converter_name = f"convert_{from_case.value}_to_{to_case.value}"
        if not hasattr(cls, converter_name):
            raise NotImplementedError(f"CaseConverter.{converter_name}")
        return getattr(cls, converter_name)

    @staticmethod
    def convert_snake_to_camel(string: str) -> str:
        """Convert a snake cased string to camel case.

        Example:
            >>> CaseConverter.convert_snake_to_camel('my_variable_name')
            'myVariableName'

            >>> CaseConverter.convert_snake_to_camel('Not_Snake Case')
            'NotSnake Case'
        """
        components = string.split("_")
        return components[0] + "".join(x.title() for x in components[1:])

    @staticmethod
    def convert_snake_to_kebab(string: str) -> str:
        """Convert a snake cased string to kebab case.

        Example:
            >>> CaseConverter.convert_snake_to_kebab('my_variable_name')
            'my-variable-name'

            >>> CaseConverter.convert_snake_to_kebab('Not_Snake Case')
            'Not-Snake Case'
        """
        return string.replace("_", "-")

    @staticmethod
    def convert_snake_to_pascal(string: str) -> str:
        """Convert a snake cased string to pascal case.

        Example:
            >>> CaseConverter.convert_snake_to_pascal('my_variable_name')
            'MyVariableName'

            >>> CaseConverter.convert_snake_to_pascal('Not_Snake Case')
            'NotSnake Case'
        """
        return "".join(x.title() for x in string.split("_"))

    @staticmethod
    def convert_camel_to_snake(string: str) -> str:
        """Convert a camel cased string to snake case.

        Example:
            >>> CaseConverter.convert_camel_to_snake('myVariableName')
            'my_variable_name'

            >>> CaseConverter.convert_camel_to_snake('NotCamel Case')
            '_not_camel _case'
        """
        return re.sub("([A-Z])", r"_\1", string).lower()

    @staticmethod
    def convert_camel_to_kebab(string: str) -> str:
        """Convert a camel cased string to kebab case.

        Example:
            >>> CaseConverter.convert_camel_to_kebab('myVariableName')
            'my-variable-name'

            >>> CaseConverter.convert_camel_to_kebab('NotCamel Case')
            '-not-camel -case'
        """
        return re.sub("([A-Z])", r"-\1", string).lower()

    @staticmethod
    def convert_camel_to_pascal(string: str) -> str:
        """Convert a camel cased string to pascal case.

        Example:
            >>> CaseConverter.convert_camel_to_pascal('myVariableName')
            'MyVariableName'

            >>> CaseConverter.convert_camel_to_pascal('NotCamel Case')
            'NotCamel Case'
        """
        return f"{string[0].upper()}{string[1:]}"

    @staticmethod
    def convert_kebab_to_snake(string: str) -> str:
        """Convert a kebab cased string to snake case.

        Example:
            >>> CaseConverter.convert_kebab_to_snake('my-variable-name')
            'my_variable_name'

            >>> CaseConverter.convert_kebab_to_snake('Not-Kebab Case')
            'Not_Kebab Case'
        """
        return string.replace("-", "_")

    @staticmethod
    def convert_kebab_to_camel(string: str) -> str:
        """Convert a kebab cased string to camel case.

        Example:
            >>> CaseConverter.convert_kebab_to_camel('my-variable-name')
            'myVariableName'

            >>> CaseConverter.convert_kebab_to_camel('Not-Kebab Case')
            'NotKebab Case'
        """
        components = string.split("-")
        return components[0] + "".join(x.title() for x in components[1:])

    @staticmethod
    def convert_kebab_to_pascal(string: str) -> str:
        """Convert a kebab cased string to pascal case.

        Example:
            >>> CaseConverter.convert_kebab_to_pascal('my-variable-name')
            'MyVariableName'

            >>> CaseConverter.convert_kebab_to_pascal('Not-Kebab Case')
            'NotKebab Case'
        """
        return "".join(x.title() for x in string.split("-"))

    @staticmethod
    def convert_pascal_to_snake(string: str) -> str:
        """Convert a pascal cased string to snake case.

        Example:
            >>> CaseConverter.convert_pascal_to_snake('MyVariableName')
            'my_variable_name'

            >>> CaseConverter.convert_pascal_to_snake('not-Pascal Case')
            'not-_pascal _case'
        """
        return re.sub("([A-Z])", r"_\1", string).lower().strip("_")

    @staticmethod
    def convert_pascal_to_camel(string: str) -> str:
        """Convert a pascal cased string to camel case.

        Example:
            >>> CaseConverter.convert_pascal_to_camel('MyVariableName')
            'myVariableName'

            >>> CaseConverter.convert_pascal_to_camel('not-Pascal Case')
            'not-Pascal Case'

        """
        return f"{string[0].lower()}{string[1:]}"

    @staticmethod
    def convert_pascal_to_kebab(string: str) -> str:
        """Convert a pascal cased string to kebab case.

        Example:
            >>> CaseConverter.convert_pascal_to_kebab('MyVariableName')
            'my-variable-name'

            >>> CaseConverter.convert_pascal_to_kebab('not-Pascal Case')
            'not--pascal -case'
        """
        return re.sub("([A-Z])", r"-\1", string).lower().strip("-")


def convert_case(string: str, from_case: Case, to_case: Case) -> str:
    """
    Convert a string from one case to another, ensuring the original string
    matches the `from_case`.

    Args:
        string: The input string to convert.
        from_case: The current case of the string.
        to_case: The target case for conversion.

    Returns:
        The string converted to the target case.

    Raises:
        ValueError: If the input string does not match the `from_case`.

    Examples:
        >>> convert_case('my_variable_name', Case.SNAKE, Case.CAMEL)
        'myVariableName'

        >>> convert_case('myVariableName', Case.CAMEL, Case.KEBAB)
        'my-variable-name'

        >>> convert_case('my-variable-name', Case.KEBAB, Case.PASCAL)
        'MyVariableName'

        >>> convert_case('MyVariableName', Case.PASCAL, Case.SNAKE)
        'my_variable_name'
    """
    is_valid = CaseValidator.get_validator(from_case)
    if not is_valid(string):
        raise ValueError(f"{string} is not a {from_case.value} case string")
    convert = CaseConverter.get_converter(from_case, to_case)
    return convert(string)


def force_case(string: str, case: Case) -> str:
    """
    Force a string into the specified case, transforming its format.

    Args:
        string: The input string to be transformed.
        case: The target case to enforce.

    Returns:
        The string transformed into the target case.

    Examples:
        >>> force_case('my-variable-name', Case.SNAKE)
        'my_variable_name'

        >>> force_case('MyVariableName', Case.KEBAB)
        'my-variable-name'

        >>> force_case('my_variable_name', Case.PASCAL)
        'MyVariableName'

        >>> force_case('myVariableName', Case.CAMEL)
        'myVariableName'
    """
    enforce = CaseEnforcer.get_enforcer(case)
    return enforce(string)
