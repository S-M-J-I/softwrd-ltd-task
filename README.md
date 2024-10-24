# Vehicle Allocation Aystem

To run this project, clone the repository:
```sh
git clone https://github.com/S-M-J-I/softwrd-ltd-task
```
or use SSH
```sh
git clone git@github.com:S-M-J-I/softwrd-ltd-task.git
```

### Running the application

**NOTE: [Docker](https://docs.docker.com/engine/install/) must be installed for this step.**

#### Step 1: Enviroment vairables

Create a `.env` file and set the following environment variables:
```sh
MONGO_CONN_STR=
MONGO_DB=
```

*NOTE: The owner of this repository has deployed his database to a MongoDB Atlas Cluster. If you need access to it, feel free to reach out to him at [jishanlion@gmail.com](mailto:jishanlion@gmail.com)*

Open up the terminal pointing to the root directory and enter the command:
```sh
docker-compose build
```

Wait for the build to be finished. Next, run the app using the following command:
```sh
docker-compose up
```

#### Credits
Done by S M Jishanul Islam