def image = "tracon/kompassi:build-${env.BUILD_NUMBER}"

stage("Build") {
  node {
    checkout scm
    sh "docker build --tag ${image} ."
  }
}

stage("Test") {
  node {
    sh """
      docker run \
        --rm \
        --env DEBUG=1 \
        ${image} \
        python manage.py test --keepdb
    """
  }
}

stage("Push") {
  node {
    sh "docker tag ${image} tracon/kompassi:latest && docker push tracon/kompassi:latest"
  }
}

stage("Deploy") {
  node {
    git url: "git@github.com:tracon/ansible-tracon"
    sh """
      ansible-playbook \
        --vault-password-file=~/.vault_pass.txt \
        --user root \
        --limit neula.kompassi.eu \
        --tags kompassi-deploy \
        tracon.yml
    """
  }
}
