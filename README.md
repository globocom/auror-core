Repositório de criação de Jobs para o Azkaban
----------------------------------------------

Projeto criado em python para facilitar a criação de jobs do AirFlow para o Azkaban.

**Guia do Usuário:** [user-guide](http://docs-bigdata.cloud.globoi.com/cluster/azkaban/user-guide/)
**Parâmetros Globais:** [global](http://docs-bigdata.cloud.globoi.com/cluster/azkaban/global/)

#### GLOSSÁRIO

* **Job**
	- Job é um processo que se deseja executar em Azkaban. Eles podem ser configurados para depender de outros jobs. A criação de propriedades do job deve ser feita em um arquivo com extensão `.job`.
* **flow**
	- Fluxo é um conjunto de jobs que depende um do outro. Suas dependências sempre são executadas antes que o próprio job possa ser executado.
* **type**
	- É definido um tipo de job a ser executado no fluxo. Ele pode ser command, python, flow, entre outros.
* **command**
	- Parâmetro de tipo de job mais comum, que permite executar uma linha de comando. Ela pode definir comandos subsequentes adicionando o sufixo .1, .2, etc.
* **python**
	- Outro tipo de job que permite a instalação e uso de pacotes python em um projeto. Para utilizá-lo, basta passar, através de parâmetros, o nome da virtualenv, o arquivo de requirements e o python desejado.
* **email**
    - É um tipo de job que permite o envio de emails de forma simples e configurável. Pode ser definido o assunto do email, o corpo do email e os destinatários. O uso do parâmetro `send` igual a **false** permite que o email não seja enviado ao destinatário.
* **name**
	- A ser definido como nome do job.
* **dependencies**
	- Parâmetro que utiliza uma lista de nomes de arquivos de job (separada por vírgulas).
* **Params**
	- Permite adicionar parâmetros que podem ser definidos, herdados e sobrescritos, sendo criadas em outro arquivo `.properties`. Além dos parâmetros `type` e `dependencies`, existem outros parâmetros que o Azkaban reserva para todos os jobs.
* **ParamsJoin**
	- Permite adicionar em uma linha todos os parâmetros desejados (variáveis de ambiente, por exemplo) usando um separador para cada configuração de um parâmetro, sendo criadas em outro arquivo `.properties`.
* **properties**
	- O job do Azkaban é especificado com um conjunto de pares de valores-chave chamado de **properties**, que farão parte da execução do job.
	- Os parâmetros de propriedades do job não precisam, necessariamente, ser definidos dentro do arquivo `.job` que está usando ele, podendo estar em um arquivo `.properties`, por exemplo. Este arquivo também deve estar no projeto e em nível de diretório igual ou mais alto.
* **args**
	- Parâmetro que permite passar os argumentos que são declarados no seu projeto Job (scala).
* **Spark**
	- Permite alterar o valor dos parâmetros definidos em spark-submit.
* **SparkExecutor**
	- Permite adicionar nome e valor da propriedade _spark.executorEnv_.
* **SparkDriver**
	- Permite adicionar nome e valor da propriedade _spark.yarn.appMasterEnv_.
* **Project**
	- Fará a criação de arquivos como `.job`, `.properties`, entre outros, dentro do path do diretório que foi definido (este diretório precisa estar criado).
* **retries**
	- Número de tentativas que serão automaticamente repetidas para tarefas com falha.
* **retry.backoff**
	- Tempo de milisegundos entre cada tentativa de repetição.
* **failure.emails**
	- Lista e-mails a serem notificados durante uma falha.
* **extra**
	- Utilizado para definir o valor passado a um parâmetro necessário para spark-submit.

#### Observações:

* É preciso chamar no job a variável de __spark-submit__. Caso nele seja definido o parâmetro **extra.jars**, utilize a variável **${spark.submit.extra.jars}**. Caso contrário, utilize **${spark.submit}**. 
* Os parâmetros declarados em seu projeto Job (scala) podem ser passados no seu job em forma de argumento (basta usar a função `with_args` no tipo Spark) ou de variável de ambiente.
* Caso queira que a configuração spark `dynamicAllocation` seja habilitada, basta usar a função `with_dynamic_allocation` passando como parâmetros os valores desejados para __min_executors__ e __max_executors__. Os parâmetros `conf.spark.dynamicAllocation.enabled`, `min_executors` e `max_executors` serão criados.
* Caso queira definir o número de executores, basta usar a função `with_num_executors` passando o valor desejado. Porém, se apenas esta função for definida, sem estabelecer a alocação dinâmica (caso acima), o parâmetro `conf.spark.dynamicAllocation.enabled` terá como valor padrão **False**.

#### Como usar
1. Primeiro, é preciso instalar o _pacote auror_ que será utilizado no projeto:

    `$ pip install auror --index-url=https://artifactory.globoi.com/artifactory/api/pypi/pypi-all/simple`

2. Em seu script python, importe a **biblioteca auror** para utilizar as classes necessárias para criação do seu job.
3. Ao executar o script python, será criado os arquivos .job, .properties, .py, por exemplo, dentro do path do diretório definido: `$ python {creation_job}.py`.

    **Obs.**: Esse diretório já precisa ser criado antes de executar o script python, pois os arquivos serão criados nesse path.

4. Será preciso compactar (.zip) essa pasta com todos os arquivos que serão usados pelo projeto, sejam eles .job, .properties, .py, entre outros.
5. Em seguida, faça o _upload_ desse arquivo compactado no Azkaban.

#### Release

Última versão está no arquivo version.txt

    $ make release VERSION=0.0.0   # sua versão no lugar de 0.0.0

#### Exemplo de criação do job com variáveis de ambiente

```
from auror.job import Job, Spark, Project, Command
from auror.params import Params, ParamsJoin, SparkDriver

## Propriedades disponíveis para todos os jobs ##

params = Params(
    "params",
    retries="{retries-value}",
    **{
        "retry.backoff": "{retry-backoff-value}",
        "failure.emails": "{e-mail}"
    }
)

driver_envs = SparkDriver(
    "driver_envs",
    PROXY_HOST = "{proxy-host}",
    PROXY_PORT = "{proxy-port}"
)

## Definição do Job ##

default_job = Job() \
    .as_type(Spark) \
    .with_name("{name-job-to-azkaban}") \
    .with_hadoop_user("{username}") \
    .with_spark_version("{spark-version}") \
    .with_queue() \
    .with_driver_memory("{driver-memory}") \
    .with_executor_memory("{executor-memory}") \
    .with_executor_cores("{executor-cores}") \
    .with_dynamic_allocation("{min-executors}", "{max-executors}") \
    .with_jar_file("{jar-file}") \
    .with_java_class("{java-class}") \
    .with_extra_jars("{extra-jars}")

Project("{job-folder-name}",
  default_job
).with_params(ParamsJoin()(driver_envs), params).write()
```

```
# Representação do diretório ao criar o diretório contendo o job

project/
├── script-to-create-job.py
├── job-folder-name/
├── ├── driver_envs.properties
├── ├── name-job-to-azkaban.job
├── ├── params.properties
```

#### Exemplo de criação do job usando extra_jars e passando argumentos (parâmetro `args`)

```
from auror.job import Job, Spark, Project, Command
from auror.params import Params

## Propriedades disponíveis para todos os jobs ##

params = Params(
    "params",
    retries="{retries-value}",
    **{
        "retry.backoff": "{retry-backoff-value}",
        "failure.emails": "{e-mail}"
    }
)

## Definição do Job ##

default_job = Job() \
    .as_type(Spark) \
    .with_hadoop_user("{username}") \
    .with_spark_version("{spark-version}") \
    .with_queue() \
    .with_name("{name-job-to-azkaban}") \
    .with_java_class("{java_class}") \
    .with_extra_jars("{extra_jars}") \
    .with_args("arg-1 arg-2") \
    ( .... )

Project("{job-folder-name}",
  default_job
).with_params(params).write()
```
