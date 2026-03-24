pipeline {
    agent any

    stages {

        stage('Checkout Github') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/cloudguru2023/socialmedia_seo_insights_generator']])
            }
        }

        /*
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                }
            }
        }

        stage('Push Image to DockerHub') {
            steps {
                script {
                    echo 'Pushing Docker image to DockerHub...'
                }
            }
        }

        stage('Update Deployment YAML with New Tag') {
            steps {
                script {
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
        */

    }
}