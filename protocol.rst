** THIS DOCUMENT IS A DRAFT **

Pynpoint Protocol
+++++++++++++++++

The Pynpoint protocol is simple, a request or respone hereafter refered to as R
must conform to the following format: 

R consists of a header(H) and a body(B) delimited by a newline. H consists of
a 4 byte protocol identifier, a single byte version, a 2 byte size, and an 
arbitrary length message type delimited by colons. B is arbitrary JSON 
corresponding to the message type.

Request Types
-------------

+----------------+----------------------------------+-----------------------------+
|  Request Type  |          Expected JSON           |        Response?            |
+----------------+----------------------------------+-----------------------------+
| hi!            | {'host':'address', 'port':port } | Any recipient responds hi!  |
+----------------+----------------------------------+-----------------------------+
| i_have         | {'type': export_type,            | Recipients respond with     |
|                |  'export': dict()}               | sha1 of json                |
+----------------+----------------------------------+-----------------------------+
| valid export types: interfaces, services, disks, hosts                          |
+----------------+----------------------------------+-----------------------------+
| heard_of?      | {query_type: value }             | Returns an i_have for value |
+----------------+----------------------------------+-----------------------------+
| valid query_types: 'host', 'service', 'disk'                                    |
+----------------+----------------------------------+-----------------------------+
