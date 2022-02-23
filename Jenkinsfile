pipeline{
        agent any
        stages{
          // Start Stages
            stage('Setuo'){
                steps{
                    echo "Setting up the project"
                }
            }
               stage('Dependencies'){
                steps{
                    echo "Installing dependencies success!"
                }
            }
               stage('Build'){
                steps{
                    echo "Building project success!"
                }
            }
               stage('Testing'){
                steps{
                    echo "Running Tests. All test passed!"
                }
            }
               stage('Deploy'){
                steps{
                    echo "Deploying the project. Succes!"
                }
            }
            stage('Cleanup'){
                steps{
                    echo "Project files all cleaned up!"
                }
            }
        }
}
