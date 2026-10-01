.. _ref_logging_guide:

Logging
=======

PyFluent uses the logging API provided by the Python standard library. You can
find out more about `Python logging here <https://www.python.org/downloads/>`_.
PyFluent provides multiple loggers and packages a logging_config.yaml in the standard
format which you can edit to configure logging according to your requirements.

PyFluent has an option to run with logging enabled. This command enables logging:

.. code:: python

  >>> import ansys.fluent.core as pyfluent
  >>> pyfluent.diagnostics.logger.enable()


You can set the global logging level using the following command:

.. code:: python

  >>> pyfluent.diagnostics.logger.set_global_level('DEBUG')


You can also configure logging to a file. Here is an example that shows how to do this:

.. code:: python
    
  >>> config_dict = pyfluent.diagnostics.logger.get_default_config()
  >>> config_dict['handlers']['pyfluent_file']['filename'] = 'test.log'
  >>> pyfluent.diagnostics.logger.enable(custom_config=config_dict)


You can list all available loggers and set the logging level for a specific logger using the following commands:

.. code:: python

  >>> pyfluent.diagnostics.logger.list_loggers()
  >>> logger = pyfluent.diagnostics.logger.get_logger('pyfluent.networking')
  >>> logger.setLevel('ERROR')

