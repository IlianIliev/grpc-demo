from proto_test.proto_pb2 import Person, Contact


person = Person(id=42, first_name="John", last_name="Doe")
contact = Contact(person_id=person.id, type="email", value="john_doe@example.org")
print("Person:\n", person)
print("-----\n")


# Method name here is confusing, it actually returns bytes
person_as_bytes = person.SerializeToString()
print("Person as string : ", person_as_bytes)

contact_as_bytes = contact.SerializeToString()
print("Contact as string: ", contact_as_bytes)

print("\n-----\n")

parsed_person = Person()
parsed_person.ParseFromString(person_as_bytes)
print("Parsed person:\n", parsed_person)

assert person == parsed_person

print("-----\n")

# Parsing a
parsed_contact = Contact()
parsed_contact.ParseFromString(person_as_bytes)
print("Parsing person data as contact:", parsed_contact)
