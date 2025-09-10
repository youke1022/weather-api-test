pipeline {
    agent any
    stages {
        stage('拉取GitHub代码') {
            steps {
                script {
                    echo "检查api-test目录是否存在..."
                    // 使用Jenkins内置的fileExists步骤判断目录是否存在（相对路径基于WORKSPACE）
                    if (fileExists('api-test')) {
                        echo "api-test目录已存在，跳过克隆环节"
                    } else {
                        echo "api-test目录不存在，开始克隆GitHub代码..."
                        bat ''' git clone https://github.com/youke1022/weather-api-test %WORKSPACE% '''
                        echo "代码拉取完成，api-test文件夹已复制到工作空间"
                    }
                }
            }
        }
        stage('创建并启动api-test容器') {
            steps {
                script {
                    echo "停止并删除已存在的api-test容器（如果存在）..."
                    bat ''' docker stop api-test || true && docker rm api-test || true '''
                    echo "创建并启动api-test容器..."
                    bat ''' docker run -d ^
                        --name api-test ^
                        -v %WORKSPACE%/api-test:/app ^
                        python:3.9-slim ^
                        tail -f /dev/null '''
                    echo "容器启动成功，api-test文件夹已挂载到/app目录"
                }
            }
        }
        stage('安装依赖并执行pytest') {
            steps {
                script {
                    echo "进入容器并安装依赖..."
                    bat "docker exec api-test sh -c \"pip install -r /app/requirement.txt\""
                    echo "依赖安装完成，执行pytest测试..."
                    bat "docker exec api-test sh -c \"cd /app && pytest\""
                    echo "pytest执行完成"
                }
            }
        }
    }
}
