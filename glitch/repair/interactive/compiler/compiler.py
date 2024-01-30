from typing import Optional, Dict, Tuple

from glitch.tech import Tech
from glitch.repr.inter import *
from glitch.repair.interactive.delta_p import *
from glitch.repair.interactive.compiler.names_database import NamesDatabase
from glitch.repair.interactive.compiler.labeler import LabeledUnitBlock


class DeltaPCompiler:
    class __Attributes:
        def __init__(self, au_type: str, tech: Tech):
            self.__au_type = NamesDatabase.get_au_type(au_type, tech)
            self.__tech = tech
            self.__attributes: Dict[str, Tuple[PExpr, Attribute]] = {}
            self.__sketched = -1

        def add_attribute(self, attribute: Attribute):
            attr_name = NamesDatabase.get_attr_name(
                attribute.name, self.__au_type, self.__tech
            )
            if attr_name is not None:
                self.__attributes[attr_name] = (
                    DeltaPCompiler._compile_expr(attribute.value, self.__tech),
                    attribute,
                )

        def get_attribute(self, attr_name: str) -> Optional[Attribute]:
            return self.__attributes.get(attr_name, (None, None))[1]

        def get_attribute_value(self, attr_name: str) -> PExpr:
            return self.__attributes.get(attr_name, (PEUndef(), None))[0]

        def __getitem__(self, key: str) -> PExpr:
            return self.get_attribute_value(key)

        def create_label_var_pair(
            self,
            attr_name: str,
            atomic_unit: AtomicUnit,
            labeled_script: LabeledUnitBlock,
        ) -> Optional[Tuple[str, str]]:
            attr = self.get_attribute(attr_name)

            if attr is not None:
                label = labeled_script.get_label(attr)
            else:
                # Creates sketched attribute
                attr = Attribute(attr_name, "", False)
                attr.line, attr.column = self.__sketched, self.__sketched
                self.__sketched -= 1
                atomic_unit.attributes.append(attr)
                self.add_attribute(attr)
                label = labeled_script.add_label(attr_name, attr, sketched=True)

            return label, labeled_script.get_var(label)

    @staticmethod
    def _compile_expr(expr: Optional[str], tech: Tech) -> PExpr:
        # FIXME to fix this I need to extend GLITCH's IR
        if expr is None:
            return None
        return PEConst(PStr(expr))

    @staticmethod
    def __handle_attribute(
        attr_name: str,
        atomic_unit: AtomicUnit,
        attributes: __Attributes,
        labeled_script: LabeledUnitBlock,
    ) -> PStatement:
        match attr_name:
            case "state":
                state_label, state_var = attributes.create_label_var_pair(
                    attr_name, atomic_unit, labeled_script
                )
                content_label, content_var = attributes.create_label_var_pair(
                    "content", atomic_unit, labeled_script
                )
                return PLet(
                    state_var,
                    attributes["state"],
                    state_label,
                    PIf(
                        PEBinOP(PEq(), PEVar(state_var), PEConst(PStr("present"))),
                        PLet(
                            content_var,
                            attributes["content"],
                            content_label,
                            PCreate(attributes["path"], PEVar(content_var)),
                        ),
                        PIf(
                            PEBinOP(PEq(), PEVar(state_var), PEConst(PStr("absent"))),
                            PRm(attributes["path"]),
                            PIf(
                                PEBinOP(
                                    PEq(), PEVar(state_var), PEConst(PStr("directory"))
                                ),
                                PMkdir(attributes["path"]),
                                PSkip(),
                            ),
                        ),
                    ),
                )
            case "owner":
                # TODO: this should use a is_defined
                owner_label, owner_var = attributes.create_label_var_pair(
                    "owner", atomic_unit, labeled_script
                )
                return PLet(
                    owner_var,
                    attributes["owner"],
                    owner_label,
                    PChown(attributes["path"], PEVar(owner_var)),
                )
            case "mode":
                # TODO: this should use a is_defined
                mode_label, mode_var = attributes.create_label_var_pair(
                    "mode", atomic_unit, labeled_script
                )
                return PLet(
                    mode_var,
                    attributes["mode"],
                    mode_label,
                    PChmod(attributes["path"], PEVar(mode_var)),
                )

        return None

    @staticmethod
    def compile(labeled_script: LabeledUnitBlock, tech: Tech) -> PStatement:
        statement = PSkip()
        script = labeled_script.script

        # TODO: Handle variables
        # TODO: Handle scopes
        for atomic_unit in script.atomic_units:
            attributes: DeltaPCompiler.__Attributes = DeltaPCompiler.__Attributes(
                atomic_unit.type, tech
            )

            if atomic_unit.type == "file":
                for attribute in atomic_unit.attributes:
                    attributes.add_attribute(attribute)

                for attribute in atomic_unit.attributes:
                    attr_name = NamesDatabase.get_attr_name(
                        attribute.name, atomic_unit.type, tech
                    )
                    attr_statement = DeltaPCompiler.__handle_attribute(
                        attr_name, atomic_unit, attributes, labeled_script
                    )
                    if attr_statement is not None:
                        statement = PSeq(statement, attr_statement)

        return statement
