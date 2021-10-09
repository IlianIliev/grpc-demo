import asyncio
import logging
import random
from collections import defaultdict

import grpc
import proto_pb2
import proto_pb2_grpc


SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = "50051"


DB = {"person": {}, "contacts": defaultdict(lambda: [])}


class AddressBookServicer:
    async def CreatePerson(self, request, context):
        # request is a Person object as defined in the proto file
        # so we use it directly
        request.id = random.randint(1, 1000)
        DB["person"][request.id] = request
        return DB["person"][request.id]

    async def GetPerson(self, request, context):
        if request.id not in DB["person"]:
            context.set_details("Not found")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return

        await asyncio.sleep(5)
        return proto_pb2.FullPersonResponse(
            person=DB["person"][request.id], contacts=DB["contacts"][request.id]
        )

    async def CreateContact(self, request, context):
        request.id = random.randint(1, 1000)
        DB["contacts"][request.person_id].append(request)

        return request


def make_server():
    server = grpc.aio.server()
    proto_pb2_grpc.add_AddressBookServicer_to_server(AddressBookServicer(), server)
    server.add_insecure_port("{}:{}".format(SERVER_ADDRESS, SERVER_PORT))

    return server


async def start_graceful_shutdown(server):
    logging.info("Starting graceful shutdown...")
    # Shuts down the server with 10 seconds of grace period. During the
    # grace period, the server won't accept new connections and allow
    # existing RPCs to continue within the grace period.
    await server.stop(10)
    logging.info("Graceful shutdown completed")


async def serve(server):
    await server.start()
    logging.info(f"Server running at {SERVER_ADDRESS}:{SERVER_PORT}")

    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    server = make_server()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(serve(server))
    finally:
        loop.run_until_complete(start_graceful_shutdown(server))
        loop.close()
