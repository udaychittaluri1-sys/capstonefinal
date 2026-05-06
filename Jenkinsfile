// ============================================
// Jenkins CI/CD Pipeline
// UI + API Hybrid Automation Framework
// ============================================

pipeline {
    agent any

    parameters {
        choice(name: 'BROWSER', choices: ['chrome', 'firefox', 'edge'], description: 'Browser for UI tests')
        choice(name: 'ENV', choices: ['dev', 'staging', 'production'], description: 'Target environment')
        booleanParam(name: 'HEADLESS', defaultValue: true, description: 'Run in headless mode')
        string(name: 'MARKERS', defaultValue: 'smoke', description: 'Pytest markers (smoke, regression, e2e, api, ui)')
        string(name: 'PARALLEL_WORKERS', defaultValue: '4', description: 'Number of parallel workers')
    }

    environment {
        TEST_ENV = "${params.ENV}"
        BROWSER = "${params.BROWSER}"
        HEADLESS = "${params.HEADLESS}"
        PYTHONPATH = "${WORKSPACE}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "Code checked out from ${env.GIT_URL}"
            }
        }

        stage('Setup Environment') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -m venv venv
                            . venv/bin/activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    } else {
                        bat '''
                            python -m venv venv
                            call venv\\Scripts\\activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    }
                }
            }
        }

        stage('API Health Check') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            . venv/bin/activate
                            python -c "import requests; r=requests.get('https://practice.expandtesting.com/notes/api/health-check'); print(f'API Status: {r.status_code}')"
                        '''
                    } else {
                        bat '''
                            call venv\\Scripts\\activate
                            python -c "import requests; r=requests.get('https://practice.expandtesting.com/notes/api/health-check'); print(f'API Status: {r.status_code}')"
                        '''
                    }
                }
            }
        }

        stage('Run Smoke Tests') {
            when { expression { params.MARKERS == 'smoke' || params.MARKERS == 'all' } }
            steps {
                script {
                    def cmd = "pytest tests/ -m smoke -v --alluredir=reports/allure-results --reruns=2 --reruns-delay=2"
                    runTests(cmd)
                }
            }
        }

        stage('Run API Tests') {
            when { expression { params.MARKERS.contains('api') || params.MARKERS == 'all' } }
            steps {
                script {
                    def cmd = "pytest tests/test_notes_api.py -v --alluredir=reports/allure-results -n ${params.PARALLEL_WORKERS} --reruns=1"
                    runTests(cmd)
                }
            }
        }

        stage('Run UI Tests') {
            when { expression { params.MARKERS.contains('ui') || params.MARKERS == 'all' } }
            steps {
                script {
                    def cmd = "pytest tests/test_login.py tests/test_notes_ui.py -v --alluredir=reports/allure-results --reruns=2"
                    runTests(cmd)
                }
            }
        }

        stage('Run E2E Tests') {
            when { expression { params.MARKERS.contains('e2e') || params.MARKERS == 'all' } }
            steps {
                script {
                    def cmd = "pytest tests/test_e2e.py -v --alluredir=reports/allure-results --reruns=2"
                    runTests(cmd)
                }
            }
        }

        stage('Run Full Regression') {
            when { expression { params.MARKERS == 'regression' || params.MARKERS == 'all' } }
            steps {
                script {
                    def cmd = "pytest tests/ -v --alluredir=reports/allure-results -n ${params.PARALLEL_WORKERS} --reruns=2 --reruns-delay=2"
                    runTests(cmd)
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                allure includeProperties: false, jdk: '', results: [[path: 'reports/allure-results']]
            }
        }
    }

    post {
        always {
            echo 'Archiving test artifacts...'
            archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
            junit testResults: 'reports/*.xml', allowEmptyResults: true
        }
        success {
            echo '✅ All tests PASSED!'
        }
        failure {
            echo '❌ Some tests FAILED. Check Allure report for details.'
        }
        cleanup {
            cleanWs()
        }
    }
}

// Helper function to run tests with venv activation
def runTests(String command) {
    if (isUnix()) {
        sh ". venv/bin/activate && ${command}"
    } else {
        bat "call venv\\Scripts\\activate && ${command}"
    }
}
