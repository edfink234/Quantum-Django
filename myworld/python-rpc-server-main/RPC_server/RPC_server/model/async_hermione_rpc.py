# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 2022

@author: Christian Melzer
"""

import logging
import sys
from threading import Thread
import time
from typing import Optional
import uuid


logger = logging.getLogger(__name__)

def use_cmd_line_args(func: callable) -> callable:
    """
    Helper function for parsing command line arguments.
    Meant to be used as a decorator.

    Parameters
    ----------
    func : callable
        The function to which to pass the parsed arguments.
        Should allow for every argument to be positional,
        because keyword arguments are not yet supported.

    Returns
    -------
    callable
        The function with parsed arguments already set.
    """

    # TODO do for kwargs ("xx"="yklsj") and use type hints for conversion

    cmd_line_args = sys.argv[1:]

    def func_to_call():
        return func(*cmd_line_args)

    # use doc string of original function (for docu)
    func_to_call.__doc__ = func.__doc__

    return func_to_call

class JobData: # TODO data class or remove
    """ Data class for job data. """

    def __init__(self, *args, **kwargs):
        """
        Job Data constructor.
        """

        self.args = args
        self.kwargs = kwargs

def function_wrapper(function: callable, result: list, *args, **kwargs):
    """
    Wraps the function to be executed.
    Most importantly, has a mutable argument that will be given the result.

    Parameters
    ----------
    function : callable
        Function to be called.
    result : list
        Mutable argument to store the result and retrieve from another thread.
    *args
        Arguments to call function with.
    **kwargs
        Keyword arguments to call function with.
    """

    logger.debug("Called %s to be executed in background with %s and %s.", function, args, kwargs)

    try:
        result += [{"result": function(*args, **kwargs)}]
    except Exception as e:
        logger.error("Error while executing working thread: %s", e)
        result += [{"error": str(e)}]

class Job:
    """
    Class to describe the job.
    The job is to execute a certain function.
    """

    process_func: callable = None
    """ The job function, i.e. the function the job is about. """

    def __init__(self, id: str, *args, **kwargs):
        """
        Job constructor.

        Parameters
        ----------
        id : str
            The unique job identifier.
        *args
            Job parameters. Passed to the job function.
        **kwargs
            Job keyword parameters. Passed to the job function.
        """

        self.id: str = id
        """ A unique identifier. """

        self.data: JobData = JobData(*args, **kwargs)
        """ The job data (copy of the job arguments). """

        self.submit_time: float = time.time()
        """ The time at which the job has been created. """

        self.finish_time: Optional[float] = None
        """ The time at which the job has completed (if it has). """

        self._result: Optional[dict] = None
        """ The result of the job, i.e. the return value of the job function. """


        self._thread_result: list = []
        """ A mutable construct to retrieve the job result from the job thread. """

        try:
            self.thread: Thread = Thread(target=function_wrapper,
                                         args=[Job.process_func, self._thread_result] + list(args),
                                         kwargs=kwargs)
            """ The thread that runs the job function. """

            self.thread.start()
        except Exception as e:
            logger.error("Processing thread of job with id %s raised exception on start: %s",
                         self.id, e)

        logger.info("Created new job %s.", self.id)

    def set_result(self, result: dict):
        """
        Properly set the result of the job.

        Parameters
        ----------
        result : dict
            The result (return value of the job function).
        """

        self._result = result
        self.finish_time = time.time()
        logger.debug("Completed execution of job %s after %s s.",
                     self.id, (self.finish_time - self.submit_time))

    def get_result(self) -> Optional[dict]:
        """
        Properly query the job result.

        Returns
        -------
        Optional[dict]
            The job result or None, if job has not yet finished
            (job function should not return None on success).
        """

        logger.debug("Trying to get result of %s.", self)
        if self.thread.is_alive():
            logger.debug("Thread of %s is still running. Cannot yet get a result.", self)
            return None

        logger.debug("Thread of %s should have finished. Joining...", self)
        self.thread.join()
        assert len(self._thread_result) == 1
        result = self._thread_result[0]
        self.set_result(result)
        logger.log(15, "Thread of %s finished properly. Result: %s", self, result)

        return result

    def __str__(self) -> str:
        """
        Get the string representation of the job object.

        Returns
        -------
        str
            String representation of the job object.
        """

        return "Job(id=%s, submit_time=%s, finish_time=%s, result=%s, data=%s)" % (self.id,
                                                                                   self.submit_time,
                                                                                   self.finish_time,
                                                                                   self._result,
                                                                                   self.data)

class JobManagement:
    """
    Class for managing all jobs of a certain kind (same job function).
    """

    jobs: dict[str : Job] = {}
    """ All managed jobs (indexed by their unique id). """

    @classmethod
    def get_unfinished_jobs(cls) -> set[str]:
        """
        Get a set containing the ids of all unfinished jobs.

        Returns
        -------
        set[str]
            A set containing the ids of all managed unfinished jobs.
        """

        unfinished_job_ids = set()
        for job_id, job in cls.jobs.items():
            if job.get_result() is None:
                unfinished_job_ids.add(job_id)
        logger.debug("There are currently %s unfinished jobs.", len(unfinished_job_ids))

        return unfinished_job_ids

    @classmethod
    def submit_job(cls, id: str, *args, **kwargs) -> str:
        """
        Submit a job. Id must be specified. Arguments are passed.

        Parameters
        ----------
        id : str
            The job id.
        *args
            Job arguments (passed to the job function).
        **kwargs Job keyword arguments (passed to the job function).

        Returns
        -------
        str
            The job id.
        """

        if id in cls.jobs:
            id = str(uuid.uuid4())
            logger.warning("Cannot submit job with already occupied id %s.\
                Choosing id of %s instead for submission.")
        cls.jobs[id] = Job(id, *args, **kwargs)
        return id

    @classmethod
    def query_job_completion(cls, id: str) -> Optional[bool]:
        """
        Get whether the specified job (via unique id) has already completed.

        Parameters
        ----------
        id : str
            Id of the job of interest.

        Returns
        -------
        Optional[bool]
            Whether the job has already completed or None, if id does not match an existing job.
        """

        job = cls.jobs.get(id, None)

        if job is None:
            logger.error("There is no job with requested id %s.", id)
            return None

        completed = not job.thread.is_alive()

        logger.debug("Queried job %s, which is %s.",
                     id, ("finished" if completed else "not yet finished"))

        return completed

    @classmethod
    def retrieve_job(cls, id: str) -> Optional[dict]:
        """
        Retrieve the result of a specified job or None, if it has not yet completed.

        Parameters
        ----------
        id : str
            The job id.

        Returns
        -------
        Optional[dict]
            The result of the job or None if it has not yet completed.
        """

        job = cls.jobs.get(id, None)

        if job is None:
            logger.error("There is no job with requested id %s.", id)
            return None

        result = job.get_result()

        if result is not None:
            cls.jobs.pop(id)
            logger.debug("Finished job %s has been removed from jobs successfully.", id)

        return result

    @classmethod
    def remove_older_jobs(cls, age: float) -> list[str]:
        """
        When called, removes all jobs that have completed at least a certain time ago.
        This should for example be called when a client reconnects to the RPC server after a crash.

        Parameters
        ----------
        age : float
            The minimum age of the jobs to remove in seconds.

        Returns
        -------
        list[str]
            The ids of the removed jobs.
        """

        job_ids = list(cls.jobs.keys())
        current_time = time.time()
        removed_jobs = []

        for job_id in job_ids:
            job = cls.jobs.get(job_id, None)
            if job is not None and job.finish_time is not None:
                job_age = current_time - job.finish_time
                if job_age > age:
                    cls.jobs.pop(job_id)
                    logger.info("Removed job with id %s on cleanup, \
                        since it was %s s old (max. allowed %s s).",
                        job_id, job_age, age)
                    removed_jobs += [job_id]

        return removed_jobs

def do_blocking_x(*args, **kwargs) -> any:
    """
    RPC function for executing the job function blockingly with the given arguments.

    Returns
    -------
    any
        Result of the job function

    Raises
    ------
    e
        Any occuring exception during the execution of the job function.
    """

    logger.debug("Executing job with input args = %s; input kwargs = %s", args, kwargs)
    try:
        result = Job.process_func(*args, **kwargs)
    except Exception as e:
        logger.error("Exception: %s", e)
        raise e
    logger.debug("Result: %s", result)

    return result

def submit_x(job_id: Optional[str], *args, **kwargs) -> str:
    """
    Submit a job.

    Parameters
    ----------
    job_id : Optional[str]
        Id of the job to submit. If None, an id is generated.

    Returns
    -------
    str
        The id of the job.
    """

    logger.debug("Submitting job with id = %s, input args = %s; input kwargs = %s",
                 job_id, args, kwargs)
    if job_id is None:
        job_id = str(uuid.uuid4())
        logger.info("Submitted job without id. Thus chose uuid %s.", job_id)
    try:
        result = JobManagement.submit_job(job_id, *args, **kwargs)
    except Exception as e:
        logger.error("Exception: %s", e)
        raise e
    logger.debug("Returning job id %s.", result)

    return [result]

def query_x_completion(job_id: str) -> bool:
    """
    Query whether the job with the given id has alredy completed.

    Parameters
    ----------
    job_id : str
        Job id.

    Returns
    -------
    Optional[bool]
        If job already has completed or None if id does not match a job.
    """

    logger.debug("Querying completion of job with id %s.", job_id)
    try:
        result = JobManagement.query_job_completion(job_id)
    except Exception as e:
        logger.error("Exception: %s", e)
        raise e
    logger.debug("Returning: %s", result)

    return result

def get_x_result(job_id: str) -> Optional[dict]:
    """
    Get the result of a job (if it has completed).
    On successfully returning a result, the job is removed from the internal job system.
    Therefore, each valid job result can only be retrieved once.

    Parameters
    ----------
    job_id : str
        Job id.

    Returns
    -------
    Optional[dict]
        Job result, if available. Otherwise, None.
    """

    logger.debug("Querying result of job with id %s", job_id)
    try:
        result = JobManagement.retrieve_job(job_id)
    except Exception as e:
        logger.error("Exception: %s", e)
        raise e
    logger.debug("Returning: %s", result)
    if result is None:
        logger.log(15, "Job result was requested, but is not yet ready.")

    return result

def remove_old_xs(age: float=3600) -> list[str]:
    """
    Removes all jobs, which completion is older than a specified minimum time.

    Parameters
    ----------
    age : float, optional
        The minimum age of a job (result) for the job to be removed, by default 3600

    Returns
    -------
    list[str]
        The ids of the removed jobs.
    """

    logger.debug("Requesting to remove all jobs older than %s seconds.", age)
    try:
        result = JobManagement.remove_older_jobs(age)
    except Exception as e:
        logger.error("Exception: %s", e)
        raise e
    logger.debug("Jobs that have been removed due to their age: %s", result)

    return result

LOG_FORMAT = "[%(asctime)s %(levelname)s %(funcName)s] %(message)s"

def configure_api(
        api,
        op_name: str,
        create_blocking_rpc_func: bool = True,
        create_info_rpc_func: bool = False,
        create_ping_rpc_func: bool = False,
        log_level: int = 25,
        ):
    """
    Configures an existing RPC server by adding the functions for a job system.

    Parameters
    ----------
    api : _type_
        The RPC server to configure.
    op_name : str
        The name of the operation this is about (as short as possible).
    create_blocking_rpc_func : bool, optional
        Whether to also create a blocking RPC function
        for executing the important function, by default True
    create_info_rpc_func : bool, optional
        Whether to also create an info RPC function, by default False
    create_ping_rpc_func : bool, optional
        Whether to also create a ping RPC function, by default False
    log_level : int, optional
        The log level to use, by default 25
    """

    logging.basicConfig(level=log_level, format=LOG_FORMAT, force=True)

    if create_blocking_rpc_func:
        api.add_function(do_blocking_x, "do_blocking_%s" % op_name)
    api.add_function(submit_x, "submit_%s" % op_name)
    api.add_function(query_x_completion, "query_%s_completion" % op_name)
    api.add_function(get_x_result, "get_%s_result" % op_name)
    api.add_function(remove_old_xs, "remove_old_%ss" % op_name)

    if create_info_rpc_func:
        @api.add_function
        def rpc_info():
            return api.rpc_info()

    if create_ping_rpc_func:
        @api.add_function
        def ping() -> float:
            return time.time()

@use_cmd_line_args
def run(addr: str, pub_key: str, name: str, pw: str):
    """
    Runs an example of an RPC server.

    Parameters
    ----------
    addr : str
        Address of the hermione switch, to which to connect the RPC server.
    pub_key : str
        String of public switch key.
    name : str
        Name of RPC server.
    pw : str
        Password of RPC server.
    """

    from RPC_server.backend.hermione_server import hermione_server

    pub_key = pub_key.encode()
    pw = pw.encode()

    log_level = 20

    api = hermione_server()
    api.init(addr, pub_key, log_level = log_level)

    configure_api(api, "test", log_level = log_level)

    api.serve(name, pw)

    logger.log(20, "Starting RPC Server for %s...", name)

def main():
    """
    Main function.
    """

    run()

if __name__ == "__main__":
    main()
