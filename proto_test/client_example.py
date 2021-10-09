import asyncio
import json

import protobuf_to_dict

from client import AddressBookClient


async def client_example():
    client = AddressBookClient(server_address="127.0.0.1:50051")

    print("Creating a new person")
    person = await client.create_person(first_name="John", last_name="Doe")
    print(f"Person created with ID: {person.id}\n")

    print("Creating person contacts")
    await client.create_contact(person.id, type="email", value="john_doe@example.org")
    await client.create_contact(person.id, type="phone", value="007")
    print("Two contacts created\n")

    print("Getting full person details")
    full_person = await client.get_person(person_id=person.id)
    full_person_dict = protobuf_to_dict.protobuf_to_dict(full_person)
    print(json.dumps(full_person_dict, indent=4))

    # unknown_user_response = await client.get_person(person_id=0)
    # assert unknown_user_response is None


if __name__ == "__main__":
    asyncio.run(client_example())
