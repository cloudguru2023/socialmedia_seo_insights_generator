pipeline {
    agent any
    environment {
        DOCKER_HUB_REPO = "oogu2020/evolue-seo"    
        DOCKER_HUB_CREDENTIALS_ID = "docker-hub-token"
        IMAGE_TAG = "v${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout Github') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/cloudguru2023/socialmedia_seo_insights_generator']])
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    dockerImage = docker.build("${DOCKER_HUB_REPO}:${IMAGE_TAG}")
                }
            }
        }

        stage('Push Image to DockerHub') {
            steps {
                script {
                    echo 'Pushing Docker image to DockerHub...'
                    docker.withRegistry('https://registry.hub.docker.com' , "${DOCKER_HUB_CREDENTIALS_ID}") {
                    dockerImage.push("${IMAGE_TAG}")
                    }
                }
            }
        }

        stage('Update Deployment YAML with New Tag') {
            steps {
                script {
                    sh """
                        sed -i 's|image: oogu2020/evolvue-seo:.*|image: oogu2020/evolvue-seo:${IMAGE_TAG}|' manifests/deployment.yaml
                    """ 
                }
            }
        }

        stage('Commit Updated YAML') {
            steps {
                script {
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'github-token',
                            usernameVariable: 'GIT_USER',
                            passwordVariable: 'GIT_PASS'
                        )
                    ]) {
                        sh '''
                        git config --global user.email "[thecloudguru2023@gmail.com]"
                        git config --global user.name "cloudguru2023"
                        git add manifests/deployment.yaml
                        git commit -m "Update image tag to ${IMAGE_TAG}"
                        git push https://${GIT_USER}:${GIT_PASS}@github.com/cloudguru2023/socialmedia_seo_insights_generator.git
                        '''

                    }
                }
            }
        }

        stage('Install Kubectl & ArgoCD CLI Setup') {
            steps {
            }
        }

        stage('Apply Kubernetes & Sync App with ArgoCD') {
            steps {
                script {
                }
            }
        }
        

    }
}