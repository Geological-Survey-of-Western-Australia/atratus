from collections import OrderedDict
import geo_digital_tools as gdt

class Step:
    """Cygnets harmonisation processing step.

    Note:
        This is a modification of the chain of responsibility behavioural pattern.
    """

    def __init__(self, name: str , save : bool = False):
        """Initialise the stage with a name and save.
        
        Args:
            name (str) : An identifier for the step.
            save (bool) : Weather or not to execute the steps save behaviour if implemented.

        Attributes:
            step_success(bool) : Defaults to False, overwritten by run method.
            input (any) : Input for stage.
            output (any) : Output of self.run()
        """
        self.name = name
        self.save = save
        self.stepsuccess = False
        self.input = None
        self.output = None

    def handle(self, input, globals):
        """Handle function performs 3 tasks.

         - Confirms a valid input via logic defined in canhandle
         - Runs the processing logic.
         - If successful either returned the parent process or runs the next step.

        Args:
            input : could be anything.
            globals : dictionary provided by parent process.

        """
        if self.canhandle(input, globals):
            self.input = input
            self.output = self.run()
            if self.save:
                self.save_method()
            return self.output

    def canhandle(self, input, globals) -> bool:
        """Confirms a valid input for this step.

        Args:
            input : could be anything.
            globals : variables in a dict availalbe to the Parent Process

        Raises/Logs:
            KnownExceptions : for anything known data issues.
            
        Returns:
            True if valid input, False otherwise.

        """
        raise NotImplementedError("Should be overwritten")

    def run(self):
        """Confirms a valid input for this step.

        Args:
            input : could be anything.

        Raises/Logs:
            KnownExceptions : for anything known data issues.

        Returns:
            True if valid input, False otherwise.

        """
        self.stepsuccess = False
        raise NotImplementedError("Should be overwritten")

    def save_method(self):
        """Defines save Behaviour for a given Step."""
        self.stepsuccess = False
        raise NotImplementedError("Should be overwritten")


class Process:
    """Cygnets process.

    Note:
        This is a modification of the chain of responsibility behavioural pattern.
    """
    def __init__(self, name, **kwargs):
        """Initialise the process with a name and any keyword args used by your process.
        
        Args:
            name : An name for the process usefull in logging.
            **kwargs : all kwargs are unpacked in the process.globals and passed to all steps.

        Attributes:
            step_dict : An orderered Dictionary of Steps that we iterate over.
            step_out : An optional location to add the outputs of each step.
            step_logs : Unused but we could add logs to the class.
        """
        self.name = name
        self.globals = {**kwargs}
        self.step_dict = OrderedDict()
        self.step_out = OrderedDict()
        self.step_logs = {}

    def __str__(self):
        """String that prints a useful summary of the process steps."""
        summary = f'''The {self.name} process contains {len(self.step_dict)} steps.\nThese are :
        {'\n        '.join([k for k in self.step_dict.keys()])} \nThe process will return the outputs of {next(reversed(self.step_dict))}
        '''
        return summary

    def addstep(self, step):
        """Adds a Step object to the process."""
        if isinstance(step, Step):
            self.step_dict[step.name] = step
        else:
            gdt.KnownException('This is not a valid step.')

    def dropstep(self, step):
        """Removes a step from the process."""
        self.step_dict.pop([step.name], None)

    def run(self):
        """Executes the process."""
        # just before running add a final step
        self.step_dict["end"] = None
        current_state = self.globals['input']
        # run each step and pass the inputs
        for step_name, step in self.step_dict.items():

            # check if its the end
            if step_name == "end":
                print("Process Complete")

            # run the next step
            else:
                current_state = step.handle(current_state, self.globals)
        return current_state
