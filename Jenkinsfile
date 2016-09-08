node {
  stage "Build"
  checkout scm
  sh "docker build --tag tracon/kompassi:build-${env.BUILD_NUMBER} ."
}
