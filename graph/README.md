# Instructions for setting up Neo4J on Docker

## Install Docker

```
brew cask install docker
```

Now we can start docker

## Run Neo4J in Docker

```
docker run \
    --name testneo4j \
    -p7474:7474 -p7687:7687 \
    -d \
    -v $HOME/neo4j/data:/data \
    -v $HOME/neo4j/logs:/logs \
    -v $HOME/neo4j/import:/var/lib/neo4j/import \
    -v $HOME/neo4j/plugins:/plugins \
    --env NEO4J_AUTH=neo4j/test \ 
    neo4j:latest
```

Note : We are passing the user id and password to docker run command. Modify if required

```
--env NEO4J_AUTH=neo4j/test \ 
```

## Open Neo4j in browser 
We can now use neo4j in browser : `http://localhost:7474/browser/`
 
Default user id/password is neo4j/test, as passed in the `docker run` command.
