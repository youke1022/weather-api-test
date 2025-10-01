pipeline {
    agent any
    stages {
        stage('拉取 GitHub 代码') {
            steps {
                script {
                    echo "检查 api-test 目录是否存在..."
                    if (fileExists('api-test')) {
                        echo "api-test 目录已存在，跳过克隆环节"
                    } else {
                        echo "api-test 目录不存在，开始克隆 GitHub 代码..."
                        bat ''' git clone https://github.com/youke1022/weather-api-test %WORKSPACE% '''
                        echo "代码拉取完成，api-test 文件夹已复制到工作空间"
                    }
                }
            }
        }
        
        stage('创建并启动 api-test 容器') {
            steps {
                script {
                    echo "检查是否存在同名容器..."
                    bat '''
                        docker
                        ...
                }
            }
        }
    }
}
