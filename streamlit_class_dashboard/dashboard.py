import inspect
from typing import Type, List, Callable, Any, Tuple

import streamlit as st


class Dashboard:
    def __init__(self, cls: Type["Dashboard"]) -> None:
        self.cls = cls
        self.dashboard()

    def dashboard(self) -> None:
        st.title(f"{self.cls.__name__}")

        fields, any_required_input_empty_init = self.initialize_fields()

        if not st.session_state.get(f"create_dashboard_{self.cls.__name__}_instance"):
            st.session_state[
                f"create_dashboard_{self.cls.__name__}_instance"
            ] = self.cls(*fields)

        for name, method in inspect.getmembers(
            st.session_state[f"create_dashboard_{self.cls.__name__}_instance"],
            predicate=inspect.ismethod,
        ):
            if name.startswith("_"):
                continue

            input_args = self.get_input_args(method)

            inputs = []
            any_required_input_empty = False
            for arg_name, arg_type, default_value in input_args:
                formatted_arg_name = self.format_field_name(arg_name)
                key = f"{name}_{arg_name}"

                value: Any
                default_value_in_widget = (
                    default_value if default_value != inspect.Parameter.empty else None
                )

                if arg_type is int:
                    value = st.number_input(
                        formatted_arg_name,
                        key=key,
                        step=1,
                        format="%d",
                        value=default_value_in_widget,
                        disabled=any_required_input_empty_init,
                    )
                elif arg_type is float:
                    value = st.number_input(
                        formatted_arg_name,
                        step=0.01,
                        key=key,
                        value=default_value_in_widget,
                        disabled=any_required_input_empty_init,
                    )
                elif arg_type is str:
                    value = st.text_input(
                        formatted_arg_name,
                        key=key,
                        value=default_value_in_widget or "",
                        placeholder="Required"
                        if default_value == inspect.Parameter.empty
                        else "Not required",
                        disabled=any_required_input_empty_init,
                    )
                else:
                    raise TypeError(f"Type {arg_type} of {arg_name} is not supported")

                inputs.append(value)
                if default_value == inspect.Parameter.empty and not value:
                    any_required_input_empty = True

            submit_button = st.button(
                self.format_method_name(name),
                on_click=None,
                disabled=any_required_input_empty or any_required_input_empty_init,
            )

            if submit_button:
                result = method(*inputs)
                st.write("Result:", result)

    def initialize_fields(self) -> Tuple[List[Any], bool]:
        init_signature = inspect.signature(self.cls.__init__)
        field_values: List[Any] = []

        any_required_input_empty = False

        for param_name, param in init_signature.parameters.items():
            if param_name == "self":
                continue

            field_type = param.annotation
            formatted_param_name = self.format_field_name(param_name)

            default_value_in_widget = (
                param.default if param.default != inspect.Parameter.empty else None
            )
            value: Any

            if field_type is int:
                value = st.sidebar.number_input(
                    formatted_param_name,
                    key=f"field_{param_name}",
                    step=1,
                    format="%d",
                    value=default_value_in_widget,
                    on_change=self.clear_instance,
                )
            elif field_type is float:
                value = st.sidebar.number_input(
                    formatted_param_name,
                    step=0.01,
                    key=f"field_{param_name}",
                    value=default_value_in_widget,
                    on_change=self.clear_instance,
                )
            elif field_type is str:
                value = st.sidebar.text_input(
                    formatted_param_name,
                    key=f"field_{param_name}",
                    value=default_value_in_widget or "",
                    on_change=self.clear_instance,
                    placeholder="Required"
                    if param.default == inspect.Parameter.empty
                    else "Not required",
                )

            if param.default == inspect.Parameter.empty and not value:
                any_required_input_empty = True

            field_values.append(value)

        return field_values, any_required_input_empty

    @staticmethod
    def get_input_args(method: Callable[[Any], Any]) -> List[Any]:
        signature = inspect.signature(method)
        args = []

        for param_name, param in signature.parameters.items():
            if param_name == "self":
                continue

            args.append((param_name, param.annotation, param.default))

        return args

    @staticmethod
    def format_field_name(field_name: str) -> str:
        return field_name.replace("_", " ").capitalize()

    @staticmethod
    def format_method_name(method_name: str) -> str:
        return method_name.replace("_", " ").capitalize()

    def clear_instance(self) -> None:
        st.session_state[f"create_dashboard_{self.cls.__name__}_instance"] = None


@Dashboard
class Dinosaur:
    def __init__(self, name: str = "T-Rex", speed: float = 30.0, age: int = 65_000_000):
        self.name = name
        self.speed = speed
        self.age = age

    def roar(self, volume: int = 100) -> str:
        return f"{self.name} roars at volume {volume} dB!"

    def run(self, distance: float = 100.0) -> str:
        return f"{self.name} runs {distance} meters in {distance / self.speed} seconds!"
