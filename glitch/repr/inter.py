from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Union


class CodeElement(ABC):
    def __init__(self) -> None:
        self.line: int = -1
        self.column: int = -1
        self.code: str = ""

    def __hash__(self) -> int:
        return hash(self.line) * hash(self.column)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, CodeElement):
            return False
        return self.line == o.line and self.column == o.column

    def __str__(self) -> str:
        return self.__repr__()

    @abstractmethod
    def print(self, tab: int) -> str:
        pass


class Block(CodeElement):
    def __init__(self) -> None:
        super().__init__()
        self.statements: List["ConditionalStatement"] = []

    def add_statement(self, statement: "ConditionalStatement") -> None:
        self.statements.append(statement)


class ConditionalStatement(Block):
    class ConditionType(Enum):
        IF = 1
        SWITCH = 2

    def __init__(
        self,
        condition: str,
        type: "ConditionalStatement.ConditionType",
        is_default: bool = False,
    ) -> None:
        super().__init__()
        self.condition: str = condition
        self.else_statement: ConditionalStatement | None = None
        self.is_default = is_default
        self.type = type

    def __repr__(self) -> str:
        return self.code.strip().split("\n")[0]

    def print(self, tab: int) -> str:
        res = (
            (tab * "\t")
            + str(self.type)
            + " "
            + self.condition
            + ("" if not self.is_default else "default")
            + " (on line "
            + str(self.line)
            + ")"
            + "\n"
        )

        res += (tab * "\t") + "\telse:\n"
        if self.else_statement is not None:
            res += self.else_statement.print(tab + 2) + "\n"

        res += (tab * "\t") + "\tblock:\n"
        for statement in self.statements:
            res += statement.print(tab + 2) + "\n"
        res = res[:-1]

        return res


class Comment(CodeElement):
    def __init__(self, content: str) -> None:
        super().__init__()
        self.content: str = content

    def __repr__(self) -> str:
        return self.content

    def print(self, tab: int) -> str:
        return (tab * "\t") + self.content + " (on line " + str(self.line) + ")"


class KeyValue(CodeElement):
    def __init__(self, name: str, value: str | None, has_variable: bool) -> None:
        self.name: str = name
        self.value: str | None = value
        self.has_variable: bool = has_variable
        self.keyvalues: List[KeyValue] = []

    def __repr__(self) -> str:
        value = repr(self.value).split("\n")[0]
        if value == "None":
            return f"{self.name}:{value}:{self.keyvalues}"
        else:
            return f"{self.name}:{value}"


class Variable(KeyValue):
    def __init__(self, name: str, value: str | None, has_variable: bool) -> None:
        super().__init__(name, value, has_variable)

    def print(self, tab: int) -> str:
        if isinstance(self.value, str):
            return (
                (tab * "\t")
                + self.name
                + "->"
                + self.value
                + " (on line "
                + str(self.line)
                + f" {self.has_variable})"
            )
        elif isinstance(self.value, type(None)):
            return (
                (tab * "\t")
                + self.name
                + "->"
                + "None"
                + " variables:"
                + f" {self.keyvalues}"
                + " (on line "
                + str(self.line)
                + f" {self.has_variable})"
            )
        else:
            return (
                (tab * "\t")
                + self.name
                + "->"
                + repr(self.value)
                + " (on line "
                + str(self.line)
                + f" {self.has_variable})"
            )


class Attribute(KeyValue):
    def __init__(self, name: str, value: str, has_variable: bool) -> None:
        super().__init__(name, value, has_variable)

    def print(self, tab: int) -> str:
        if isinstance(self.value, str):
            return (
                (tab * "\t")
                + self.name
                + "->"
                + self.value
                + " (on line "
                + str(self.line)
                + f" {self.has_variable})"
            )
        elif isinstance(self.value, type(None)):
            return (
                (tab * "\t")
                + self.name
                + "->"
                + "None"
                + " attributes:"
                + f" {self.keyvalues}"
                + " (on line "
                + str(self.line)
                + f" {self.has_variable})"
            )
        else:
            return (
                (tab * "\t")
                + self.name
                + "->"
                + repr(self.value)
                + " (on line "
                + str(self.line)
                + f" {self.has_variable})"
            )


class AtomicUnit(Block):
    def __init__(self, name: str, type: str) -> None:
        super().__init__()
        self.name: str = name
        self.type: str = type
        self.attributes: list[Attribute] = []

    def add_attribute(self, a: Attribute) -> None:
        self.attributes.append(a)

    def __repr__(self) -> str:
        return f"{self.name} {self.type}"

    def print(self, tab: int) -> str:
        res = (
            (tab * "\t")
            + self.type
            + " "
            + self.name
            + " (on line "
            + str(self.line)
            + ")\n"
        )

        for attribute in self.attributes:
            res += attribute.print(tab + 1) + "\n"

        res += (tab * "\t") + "block:\n"
        for statement in self.statements:
            res += statement.print(tab + 2) + "\n"
        res = res[:-1]

        return res


class Dependency(CodeElement):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name: str = name

    def __repr__(self) -> str:
        return self.name

    def print(self, tab: int) -> str:
        return (tab * "\t") + self.name + " (on line " + str(self.line) + ")"


class UnitBlockType(str, Enum):
    script = "script"
    tasks = "tasks"
    vars = "vars"
    block = "block"
    unknown = "unknown"


class UnitBlock(Block):
    def __init__(self, name: str, type: UnitBlockType) -> None:
        super().__init__()
        self.dependencies: list[Dependency] = []
        self.comments: list[Comment] = []
        self.variables: list[Variable] = []
        self.atomic_units: list[AtomicUnit] = []
        self.unit_blocks: list["UnitBlock"] = []
        self.attributes: list[Attribute] = []
        self.name: str | None = name
        self.path: str = ""
        self.type: UnitBlockType = type

    def __repr__(self) -> str:
        return self.name if self.name is not None else ""

    def add_dependency(self, d: Dependency) -> None:
        self.dependencies.append(d)

    def add_comment(self, c: Comment) -> None:
        self.comments.append(c)

    def add_variable(self, v: Variable) -> None:
        self.variables.append(v)

    def add_atomic_unit(self, a: AtomicUnit) -> None:
        self.atomic_units.append(a)

    def add_unit_block(self, u: "UnitBlock") -> None:
        self.unit_blocks.append(u)

    def add_attribute(self, a: Attribute) -> None:
        self.attributes.append(a)

    def print(self, tab: int) -> str:
        if self.name is not None:
            res = (tab * "\t") + self.name + "\n"
        else:
            res = ""

        res += (tab * "\t") + "\tdependencies:\n"
        for dependency in self.dependencies:
            res += dependency.print(tab + 2) + "\n"

        res += (tab * "\t") + "\tcomments:\n"
        for comment in self.comments:
            res += comment.print(tab + 2) + "\n"

        res += (tab * "\t") + "\tvariables:\n"
        for variable in self.variables:
            res += variable.print(tab + 2) + "\n"

        res += (tab * "\t") + "\tattributes:\n"
        for attribute in self.attributes:
            res += attribute.print(tab + 2) + "\n"

        res += (tab * "\t") + "\tatomic units:\n"
        for atomic in self.atomic_units:
            res += atomic.print(tab + 2) + "\n"

        res += (tab * "\t") + "\tunit blocks:\n"
        for unit_block in self.unit_blocks:
            res += unit_block.print(tab + 2) + "\n"

        res += (tab * "\t") + "\tblock:\n"
        for statement in self.statements:
            res += statement.print(tab + 2) + "\n"

        return res


class File:
    def __init__(self, name: str) -> None:
        self.name: str = name

    def print(self, tab: int) -> str:
        return (tab * "\t") + self.name


class Folder:
    def __init__(self, name: str) -> None:
        self.content: List[Union["Folder", File]] = []
        self.name: str = name

    def add_folder(self, folder: "Folder") -> None:
        self.content.append(folder)

    def add_file(self, file: File) -> None:
        self.content.append(file)

    def print(self, tab: int) -> str:
        res = (tab * "\t") + self.name + "\n"

        for c in self.content:
            res += c.print(tab + 1) + "\n"
        res = res[:-1]

        return res


class Module:
    def __init__(self, name: str, path: str) -> None:
        self.name: str = name
        self.path: str = path
        self.blocks: list[UnitBlock] = []
        self.folder: Folder = Folder(name)

    def __repr__(self) -> str:
        return self.name

    def add_block(self, u: UnitBlock) -> None:
        self.blocks.append(u)

    def print(self, tab: int) -> str:
        res = (tab * "\t") + self.name + "\n"

        res += (tab * "\t") + "\tblocks:\n"
        for block in self.blocks:
            res += block.print(tab + 2)

        res += (tab * "\t") + "\tfile structure:\n"
        res += self.folder.print(tab + 2)

        return res


class Project:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.modules: list[Module] = []
        self.blocks: list[UnitBlock] = []

    def __repr__(self) -> str:
        return self.name

    def add_module(self, m: Module) -> None:
        self.modules.append(m)

    def add_block(self, u: UnitBlock) -> None:
        self.blocks.append(u)

    def print(self, tab: int) -> str:
        res = self.name + "\n"

        res += (tab * "\t") + "\tmodules:\n"
        for module in self.modules:
            res += module.print(tab + 2)

        res += (tab * "\t") + "\tblocks:\n"
        for block in self.blocks:
            res += block.print(tab + 2)

        return res
