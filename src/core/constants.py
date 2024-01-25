from enum import StrEnum

AMQP_TOPIC_VERSION = "v1"


class AMQPRoutingKeys(StrEnum):
    AMQP_API_ORGANIZATIONS_CREATED_ROUTING_KEY = (
        f"kiwi-api.organizations.created.{AMQP_TOPIC_VERSION}"
    )
    AMQP_API_ORGANIZATIONS_DELETED_ROUTING_KEY = (
        f"kiwi-api.organizations.deleted.{AMQP_TOPIC_VERSION}"
    )
