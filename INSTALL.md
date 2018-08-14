                Installation instructions for CAV ETL
                =====================================

***TBD: These installation instructions are still to be written.***

## Docker
There is very little setup required. If Docker works on your system, change into the root directory of this project and run:

$ docker-compose -p cavetl up --build

This command will build and run the full Docker setup for both the dmf and leie repositories.

leie will now serve on local port 5000
dmf will serve on local port 5001