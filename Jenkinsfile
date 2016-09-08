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
