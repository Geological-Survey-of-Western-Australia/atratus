from collections import OrderedDict


class Step:
    """
    Cygnets harmonisation processing step.

    Note:
        This is a modification of the chain of responsibility behavioural pattern.

    Args:
        name (str) : An identifier for the step.

    Attributes:
        step_success(bool) : Defaults to False, overwritten by run method.
        input (any) : Input for stage.
        output (any) : Output of self.run()

    """

    def __init__(self, name: str):
        self.name = name
        self.stepsuccess = False
        self.input = None
        self.output = None

    def handle(self, input):
        """
        Handle function performs 3 tasks:
         - Confirms a valid input via logic defined in canhandle
         - Runs the processing logic.
         - If successful either returned the parent process or runs the next step.

        Args:
            input : could be anything

        """
        if self.canhandle(input):
            self.input = input
            self.output = self.run()
            return self.output

    def canhandle(self, input) -> bool:
        """
        Confirms a valid input for this step.

        Args:
            input : could be anything.
        Raises/Logs:
            KnownExceptions : for anything known data issues.
        Returns:
            True if valid input, False otherwise.

        """
        raise NotImplementedError("Should be overwritten")

    def run(self):
        """
        Confirms a valid input for this step.

        Args:
            input : could be anything.
        Raises/Logs:
            KnownExceptions : for anything known data issues.
        Returns:
            True if valid input, False otherwise.

        """
        self.stepsuccess = False
        raise NotImplementedError("Should be overwritten")


class Process:
    def __init__(self, name, **kwargs):
        self.name = name
        self.step_dict = OrderedDict()
        self.step_out = OrderedDict()
        self.step_logs = {}

    def __str__(self):
        summary = f'''The {self.name} process contains {len(self.step_dict)} steps.\nThese are :
        {'\n        '.join([k for k in self.step_dict.keys()])} \nThe process will return the outputs of {next(reversed(self.step_dict))}
        '''
        return summary

    def addstep(self, step):
        self.step_dict[step.name] = step

    def dropstep(self, step):
        self.step_dict.pop([step.name], None)

    def run(self, data):
        # just before running add a final step
        self.step_dict["end"] = None
        current_state = data

        # run each step and pass the inputs
        for step_name, step in self.step_dict.items():

            # check if its the end
            if step_name == "end":
                print("Process Complete")

            # run the next step
            if step_name != "end":
                current_state = step.handle(current_state)
        return current_state
