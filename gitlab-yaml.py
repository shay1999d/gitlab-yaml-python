from job import Job
import yaml


class GitlabYAML:
    def __init__(self):
        self.instructions = {
            'image': {},
            'stages': [],
        }

        self.jobs = {}
        self.default = None
        self.active_stage = None
        self.active_job = None

    def clear_unused_keys(self, obj):
        removable = [[], None, {}, '']
        if isinstance(obj, dict):
            return {k: self.clear_unused_keys(v) for k, v in obj.items() if v not in removable}
        elif isinstance(obj, Job):
            return {k: v for k, v in obj.__dict__.items() if v not in removable}
        else:
            return obj

    def build(self):
        if self.jobs:
            self.instructions.update(self.jobs)
        self.instructions = self.clear_unused_keys(self.instructions)
        return yaml.dump(self.instructions, default_flow_style=False)

    def write(self, path='.gitlab-ci.yml'):
        open(path, 'w').write(self.build())

    def image(self, name=None, entrypoint=None, command=None, alias=None):
        if name:
            self.instructions['image']['name'] = name
        if entrypoint:
            self.instructions['image']['entrypoint'] = entrypoint
        if command:
            self.instructions['image']['command'] = command
        if alias:
            self.instructions['image']['alias'] = alias
        return self

    def stage(self, stage_name):
        self.active_stage = stage_name
        if stage_name not in self.instructions['stages']:
            self.instructions['stages'].append(stage_name)
        return self

    def job(self, job_name):
        self.active_job = job_name
        self.jobs[job_name] = Job(job_name, self.active_stage)
        return self.jobs[job_name]

    def script(self, command):
        if isinstance(self.jobs['staging'], Job):
            self.jobs[self.active_job].add_script(command)
        return self

    def before_script(self, command):
        return self

    def after_script(self, command):
        return self

    # TODO add validator for config from https://docs.gitlab.com/ee/api/lint.html

if __name__ == '__main__':
    config = GitlabYAML()
    # config.image('ruby:4.0.1')
    build_stage = config.stage('deploy')
    build_stage.job('staging').add_script('echo test').add_script('test code').add_script('sup man').add_after_script(
        'hello user').add_before_script('sup')

    print(config.build())
    config.write()
