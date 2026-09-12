.. _ref_file_transfer_guide:

File transfer
=============

The file transfer service enables you to upload files to the server and download files from it. You have the option to specify 
a different name for the file being uploaded; if you do not, the default name is that of the file being uploaded. 
Similarly, when downloading a file from the server, you can indicate a specific download directory; if not specified, 
the file is saved in the current working directory. You can define your own file transfer service and utilize it with 
launch_fluent(file_transfer_service=<name_of_the_file_transfer_service>).

The following file transfer services are available:

#. **Local file transfer service**:

   * The :ref:`Local file transfer service <ref_file_transfer_service>` is suitable for Fluent when launched in standalone mode.

#. **Remote file transfer service**:

   * The :ref:`Remote file transfer service <ref_file_transfer_service>` utilizes the `gRPC client <https://filetransfer.tools.docs.pyansys.com/version/stable/>`_ and `gRPC server <https://filetransfer-server.tools.docs.pyansys.com/version/stable/>`_.
   * This service can be employed for Fluent when launched in container mode.

#. **PIM file transfer service**:

   * The :ref:`PIM file transfer service <ref_file_transfer_service>` utilizes the `PIM <https://pypim.docs.pyansys.com/version/stable/>`_.
   * This service is the default for Fluent when launched in a PIM-configured environment.

Examples
--------

.. code-block:: python

   >>> import ansys.fluent.core as pyfluent
   >>> from ansys.fluent.core import examples
   >>> from ansys.fluent.core.utils.file_transfer_service import LocalFileTransferStrategy, RemoteFileTransferStrategy

   >>> case_file_name = examples.download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
   >>> mesh_file_name = examples.download_file("mixing_elbow.msh.h5", "pyfluent/mixing_elbow")

   >>> # Local file transfer service
   >>> meshing_session = pyfluent.launch_fluent(mode=pyfluent.FluentMode.MESHING, file_transfer_service=LocalFileTransferStrategy())
   >>> meshing_session.upload(file_name=mesh_file_name, remote_file_name="elbow.msh.h5")
   >>> meshing_session.meshing.File.ReadMesh(FileName="elbow.msh.h5")
   >>> meshing_session.meshing.File.WriteMesh(FileName="write_elbow.msh.h5")
   >>> meshing_session.download(file_name="write_elbow.msh.h5", local_directory="<local_directory_path>")

   >>> # Remote file transfer service
   >>> solver_session = pyfluent.launch_fluent(mode=pyfluent.FluentMode.SOLVER, file_transfer_service=RemoteFileTransferStrategy())
   >>> solver_session.upload(file_name=case_file_name, remote_file_name="elbow.cas.h5")
   >>> solver_session.file.read_case(file_name="elbow.cas.h5")
   >>> solver_session.file.write_case(file_name="write_elbow.cas.h5")
   >>> solver_session.download(file_name="write_elbow.cas.h5", local_directory="<local_directory_path>")

   >>> # PIM file transfer service
   >>> solver_session = pyfluent.launch_fluent(mode=pyfluent.FluentMode.SOLVER)
   >>> solver_session.upload(file_name=case_file_name, remote_file_name="elbow.cas.h5")
   >>> solver_session.file.read_case(file_name="elbow.cas.h5")
   >>> solver_session.file.write_case(file_name="write_elbow.cas.h5")
   >>> solver_session.download(file_name="write_elbow.cas.h5", local_directory="<local_directory_path>")

