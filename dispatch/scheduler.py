
from __future__ import absolute_import, print_function

import os
import threading

from mesos.interface import Scheduler
from mesos.interface import mesos_pb2
from mesos.native import MesosSchedulerDriver as SchedulerDriver
import urlparse

from . import log
from . import state
from . import version

class DispatchScheduler(Scheduler):

    name = "dispatch"
    version = version

    def __init__(self):
        self.location = None
        self.fwkinfo = self.get_fwkinfo()
        self.driver = self.get_driver()

    def __str__(self):
        return "{0}-{1}".format(self.name, self.version)

    def run(self):
        t = threading.Thread(target=self.driver.run)
        t.setDaemon(True)
        t.start()

    def get_fwkinfo(self):
        return mesos_pb2.FrameworkInfo(user=state.ARGS.user, name=str(self))

    def get_driver(self):
        return SchedulerDriver(self, self.fwkinfo, state.ARGS.master)

    def registered(self, driver, fwid, minfo):
        log.info("registered: {0}".format(fwid.value))

    def set_resource(self, a, x):
        if x.name == "ports":
            a[x.name] = map(lambda x: [x.begin, x.end], x.ranges.range)
        else:
            a[x.name] = x.scalar.value
        return a

    def convert_offer(self, offer):
        return (offer, reduce(self.set_resource, offer.resources, {}))

    def fit_offer(self, resource):
        job = state.CURRENT.next()
        if len([v for k,v in resource.iteritems() if job.resource.get(k, 0) > v]) > 0:
            return None
        if not "ports" in resource:
            return None
        return job

    def resourceOffers(self, driver, offers):
        for offer, r in map(lambda x: self.convert_offer(x), offers):
            log.info("offer: {0}".format(offer.id.value))

            if state.CURRENT.empty:
                driver.declineOffer(offer.id)
                continue

            # XXX - naive way to fit offers, should be better
            job = self.fit_offer(r)
            if not job:
                driver.declineOffer(offer.id)
                continue

            job.location = offer.hostname
            task = self.make_task(job, offer, r)
            print("job: {0}; task: {1}; host: {2}".format(
                job.id,
                task.task_id.value,
                offer.hostname))
            driver.launchTasks(offer.id, [task])

    def make_task(self, job, offer, resources):
        task = mesos_pb2.TaskInfo(
            slave_id=offer.slave_id,
            command=self.build_cmd(job, resources["ports"][0][0]))
        task.task_id.value = job.id
        task.name = str(self)

        for k, v in job.resource.iteritems():
            r = task.resources.add()
            r.name = k
            r.type = mesos_pb2.Value.SCALAR
            r.scalar.value = v

        # XXX - Assuming there's at least one port in the offer
        r = task.resources.add()
        r.name = "ports"
        r.type = mesos_pb2.Value.RANGES
        p = r.ranges.range.add()
        p.begin = resources["ports"][0][0]
        p.end = resources["ports"][0][0] + 1

        return task

    def build_cmd(self, job, port):
        cmd = mesos_pb2.CommandInfo()
        cmd.value = "bash wrapper.bash"

        env = cmd.environment.variables.add()
        env.name = "PORT"
        env.value = str(port)

        # XXX - This is definitely the wrong place to do this.
        job.port = port

        for uri in job.uris():
            cmd.uris.add().value = uri

        return cmd

    def statusUpdate(self, driver, status):

        # XXX - This is hard-coded, this is bad.
        if status.state == mesos_pb2.TASK_RUNNING:
            current = state.CURRENT[status.task_id.value]
            current.running = True

        # XXX - Remove job from status on completion
        pass
