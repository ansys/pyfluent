.. _ref_file_transfer_guide:

File transfer
=============

PyFluent provides a file transfer service that manages how files are uploaded to and downloaded from the Fluent server.  
This service allows file-based API methods like `read_case()` and `write_mesh()` to work seamlessly—even when Fluent is running remotely, 
in a container, or in a PIM-managed environment.

Depending on how Fluent is launched, different file transfer strategies are available:

1. **PIM file transfer service**

   When launching Fluent through the `Product Instance Management (PIM) <https://pypim.docs.pyansys.com/version/stable/>`_ file transfer is fully automated.  
   You don’t need to call `upload()` or `download()`—files are transferred transparently when you use file-based API methods.

   Use this service when:

   - You launch Fluent using PIM.
   - You want seamless file transfers without needing to manage them directly.

   Example:

   .. code-block:: python

      >>> import ansys.fluent.core as pyfluent
      >>> from ansys.fluent.core import examples

      >>> case_file = examples.download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")

      >>> session = pyfluent.launch_fluent()
      >>> session.file.read_case(file_name=case_file)
      >>> session.file.write_case(file_name="write_mixing_elbow.cas.h5")


2. **Container file transfer service**

   When Fluent runs in a Docker container, files cannot be shared directly between client and server.  
   The remote file transfer service uses a gRPC-based mechanism to manage transfers.

   Use this service when:

   - Fluent is running in container mode.
   - You need to transfer files explicitly between environments.

   Example:

   .. code-block:: python

      >>> import ansys.fluent.core as pyfluent
      >>> from ansys.fluent.core import examples
      >>> from ansys.fluent.core.utils.file_transfer_service import ContainerFileTransferStrategy

      >>> case_file = examples.download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow", return_without_path=False)

      >>> file_transfer_service = ContainerFileTransferStrategy()
      >>> container_dict = {"mount_source": file_transfer_service.mount_source}
      >>> session = pyfluent.launch_fluent(file_transfer_service=file_transfer_service, container_dict=container_dict)
      >>> session.file.read_case(file_name=case_file)
      >>> session.file.write_case(file_name="write_mixing_elbow.cas.h5")


3. **Standalone file transfer service**

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

