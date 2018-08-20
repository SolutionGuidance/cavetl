                Installation instructions for CAV ETL
                =====================================

Each CAV ETL application runs as its own microservice.  (We do not
provide any orchestration yet, but will consider doing so as the set
of services grows.)  Each service is deployed in a fairly standard
Python-y way: you activate a Python virtualevn, install the
requirements, and run.

You can run all the services via Docker -- see the corresponding
section below -- or run each service individually:

* [LEIE](leie/README.md)
* [DMF](dmf/README.md)

## Docker

If Docker is set up on your system, go to the root directory of this
project and run:

    $ docker-compose -p cavetl up --build

This will build and run the full Docker setup for both the LEIE and
DMF services.

* LEIE will serve on local port 5000
* DMF will serve on local port 5001
