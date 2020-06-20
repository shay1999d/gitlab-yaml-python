class Job:
    def __init__(self, name, stage):
        self.name = name
        self.stage = stage
        self.before_scripts = []
        self.scripts = []

        self.after_scripts = []

    def add_script(self, command):
        self.scripts.append(command)
        return self

    def add_before_script(self, command):
        self.before_scripts.append(command)
        return self

    def add_after_script(self, command):
        self.after_scripts.append(command)
        return self

    def only(self, branch):
        pass
