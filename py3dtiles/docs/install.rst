Install
-------

From pypi
~~~~~~~~~~~~

`py3dtiles` is published on pypi.org.

```
pip install py3dtiles
```

From docker
~~~~~~~~~~~~

We currently publish docker images on gitlab registry. Please see [the currently published versions](https://gitlab.com/Oslandia/py3dtiles/container_registry/4248842).
```
docker run --rm registry.gitlab.com/oslandia/py3dtiles:<version> --help
```


NOTE:

- the `--mount` option is necessary for docker to read your source data and to write the result. The way it is written in this example only allows you to read source files in the current folder or in a subfolder
- This line `--volume /etc/passwd:/etc/passwd:ro --volume /etc/group:/etc/group:ro --user $(id -u):$(id -g)` is only necessary if your uid is different from 1000.

From sources
~~~~~~~~~~~~

To use py3dtiles from sources:

.. code-block:: shell

    $ apt install git python3 python3-pip virtualenv
    $ git clone git@gitlab.com:Oslandia/py3dtiles.git
    $ cd py3dtiles
    $ virtualenv -p python3 venv
    $ . venv/bin/activate
    (venv)$ pip install .

If you want to run unit tests:

.. code-block:: shell

    (venv)$ pip install -e .[dev]
    (venv)$ pytest


Supporting LAZ files
~~~~~~~~~~~~~~~~~~~~

To support laz files you need an external library and a laz backend for
laspy, see [this link]](https://laspy.readthedocs.io/en/latest/installation.html#pip). Short answer, for laszip, you need to follow these steps:

.. code-block:: shell

  $ # install liblaszip, for instance on ubuntu 22.04
  $ apt-get install -y liblaszip8

  $ # Install with LAZ support via laszip
  $ pip install laspy[laszip]
