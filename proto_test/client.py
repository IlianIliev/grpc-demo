import json

import grpc
import proto_pb2
import proto_pb2_grpc


class AddressBookClient:
    GRPC_RETRY_METHODS = (
        "CreatePerson",
        "GetPerson",
    )
    GRPC_RETRY_POLICY = {
        "maxAttempts": 3,
        "initialBackoff": "0.1s",
        "maxBackoff": "1s",
        "backoffMultiplier": 3,
        "retryableStatusCodes": [
            grpc.StatusCode.UNAVAILABLE.name,
            grpc.StatusCode.UNKNOWN.name,
        ],
    }

    GRPC_METHOD_CONFIG = {
        "methodConfig": [
            {
                "name": [
                    {
                        "service": f"{proto_pb2.DESCRIPTOR.package}.AddressBook",
                        "method": method,
                    }
                    for method in GRPC_RETRY_METHODS
                ],
                "retryPolicy": GRPC_RETRY_POLICY,
            },
        ],
    }
    GRPC_OPTIONS = (
        ("grpc.service_config", json.dumps(GRPC_METHOD_CONFIG)),
        ("grpc.enable_retries", True),
    )

    def __init__(self, server_address):
        self.server_address = server_address

    async def create_person(self, first_name, last_name):
        async with grpc.aio.insecure_channel(
            self.server_address, options=self.GRPC_OPTIONS
        ) as channel:
            stub = proto_pb2_grpc.AddressBookStub(channel)
            res = await stub.CreatePerson(
                proto_pb2.Person(first_name=first_name, last_name=last_name)
            )
            return res

    async def create_contact(self, person_id, type, value):
        async with grpc.aio.insecure_channel(
            self.server_address, options=self.GRPC_OPTIONS
        ) as channel:
            stub = proto_pb2_grpc.AddressBookStub(channel)
            res = await stub.CreateContact(
                proto_pb2.Contact(person_id=person_id, type=type, value=value)
            )

            return res

    async def get_person(self, person_id):
        async with grpc.aio.insecure_channel(
            self.server_address, options=self.GRPC_OPTIONS
        ) as channel:
            stub = proto_pb2_grpc.AddressBookStub(channel)
            try:
                res = await stub.GetPerson(proto_pb2.PersonId(id=person_id))
                return res
            except grpc.aio.AioRpcError as error:
                if error.code() == grpc.StatusCode.NOT_FOUND:
                    # person not found
                    return None
                else:
                    # something went wrong
                    raise error
