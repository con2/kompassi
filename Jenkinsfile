def appName = "kompassi"

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

def environmentName = environmentNameMap[env.BRANCH_NAME]
def namespace = "${appName}-${environmentName}"

def tag = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"

def tempImage = "tracon/${appName}:${tag}"
def finalImage = "tracon/${appName}:${imageMap[env.BRANCH_NAME]}"

def tempStaticImage = "tracon/${appName}-static:${tag}"
def finalStaticImage = "tracon/${appName}-static:${imageMap[env.BRANCH_NAME]}"



node {
  stage("Build") {
    checkout scm
    sh "docker build --tag ${tempImage} ."
  }

  stage("Test") {
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

  stage("Push") {
    sh "docker tag ${tempImage} ${finalImage} && docker push ${finalImage} && docker push ${tempImage}"
  }

  stage("Static") {
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

  stage("Setup") {
    if (env.BRANCH_NAME == "development") {
      sh """
        kubectl delete job/setup \
          -n ${namespace} \
          --ignore-not-found && \
        emrichen kubernetes/jobs/setup.in.yml \
          -f kubernetes/${environmentName}.vars.yml \
          -D ${appName}_tag=${tag} | \
        kubectl apply -n ${namespace} -f - && \
        kubectl wait --for condition=complete -n ${namespace} job/setup
      """
    }
  }

  stage("Deploy") {
    if (env.BRANCH_NAME == "development") {
      // Kubernetes deployment
      sh """
        emrichen kubernetes/template.in.yml \
          -f kubernetes/${environmentName}.vars.yml \
          -D ${appName}_tag=${tag} | \
        kubectl apply -n ${namespace} -f -
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

  stage("Cleanup") {
    sh """
      docker rmi ${tempStaticImage} && \
      docker rmi ${tempImage}
    """
  }
}
