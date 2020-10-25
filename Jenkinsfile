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

def tempImage = "harbor.con2.fi/con2/${appName}:${tag}"
def finalImage = "harbor.con2.fi/con2/${appName}:${imageMap[env.BRANCH_NAME]}"

def tempStaticImage = "harbor.con2.fi/con2/${appName}-static:${tag}"
def finalStaticImage = "harbor.con2.fi/con2/${appName}-static:${imageMap[env.BRANCH_NAME]}"



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
