image = "tracon/kompassi:build-${env.BUILD_NUMBER}"

stage("Build") {
  node {
    checkout scm
    sh "docker build --tag ${image} ."
  }
}

stage("Test") {
  node {
    sh '''
      docker run --rm ${image} \
        -e DEBUG=1 \
        python manage.py test --keepdb
    '''
  }
}
