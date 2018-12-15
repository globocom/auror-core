# Auror Core

Simple Flow creation for Azkaban

![auror](https://pm1.narvii.com/6278/52c20397d131f309c687f0baa5125968cf79aea3_hq.jpg)

## Install
```
pip install auror_core
```

## Usage

### Creating a simple Azkaban flow with one command 

You just need to import job type and project

```
from auror_core.v1.job import Job, Command
from auror_core import Project

com1 = Job()\
.as_type(Command)\
.with_name("commands job")\
.with_command("bash echo 1")\
.with_another_command("bash echo 2")

Project("folder_to_generate_files", com1).write()

```

### Creating a simple V2 Azkaban flow with one command 

V2 flow is implemented under v2 subfolder with same job types

```
from auror_core.v2.job import Job, Command
from auror_core import Project

com1 = Job()\
.as_type(Command)\
.with_name("commands job")\
.with_command("bash echo 1")\
.with_another_command("bash echo 2")

Project("folder_to_generate_files", com1).is_v2().write()

```

### Creating Flows with dependencies

```
from auror_core.v2.job import Job, Command
from auror_core import Project

com1 = Job()\
.as_type(Command)\
.with_name("commands job")\
.with_command("bash echo 1")\
.with_another_command("bash echo 2")

com2 = Command()\
.with_name("sub command job")\
.with_command("bash echo 1")\
.with_dependencies(com1)

Project("folder_to_generate_files", com1, com2).is_v2().write()

```

### Sharing job attributes

Organize jobs with same configuration

```
from auror_core.v2.job import Command
from auror_core import Project

com = Command()\
.with_command("bash echo 1")

com1 = com.with_name("commands job")\
.with_another_command("bash echo 2")

com2 = com.with_name("sub command job")\
.with_dependencies(com1)

Project("folder_to_generate_files", com1, com2).is_v2().write()

```

### Job with extra customization and configuration 

Simulating a Command with base Job (NOT RECOMMENDED)

```
from auror_core.v1.job import Job
from auror_core import Project

com1 = Job()\
.with_name("commands job")\
.with_(command="bash echo 1")

com1._type = "command"

Project("folder_to_generate_files", com1).write()

```

### Integrating with Flow (just for V1)

V2 already have flow included

```
from auror_core.v1.job import Command, Flow, Job
from auror_core import Project

com1 = Command()\
.with_name("commands job")\
.with_command("bash echo 1")

flow = Job()\
.as_type(Flow)\
.with_name("flow")\
.with_dependencies(com1)

Project("folder_to_generate_files", com1, flow).write()

```

### Using Flow Params

```
from auror_core.v2.job import Command
from auror_core.v2.params import Params
from auror_core import Project

params = Params(
    teste1="my test",
    variable="my variable"
)

com = Command()\
.with_command("bash echo ${variable}")

Project("folder_to_generate_files", com)\
.is_v2()\
.with_params(params)\
.write()

```

### Using Flow Environment Variables


```
from auror_core.v2.job import Command
from auror_core.v2.params import Env
from auror_core import Project

env = Env(
    TESTE="my test",
    VARIABLE="my variable"
)

com = Command()\
.with_command("bash echo $VARIABLE")

Project("folder_to_generate_files", com)\
.is_v2()\
.with_params(env)\
.write()

```

### Using Flow Environment Variables and Params


```
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

com = Command()\
.with_command("bash echo $VARIABLE ${variable}")

Project("folder_to_generate_files", com)\
.is_v2()\
.with_params(params, env)\
.write()

```

### Join multiple variables in one

```
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

com = Command()\
.with_command("bash echo ${params_strange_name}") 
## it will print: my test,my variable,env test,env variable
## THERE IS NO ORDER GUARANTEE, JUST Python 3.6 >

Project("folder_to_generate_files", com)\
.is_v2()\
.with_params(one_param(params, env))\
.write()

```

## Plugins

Plugins are just extensions from auror_core

There is a cookiecutter for new azkaban jobtypes with Auror template too: https://github.com/globocom/azkaban-jobtype-cookiecutter

We already have email plugin: https://github.com/globocom/azkaban-jobtype-email
