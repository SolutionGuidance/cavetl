                Installation instructions for CAV ETL
                =====================================

Each CAV ETL application runs as its own microservice.  (We do not
provide any orchestration yet, but will consider doing so as the set
of services grows.)

Each service is deployed in a fairly standard Python-y way: you
activate a Python virtualevn, install the requirements, and run.  See
the individual services for details:

* [LEIE](leie/README.md)
* [DMF](dmf/README.md)
