"""
Implement examples for a Hammerspace workflow including

This will show how to:
- Create an attribute via the API
- Load an attribute via the API
- Create a listener by binding a callback to a topic
- Start listening for message
- Handle a ftrack.update message by filtering and dispatching them
- Use the location system to load the paths of component in central storage
- Manually build paths to central storage with support from the location system

Once you run the script, you'll have two new hs_location attributes on Task and
AssetVersion entity types. When you set values on these attributes for records,
the listener will get the update messages and will print the paths to the
console. This would be replaced with Hammerspace metadata modification calls.
"""

import logging
import sys

import json
import dotenv

import ftrack_api


def main():
    """
    Main script entry point

    This relies on dot env and the information for the ftrack connection being
    in the .env file
    """
    dotenv.load_dotenv()

    app = HammerspaceIntegration()
    app.create_hs_attribute_on_entity("task", "Task")
    app.create_hs_attribute_on_entity("assetversion")
    app.register_trigger()
    app.listen()


class HammerspaceIntegration:
    """
    This class represents our integration
    """

    def __init__(self):
        self._logger = self._setup_logging(logging.DEBUG)
        self._logger.debug("Initialized")

        # The initialization of the API also initializes the event hub because this
        # example also sets up triggers and actions.
        # https://ftrack-python-api.rtd.ftrack.com/en/stable/api_reference/session.html#ftrack_api.session.Session
        self._session = ftrack_api.Session(auto_connect_event_hub=True)

        # Get the central storage location
        self._location = self._session.pick_location()
        if self._location is None:
            raise RuntimeError("No central storage location found.")

    def create_hs_attribute_on_entity(
        self, entity_type: str, object_type_name: str | None = None
    ):
        """
        Create a Hammerspace attribute on an entity type.
        Make sure it doesn't already exist first.
        """
        # See this doc page for the interplay between these two args and the validations
        # taking place
        # https://ftrack-python-api.readthedocs.io/en/stable/example/manage_custom_attribute_configuration.html#entity-types
        if entity_type == "task" and object_type_name is None:
            raise ValueError(
                'If the entity_type argument is "task" an object_type_name argument is required.'
            )

        if entity_type != "task" and object_type_name is not None:
            self._logger.warning(
                "The object_type_name argument will be ignored when creating the attribute because "
                "the entity_type attribute is not task."
            )

        config = json.dumps(
            {
                "multiSelect": True,
                "data": json.dumps(
                    [
                        {"value": "yul", "menu": "Montreal"},
                        {"value": "lax", "menu": "Los Angeles"},
                        {"value": "yyz", "menu": "Toronto"},
                        {"value": "muc", "menu": "Munich"},
                    ]
                ),
            }
        )
        attribute = self._get_hs_attribute(entity_type, object_type_name)

        if attribute:
            if attribute["config"] != config:
                attribute["config"] = config
        else:
            security_roles = self._get_security_roles()
            data = {
                "entity_type": entity_type,
                "type": self._get_custom_attribute_type("enumerator"),
                "label": "Hammerspace Location",
                "key": "hs_location",
                "config": config,
                "write_security_roles": security_roles,
                "read_security_roles": security_roles,
            }

            if object_type_name:
                data["object_type"] = self._get_object_type(object_type_name)

            attribute = self._session.create("CustomAttributeConfiguration", data)

        self._session.commit()

    def register_trigger(self) -> None:
        """
        Setup a listener for handling hs_location changes for a certain entity type
        """
        self._logger.info("Setting up callback.")
        self._session.event_hub.subscribe(
            "topic=ftrack.update",
            self._handle_hs_location_change,
        )

    def listen(self):
        """
        Let the API handle listening infinitely for messages from ftrack and dispatch
        them to previously setup callbacks.
        """
        # https://ftrack-python-api.rtd.ftrack.com/en/stable/api_reference/event/hub.html#ftrack_api.event.hub.EventHub.wait
        self._session.event_hub.wait()

    def _handle_hs_location_change(self, event: ftrack_api.event.base.Event):
        """
        Process an event for an hs_location attribute changing on something.

        An example event will look as follows:

        {
            "id": "d57afc635193420b9c4a357df3894c04",
            "data": {
                "entities": [
                    {
                        "entity_type": "Task",
                        "keys": ["hs_location"],
                        "objectTypeId": "11c137c0-ee7e-4f9c-91c5-8c77cec22b2c",
                        "entityType": "task",
                        "parents": [
                            {
                                "entityId": "ecc077e8-8475-11ec-9a8b-8e5ff4a86448",
                                "entityType": "task",
                                "entity_type": "Task",
                                "parentId": "ecbcae1a-8475-11ec-9a8b-8e5ff4a86448",
                            },
                            {
                                "entityId": "ecbcae1a-8475-11ec-9a8b-8e5ff4a86448",
                                "entityType": "task",
                                "entity_type": "Shot",
                                "parentId": "c68ba6e6-7585-11ec-88c9-f6749bb4bf64",
                            },
                            {
                                "entityId": "c68ba6e6-7585-11ec-88c9-f6749bb4bf64",
                                "entityType": "task",
                                "entity_type": "Sequence",
                                "parentId": "c32bcad8-98c8-11ec-ae9e-e61c2077ba79",
                            },
                            {
                                "entityId": "c32bcad8-98c8-11ec-ae9e-e61c2077ba79",
                                "entityType": "task",
                                "entity_type": "Episode",
                                "parentId": "896b8ea8-6fe4-11ec-824d-3e6e0ed5ae4e",
                            },
                            {
                                "entityId": "896b8ea8-6fe4-11ec-824d-3e6e0ed5ae4e",
                                "entityType": "show",
                                "entity_type": "Project",
                                "parentId": None,
                            },
                        ],
                        "parentId": "ecbcae1a-8475-11ec-9a8b-8e5ff4a86448",
                        "action": "update",
                        "entityId": "ecc077e8-8475-11ec-9a8b-8e5ff4a86448",
                        "changes": {"hs_location": {"new": "yul", "old": ""}},
                    }
                ],
                "pushToken": "82114452360b11ed8045c2d54ad10e71",
                "parents": [
                    "c32bcad8-98c8-11ec-ae9e-e61c2077ba79",
                    "ecc077e8-8475-11ec-9a8b-8e5ff4a86448",
                    "c68ba6e6-7585-11ec-88c9-f6749bb4bf64",
                    "ecbcae1a-8475-11ec-9a8b-8e5ff4a86448",
                    "896b8ea8-6fe4-11ec-824d-3e6e0ed5ae4e",
                ],
                "user": {
                    "userid": "bcdf57b0-acc6-11e1-a554-f23c91df1211",
                    "name": "Patrick+Admin Boucher",
                },
                "clientToken": "8149e600-360b-11ed-8045-c2d54ad10e71-1663365856721",
            },
            "topic": "ftrack.update",
            "sent": None,
            "source": {
                "clientToken": "8149e600-360b-11ed-8045-c2d54ad10e71-1663365856721",
                "applicationId": "ftrack.client.web",
                "user": {
                    "username": "patrick.boucher@ftrack.com",
                    "id": "bcdf57b0-acc6-11e1-a554-f23c91df1211",
                },
                "id": "8149e600-360b-11ed-8045-c2d54ad10e71-1663365856721",
            },
            "target": "",
            "in_reply_to_event": None,
        }
        """
        for entity in event.get("data", {}).get("entities", []):
            if "hs_location" not in entity.get("keys", []):
                continue

            entity_type = entity.get("entity_type")
            func_name = f"_handle_{entity_type.lower()}_change"
            func = getattr(self, func_name, None)
            if func is not None:
                func(entity)
            else:
                self._logger.warning("No handler for entity type %s", entity_type)
                # TODO: Revert the attribute change because we've not taken action on it.

        # If you want a trigger to return a notification you can do so by returning
        # a structure from the trigger itself.
        return {"success": True, "message": "Marked objects with Hammerspace metadata"}

    def _handle_task_change(self, event_entity: dict):
        """
        Handle what should happen when a task changes.

        A task in this context is the old legacy entity type. A task is any
        object defined in the GUI in the Workflow -> Objects section.

        In this case we'll get the entity and build its path based on its link
        attribute which is a list of parent entities.

        The default implementation of a structure in
        ftrack_api.structure.standard.StandardStructure (which is what is used
        by default for central storage locations) does not support anyting other
        than components so we need to do the path building ourselves.
        """
        entity = self._session.query(
            f"select link from {event_entity['entity_type']} where id = {event_entity['entityId']}"
        ).first()
        if entity is None:
            return

        links = entity["link"]
        project = self._session.get("Project", links[0]["id"])
        if project is None:
            raise RuntimeError("Could not find project for task")

        parts = [project["name"]]
        parts.extend([link["name"] for link in links[1:-1]])

        path = self._location.structure.path_separator.join(
            [self._location.structure.sanitise_for_filesystem(part) for part in parts]
        )
        path = self._location.accessor.get_filesystem_path(path)

        value = event_entity["changes"]["hs_location"]
        self._mark_in_hammerspace(path, value["old"], value["new"])

    def _handle_assetversion_change(self, event_entity: dict):
        """
        Handle what should happen when an asset version changes.

        In this case we'll go get all the components for a given asset version
        and see if any are on the central storage location. If so, we'll get
        their paths and mark them in Hammerspace.

        The default implementation of a structure in
        ftrack_api.structure.standard.StandardStructure (which is what is used
        by default for central storage locations) supports Components so we can
        use that to get the paths.

        :param event_entity: The entity that was changed as described in the event
        """
        entity = self._session.query(
            f"select components from {event_entity['entity_type']} where id = {event_entity['entityId']}"
        ).first()
        if entity is None:
            return

        value = event_entity["changes"]["hs_location"]

        processed = False
        components = entity["components"]
        availabilities = self._location.get_component_availabilities(components)
        for index, component in enumerate(components):
            availability = availabilities[index]
            if availability == 0.0:
                # TODO: Revert the attribute change because we've not taken action on it.
                continue

            path = self._location.get_filesystem_path(component)
            self._mark_in_hammerspace(path, value["old"], value["new"])
            processed = True

        if not processed:
            self._logger.debug("No components found on central storage location")

    def _mark_in_hammerspace(self, path: str, old_value: str, new_value: str):
        """
        Mark a path in Hammerspace with the appropriate metadata.

        Depending on what the old and new values are, the actual action in
        Hammerspace may be different.

        :param path: The path to mark in Hammerspace
        :param old_value: The old value of the hs_location ftrack attribute
        :param new_value: The new value of the hs_location ftrack attribute
        """
        # TODO: Actually mark the path in Hammerspace with the appropriate metadata.
        self._logger.info("%s : %s -> %s", path, old_value, new_value)

    # ------------------------------------- #
    # Helper methods for attribute creation #
    # ------------------------------------- #

    def _get_hs_attribute(
        self,
        entity_type: str,
        object_type_name: str | None,
    ) -> ftrack_api.entity.base.Entity | None:
        """
        Get an existing HS attribute.

        :param entity_type: The entity type to get the attribute for
        :param object_type_name: The object type name to get the attribute for
            if the entity type is 'task'

        :return: The attribute if it exists, otherwise None
        """
        query = (
            "select config from "
            "CustomAttributeConfiguration where "
            "key is hs_location and "
            "type.name is enumerator and "
            f"entity_type is {entity_type}"
        )

        if object_type_name is not None:
            query += f" and object_type.name is {object_type_name}"

        return self._session.query(query).first()

    def _get_custom_attribute_type(
        self,
        attribute_type_name: str,
    ) -> ftrack_api.entity.base.Entity:
        """
        Given an attribute type's name, return the object. This is to support the
        creation of CustomAttributeConfiguration objects

        :param attribute_type_name: The name of the attribute type

        :return: The attribute type object
        """
        return self._session.query(
            f"CustomAttributeType where name is {attribute_type_name}"
        ).one()

    def _get_object_type(self, object_type_name: str) -> ftrack_api.entity.base.Entity:
        """
        Given an object type's name, return the object. This is to support the
        creation of CustomAttributeConfiguration objects

        :param object_type_name: The name of the object type record

        :return: The object type record
        """
        return self._session.query(f"ObjectType where name is {object_type_name}").one()

    def _get_security_roles(self) -> ftrack_api.entity.base.Entity:
        """
        Get all the security roles.

        This is to support the creation of CustomAttributeConfiguration objects.
        """
        return self._session.query("SecurityRole").all()

    # --------------- #
    # Utility methods #
    # --------------- #

    def _setup_logging(self, level: int) -> logging.Logger:
        """
        Setup logging for the app

        :param level: The logging level to use
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(level)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        logger.addHandler(console_handler)
        return logger


if __name__ == "__main__":
    sys.exit(main())
