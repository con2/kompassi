def imageMap = [
  "development": "staging",
  "master": "latest"
]

def environmentNameMap = [
  "master": "production",
  "development": "staging"
]

def tag = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
def environmentName = environmentNameMap[env.BRANCH_NAME]

def buildImage = "tracon/kompassi2-build:${tag}"

def tempStaticImage = "tracon/kompassi2:${tag}"
def finalStaticImage = "tracon/kompassi2:${imageMap[env.BRANCH_NAME]}"


node {
  stage("Build") {
    checkout scm
    sh "docker build --tag $buildImage ."
    sh ". $HOME/.kompassi2.env && docker build --file Dockerfile.static --build-arg FRONTEND_IMAGE=$buildImage --build-arg PUBLIC_URL=\$PUBLIC_URL --build-arg REACT_APP_KOMPASSI_BASE_URL=\$REACT_APP_KOMPASSI_BASE_URL --build-arg REACT_APP_CLIENT_ID=\$REACT_APP_CLIENT_ID --tag $tempStaticImage ."
  }

  stage("Push") {
    sh """
      docker rmi $buildImage && \
      docker tag $tempStaticImage $finalStaticImage && \
      docker push $finalStaticImage && \
      docker push $tempStaticImage && \
      docker rmi $tempStaticImage
    """
  }

  stage("Deploy") {
    if (env.BRANCH_NAME == "development") {
      // Kubernetes deployment
      sh """
        emrichen kubernetes/template.in.yml \
          -f kubernetes/${environmentName}.vars.yml \
          -D kompassi2_tag=${tag} | \
        kubectl apply -n conikuvat-${environmentName} -f -
      """
    } else {
      git url: "git@github.com:tracon/ansible-tracon"
      sh """
        ansible-playbook \
          --vault-password-file=~/.vault_pass.txt \
          --user root \
          --limit neula.kompassi.eu \
          --tags kompassi2-deploy \
          tracon.yml
      """
    }
  }
}
