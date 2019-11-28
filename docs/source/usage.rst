 .. Licensed to the Apache Software Foundation (ASF) under one
    or more contributor license agreements.  See the NOTICE file
    distributed with this work for additional information
    regarding copyright ownership.  The ASF licenses this file
    to you under the Apache License, Version 2.0 (the
    "License"); you may not use this file except in compliance
    with the License.  You may obtain a copy of the License at

 ..   http://www.apache.org/licenses/LICENSE-2.0


Usage
=============

V1
--


Simple Azkaban flow
'''''''''''''''''''

You just need to import job type and project

.. code:: python

    from auror_core.v1.job import Job, Command
    from auror_core import Project

    com1 = Job()\
        .as_type(Command)\
        .with_name("commands job")\
        .with_command("bash echo 1")\
        .with_another_command("bash echo 2")

    Project("folder_to_generate_files", com1).write()


Job with extra customization and configuration
''''''''''''''''''''''''''''''''''''''''''''''

Simulating a Command with base Job (NOT RECOMMENDED)

.. code:: python

    from auror_core.v1.job import Job
    from auror_core import Project

    com1 = Job()\
        .with_name("commands job")\
        .with_(command="bash echo 1")

    com1._type = "command"

    Project("folder_to_generate_files", com1).write()


Integrating with Flow
'''''''''''''''''''''

V2 already have flow included

.. code:: python

    from auror_core.v1.job import Command, Flow, Job
    from auror_core import Project

    com1 = Command() \
        .with_name("commands job") \
        .with_command("bash echo 1")

    flow = Job() \
        .as_type(Flow) \
        .with_name("flow") \
        .with_dependencies(com1)

    Project("folder_to_generate_files", com1, flow).write()


V2
--


Simple V2 Azkaban flow
''''''''''''''''''''''

V2 flow is implemented under v2 subfolder with same job types

.. code:: python

    from auror_core.v2.job import Job, Command
    from auror_core import Project

    com1 = Job() \
        .as_type(Command) \
        .with_name("commands job") \
        .with_command("bash echo 1") \
        .with_another_command("bash echo 2")

    Project("folder_to_generate_files", com1).is_v2().write()


Flows with dependencies
'''''''''''''''''''''''

.. code:: python

    from auror_core.v2.job import Job, Command
    from auror_core import Project

    com1 = Job() \
        .as_type(Command) \
        .with_name("commands job") \
        .with_command("bash echo 1") \
        .with_another_command("bash echo 2")

    com2 = Command() \
        .with_name("sub command job") \
        .with_command("bash echo 1") \
        .with_dependencies(com1)

    Project("folder_to_generate_files", com1, com2).is_v2().write()


Sharing job attributes
''''''''''''''''''''''

Organize jobs with same configuration

.. code:: python

    from auror_core.v2.job import Command
    from auror_core import Project

    com = Command() \
        .with_command("bash echo 1")

    com1 = com.with_name("commands job") \
        .with_another_command("bash echo 2")

    com2 = com.with_name("sub command job") \
        .with_dependencies(com1)

    Project("folder_to_generate_files", com1, com2).is_v2().write()


Using Flow Params
'''''''''''''''''

.. code:: python

    from auror_core.v2.job import Command
    from auror_core.v2.params import Params
    from auror_core import Project

    params = Params(
        teste1="my test",
        variable="my variable"
    )

    com = Command() \
        .with_command("bash echo ${variable}")

    Project("folder_to_generate_files", com) \
        .is_v2() \
        .with_params(params) \
        .write()


Using Flow Environment Variables
''''''''''''''''''''''''''''''''

.. code:: python

    from auror_core.v2.job import Command
    from auror_core.v2.params import Env
    from auror_core import Project

    env = Env(
        TESTE="my test",
        VARIABLE="my variable"
    )

    com = Command() \
        .with_command("bash echo $VARIABLE")

    Project("folder_to_generate_files", com) \
        .is_v2() \
        .with_params(env) \
        .write()


Using Flow Environment Variables and Params
'''''''''''''''''''''''''''''''''''''''''''

.. code:: python

    from auror_core.v2.job import Command
    from auror_core.v2.params import Env, Params
    from auror_core import Project

    env = Env(
        TESTE="my test",
        VARIABLE="my variable"
    )

    params = Params(
        teste1="my test",
        variable="my variable"
    )

    com = Command() \
        .with_command("bash echo $VARIABLE ${variable}")

    Project("folder_to_generate_files", com) \
        .is_v2() \
        .with_params(params, env) \
        .write()


Join multiple variables in one
''''''''''''''''''''''''''''''

.. code:: python

    from auror_core.v2.job import Command
    from auror_core.v2.params import Env
    from auror_core import Project

    env = Env(
        TESTE="env test",
        VARIABLE="env variable"
    )

    params = Params(
        teste1="my test",
        variable="my variable"
    )

    one_param = ParamsJoin("params_strange_name", ",") ## param name and separator

    com = Command() \
        .with_command("bash echo ${params_strange_name}") 
    ## it will print: my test,my variable,env test,env variable
    ## THERE IS NO ORDER GUARANTEE, JUST Python 3.6 >

    Project("folder_to_generate_files", com) \
        .is_v2() \
        .with_params(one_param(params, env)) \
        .write()


Load jobs from YAML File
''''''''''''''''''''''''

You can find some YAML File examples on `Azkaban Flow Documentation`__

.. __: https://github.com/azkaban/azkaban/wiki/Azkaban-Flow-2.0-Design#flow-yaml-file

.. code:: python

    from auror_core.v2.loader import Loader

    loader = Loader('/path/to/file/flow.yaml')
    jobs = loader.as_job_objects()

Or you can export these jobs as a Python File

.. code:: python

    from auror_core.v2.loader import Loader

    loader = Loader('/path/to/file/flow.yaml')
    jobs = loader.as_python_file('/path/to/desired/directory') # will be dumped with 'flow.py' name


Dump memory flows to a Python File
''''''''''''''''''''''''''''''''''

.. code:: python

    from auror_core.v2.dumper import Dumper

    com1 = Job() \
        .with_name("commands job 1") \
        .with_(command="bash echo 1")

    com2 = Job() \
        .with_name("commands job 2") \
        .with_(command="bash echo 2")

    dumper = Dumper('/path/to/desired/directory') # will be dumped with 'flow.py' name
    dumper.dump_jobs(com1, com2)
