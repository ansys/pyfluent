.. _ref_file_transfer_guide:

File transfer
=============

PyFluent provides a file transfer service that manages how files are uploaded to and downloaded from the Fluent server.  
This service allows file-based API methods like `read_case()` and `write_mesh()` to work seamlessly.

* **Standalone file transfer service**

   When Fluent is launched in standalone mode on the same machine as the Python client, files can be accessed directly from the local file system. 
   In this case, the local file transfer service is used.

   Use this service when:

   - Fluent is running locally.
   - You want to ensure explicit control over file movement using `upload()` and `download()`.

   Example:

   .. code-block:: python

      >>> import ansys.fluent.core as pyfluent
      >>> from ansys.fluent.core import examples
      >>> from ansys.fluent.core.utils.file_transfer_service import StandaloneFileTransferStrategy

      >>> mesh_file = examples.download_file("mixing_elbow.msh.h5", "pyfluent/mixing_elbow")

      >>> session = pyfluent.launch_fluent(mode=pyfluent.FluentMode.MESHING, file_transfer_service=StandaloneFileTransferStrategy())
      >>> session.upload(file_name=mesh_file, remote_file_name="elbow.msh.h5")
      >>> session.meshing.File.ReadMesh(FileName="elbow.msh.h5")
      >>> session.meshing.File.WriteMesh(FileName="write_elbow.msh.h5")
      >>> session.download(file_name="write_elbow.msh.h5", local_directory="<local_path>")

