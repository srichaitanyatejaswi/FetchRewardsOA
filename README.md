# FetchRewardsOA
This repo contains Fetchwards Online Assessment files.
This Project calculates the similarity between two texts i.e., If two sentences are exactly same then the similarity should be 1 or If no words are matching in the two sentences, then the similarity is 0
## Procedure
1. Ignored Puntuations
2. converted into vectors
3. Calculated Cosine Similarity
### Implemented two methods to calculate cosine similarity:
i) Occurences of words in the texts as vectors and Calculated Cosine Similarity
ii) TF-IDF vectors and then Cosine Similarity
#### Although TF-IDF does gives vectors when the Sample test cases given, In some cases(small similar sentences), It fails and throws exception error.
## Completed Requirements
1. Code Runs
2. Used only standard library
3. Built as Flask application in response to a POST request containing two texts
4. Dokcerized the Flask Application that can be built and run locally or pull from Dockerhub

## How to Run
1. Clone the github Repo and cd to that directory
##### Next step needs Docker to be installed on your system.
2. In Terminal "docker build --tag textsimilarity ."
3. docker run --publish 5000:5000 --detach --name ts textsimilarity
4. Open Browser and go to localhost:5000
5. Paste two sentences and Click Submit
##### To quit close the browser and press ctrl+c in terminal
##### To remove the container type in the terminal
1. Type "docker ps -a" and You can see a container with name ts. 
2. Copy the containerID and type "docker stop containerID"
3. To remove the container "docker rm --force ts"
