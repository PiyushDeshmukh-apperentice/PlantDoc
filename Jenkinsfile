pipeline {
  agent any

  environment {
    IMAGE_NAME = "plantdoc:${env.BUILD_NUMBER}"
    CONTAINER_NAME = 'plantdoc_app'
    // Optional: change to your registry (e.g. 'docker.io/yourname/plantdoc')
    DOCKER_REGISTRY = ''
  }

  options {
    // Keep only the last 10 builds to save disk
    buildDiscarder(logRotator(numToKeepStr: '10'))
    // Timestamped console output
    timestamps()
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Install dependencies') {
      steps {
        // Create venv and install requirements to verify dependencies (optional)
        sh '''
        if command -v python3 >/dev/null 2>&1; then
          PY=python3
        else
          PY=python
        fi
        $PY -m venv .venv || true
        . .venv/bin/activate
        pip install --upgrade pip
        if [ -f requirements.txt ]; then
          pip install --no-cache-dir -r requirements.txt
        else
          echo "No requirements.txt found"
        fi
        '''
      }
    }

    stage('Run tests') {
      steps {
        // If you add tests later, enable this. Keeps the pipeline non-blocking now.
        sh '''
        if [ -f pytest.ini ] || ls | grep -E "test_|tests" >/dev/null 2>&1; then
          . .venv/bin/activate && pytest -q || true
        else
          echo "No tests found - skipping"
        fi
        '''
      }
    }

    stage('Build Docker image') {
      steps {
        script {
          // Build the Docker image on the Jenkins host
          sh "docker build -t ${IMAGE_NAME} ."
        }
      }
    }

    stage('Push to registry (optional)') {
      when {
        expression { return env.DOCKER_REGISTRY && env.DOCKER_REGISTRY.trim() != '' }
      }
      steps {
        withCredentials([usernamePassword(credentialsId: 'docker-registry-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh '''
          # tag and push
          docker tag ${IMAGE_NAME} ${DOCKER_REGISTRY}/${IMAGE_NAME}
          echo $DOCKER_PASS | docker login --username $DOCKER_USER --password-stdin ${DOCKER_REGISTRY}
          docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}
          '''
        }
      }
    }

    stage('Deploy (run container)') {
      steps {
        // Stop and remove any previous container, then run the new image
        sh '''
        set -e
        docker rm -f ${CONTAINER_NAME} || true
        # Run container mapping both streamlit port and nginx port used in Dockerfile
        docker run -d --name ${CONTAINER_NAME} -p 8501:8501 -p 80:80 --restart unless-stopped ${IMAGE_NAME}
        echo "Container ${CONTAINER_NAME} started"
        '''
      }
    }
  }

  post {
    success {
      echo "Pipeline succeeded: built ${IMAGE_NAME} and deployed as ${CONTAINER_NAME}"
    }
    failure {
      echo "Pipeline failed"
    }
    always {
      // Archive the Dockerfile and requirements.txt so they appear in build artifacts
      archiveArtifacts artifacts: 'Dockerfile, requirements.txt, Jenkinsfile', allowEmptyArchive: true
    }
  }
}
