from ..lib.service import Service
from .helpers import FrameioHelpers


class Project(Service):
    def create(self, team_id, **kwargs):
        """
        Create a project.

        :Args:
          team_id (string): The team id.
        :Kwargs:
          kwargs (optional): additional request parameters.

          Example::

            client.projects.create(
              team_id="123",
              name="My Awesome Project"
            )
        """

        endpoint = "/teams/{}/projects".format(team_id)
        return self.client._api_call("post", endpoint, payload=kwargs)

    def get(self, project_id):
        """
        Get an individual project

        :Args:

          project_id (string): The project's id

        Example::

          client.project.get(
            project_id="123"
          )
        """

        endpoint = "/projects/{}".format(project_id)
        return self.client._api_call("get", endpoint)

    def tree(self, project_id, slim):
        """
        Fetch a tree representation of all files/folders in a project.

        :Args:
          project_id (string): The project's id
          slim (bool): If true, fetch only the minimum information for the following: \
            filename, \
            filesize, \
            thumbnail, \
            creator_id, \
            inserted_at (date created), \
            path (represented like a filesystem) \

          Example::

            client.projects.get(
              project_id="123",
              slim=True
            )
        """

        # endpoint = "/projects/{}/tree?depth=20&drop_includes=a.transcode_statuses,a.transcodes,a.source,a.checksums&only_fields=a.name,a.filesize,u.name,a.item_count,a.creator_id,a.inserted_at,a.uploaded_at".format(project_id)
        # return self.client._api_call('get', endpoint)

        return FrameioHelpers(self.client).build_project_tree(project_id, slim)

    def download(self, project_id, destination_directory="downloads"):
        """
        Download the provided project to disk.

        :Args:
          project_id (uuid): The project's id.
          destination_directory (string): Directory on disk that you want to download the project to.

          Example::

            client.projects.download(
              project_id="123",
              destination_directory="./downloads"
            )
        """

        return FrameioHelpers(self.client).download_project(
            project_id, destination=destination_directory
        )

    def get_collaborators(self, project_id, **kwargs):
        """
        Get collaborators for a project

        :Args:
          project_id (uuid): The project's id

          Example::

            client.projects.get_collaborators(
              project_id="123"
            )
        """

        endpoint = "/projects/{}/collaborators?include=project_role".format(project_id)
        return self.client._api_call("get", endpoint, kwargs)

    def get_pending_collaborators(self, project_id, **kwargs):
        """
        Get pending collaborators for a project

        :Args:
          project_id (uuid): The project's id

          Example::

            client.projects.get_pending_collaborators(
              project_id="123"
            )
        """

        endpoint = "/projects/{}/pending_collaborators".format(project_id)
        return self.client._api_call("get", endpoint, kwargs)

    def add_collaborator(self, project_id, email):
        """
        Add Collaborator to a Project Collaborator.

        :Args:
          project_id (uuid): The project id
          email (string): Email user's e-mail address

          Example::

            client.projects.add_collaborator(
              project_id="123",
              email="janedoe@frame.io",
            )
        """

        payload = {"email": email}
        endpoint = "/projects/{}/collaborators".format(project_id)
        return self._api_call("post", endpoint, payload=payload)

    def remove_collaborator(self, project_id, email):
        """
        Remove Collaborator from Project.

        :Args:
          project_id (uuid): The Project ID.
          email (string): The user's e-mail address

        Example::

          client.projects.remove_collaborator(
            project_id="123",
            email="janedoe@frame.io"
          )
        """

        endpoint = "/projects/{}/collaborators/_?email={}".format(project_id, email)
        return self._api_call("delete", endpoint)
