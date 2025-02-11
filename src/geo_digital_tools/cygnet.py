from collections import OrderedDict

import geo_digital_tools as gdt


class Step:
    """A framework to define processing code within a cygnet's Process.

    Each Step represents a distinct transformation of an input.
    Steps can access a class level namespace of global configuration and state.

    A Step is defined with a few key considerations:
    - Determine if the Step can be executed on a provided input.
        canhandle() is where failures due to input to step are handled.
        e.g. Step loads a path -> it receives an invalid path = invalid input -> Step does not run.
    - Execute a defined set of transforms and rules.
        All code that transforms the data is defined in the run method.
        run() is where failures occuring within the step are handled.
        e.g. Step loads a path -> it receives a valid path -> loading path fails = Step fails.
    - Shared functionality such as save /database write*.
        We might want to do things at each step (catalogue errors, save outputs etc)
            Presently this feature is still being defined.

    Note:
        This is a modification of the chain of responsibility behavioural pattern.
    """

    def __init__(self, name: str, save: bool = False):
        """Initialise the stage with a name, and configure saving.

        Args:
            name : An identifier for the step.
            save : Whether or not to execute the steps save behaviour if implemented.

        Attributes:
            step_success: Defaults to False, overwritten by run method.
            input_ : Input for stage.
            output : Output of self.run()
        """
        self.name = name
        self.save = save
        self.input_ = None
        self.output = None

    def handle(self, input_, global_cfg):
        """Handle the input, with validation and error checking.

        This function performs 3 tasks.
         - Confirms a valid input via logic defined in canhandle
         - Runs the processing logic.
         - If successful either returned the parent process or runs the next step.

        Args:
            input_ : Any valid input to the Steps processing code.
            global_cfg : dictionary provided by parent process.
        """
        if self.canhandle(input_, global_cfg):
            self.input_ = input_
            self.output = self.run()
            if self.save and self.output is not None:
                self.save_method()
            return self.output

    def canhandle(self, input_, global_cfg) -> bool:
        """Confirms if the input is valid for this step.

        Args:
            input_ : Any input. Overwrite this function to define which inputs can be handled.
            global_cfg : variables in a dict available to the Parent Process

        Raises:
            KnownException : for any known data issues.

        Returns:
            True if valid input, False otherwise.
        """
        raise NotImplementedError("Should be overwritten")

    def run(self):
        """Run user-defined processing code on a valid input.

        Args:
            input : Any input which has been validated by canhandle()

        Raises:
            KnownException : for any known data issues.

        Returns:
            True if valid input, False otherwise.
        """
        raise NotImplementedError("Should be overwritten")

    def save_method(self):
        """Defines save behaviour for a given Step."""
        raise NotImplementedError("Should be overwritten")


class Process:
    """A container for processing Steps within a cygnet.

    A cygnet is a defined series of operations (Steps) to apply to geoscientific data.
    The order and configuration of those Steps is defined within a Process.

    Global variables
        Some variables (such as database views etc.) should be created once and available through the process.
        These process inputs are variable (process to process) and should be able to be specified by the developer.
    Chain of Responsibility
        Each step passes its outputs to the next step added to the process.
        Each step has access to variables global to the process.
        Each step can validate that the required global variables exist, and outputs of steps meet requirements.
    Centralised collection of arguments (input, output, logs) *
        It is likely that in future we will want to collect logs on a process-by-process approach.
        It's also useful to be able to view the outputs of each step of a process to aid in debugging.
    """

    def __init__(self, name, **kwargs):
        """Initialise the process with a name and any keyword args used by your process.

        Args:
            name : An name for the process useful in logging.
            **kwargs : all kwargs are unpacked in the process.global_cfg and passed to all steps.

        Attributes:
            step_dict : An orderered Dictionary of Steps that we iterate over.
            step_out : An optional location to add the outputs of each step.
            step_logs : Unused but we could add logs to the class.
        """
        self.name = name
        self.global_cfg = {**kwargs}
        self.step_dict: OrderedDict[str, Step] = OrderedDict()
        self.step_out: OrderedDict[str, Step] = OrderedDict()
        self.step_history = {}

    def __str__(self):
        """String that prints a useful summary of the process steps."""
        summary = f"The {self.name} process contains {len(self.step_dict)} steps.\n"
        f"These are:{'\n        '.join([k for k in self.step_dict.keys()])}\n"
        f"The process will return the outputs of {next(reversed(self.step_dict))}"
        return summary

    def addstep(self, step: Step):
        """Adds a Step object to the process."""
        if isinstance(step, Step):
            self.step_dict[step.name] = step
        else:
            gdt.KnownException("This is not a valid Step object.")

    def dropstep(self, step: Step):
        """Removes a step from the process."""
        self.step_dict.pop([step.name], None)

    def start(self):
        """Executes the process."""
        # Append a finalising "end" step to the process.
        self.step_dict["end"] = None

        output = self.global_cfg["input_"]
        # run each step and pass the inputs
        for step_name, step in self.step_dict.items():
            if step_name == "end":
                self.step_history["end"] = True
            else:
                output = step.handle(output, self.global_cfg)
            if output is None:  # Step failed
                self.step_history[step.name] = False
                break

        return output
