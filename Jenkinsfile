def imageMap = [
  "development": "staging",
  "master": "latest"
]

def deploymentTagMap = [
  "master": "kompassi-production"
]

def environmentNameMap = [
  "master": "production",
  "development": "staging"
]

def tag = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"

def tempImage = "tracon/kompassi:${tag}"
def finalImage = "tracon/kompassi:${imageMap[env.BRANCH_NAME]}"

def tempStaticImage = "tracon/kompassi-static:${tag}"
def finalStaticImage = "tracon/kompassi-static:${imageMap[env.BRANCH_NAME]}"

def environmentName = environmentNameMap[env.BRANCH_NAME]


stage("Build") {
  node {
    checkout scm
    sh "docker build --tag ${tempImage} ."
  }
}

stage("Test") {
  node {
    sh """
      docker run \
        --rm \
        --link jenkins.tracon.fi-postgres:postgres \
        --env-file ~/.kompassi.env \
        --entrypoint "" \
        ${tempImage} \
        python manage.py test --keepdb
    """
  }
}

stage("Push") {
  node {
    sh "docker tag ${tempImage} ${finalImage} && docker push ${finalImage} && docker push ${tempImage}"
  }
}

stage("Static") {
  node {
    sh """
      docker build \
        --build-arg KOMPASSI_IMAGE=${tempImage} \
        --tag ${tempStaticImage} \
        --file Dockerfile.static . && \
      docker push ${tempStaticImage} && \
      docker tag ${tempStaticImage} ${finalStaticImage} && \
      docker push ${finalStaticImage}
    """
  }
}

stage("Deploy") {
  node {
    if (env.BRANCH_NAME == "development") {
      // Kubernetes deployment
      sh """
        emrichen kubernetes/template.in.yml \
          -f kubernetes/${environmentName}.vars.yml \
          -D kompassi_tag=${tag} | \
        kubectl apply -n kompassi-${environmentName} -f -
      """
    } else {
      // Legacy deployment
      git url: "git@github.com:tracon/ansible-tracon"
      sh """
        ansible-playbook \
          --vault-password-file=~/.vault_pass.txt \
          --user root \
          --limit neula.kompassi.eu \
          --tags ${deploymentTagMap[env.BRANCH_NAME]} \
          tracon.yml
      """
    }
  }
}

stage("Cleanup") {
  node {
    sh """
      docker rmi ${tempStaticImage} && \
      docker rmi ${tempImage}
    """
  }
}
