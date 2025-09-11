pipeline {
    agent any
    stages {
        stage('拉取GitHub代码') {
            steps {
                script {
                    echo "检查 api-test 目录是否存在..."
                    // 使用 Jenkins 内置的 fileExists 步骤判断目录是否存在（相对路径基于 WORKSPACE）
                    if (fileExists('api-test')) {
                        echo "api-test 目录已存在，跳过克隆环节"
                    } else {
                        echo "api-test 目录不存在，开始克隆 GitHub 代码..."
                        bat '''
                            git clone https://github.com/youke1022/weather-api-test %WORKSPACE%\\api-test
                        '''
                        echo "代码拉取完成，api-test 文件夹已复制到工作空间"
                    }
                }
            }
        }

        stage('检查/创建并启动 api-test 容器') {
            steps {
                script {
                    echo "检查是否已有名为 api-test 的 Docker 容器....
                    def containerName = bat(script: 'docker ps -a --filter "name=api-test" --format "{{.Name}}"', returnStdout: true).trim()
                    if (containerName.contains("api-test")) {
                        echo "✅ 检测到同名容器 '${containerName}' 已存在，跳过容器创建，直接进入容器执行后续操作"
                    } else {
                        echo "❌ 未检测到名为 'api-test' 的容器，正在创建并启动..."
                        bat '''
                            docker run -d \
                                --name api-test \
                                -v %WORKSPACE%\\api-test:/app \
                                python:3.9-slim \
                                tail -f /dev/null
                        '''
                        echo "✅ 容器 'api-test' 启动成功，api-test 文件夹已挂载到 /app 目录"
                    }
                }
            }
        }

        stage('安装依赖并执行 pytest') {
            steps {
                script {
                    echo "进入容器 'api-test' 并安装依赖..."
                    bat '''
                        docker exec api-test sh -c "pip install -r /app/requirements.txt"
                    '''
                    echo "✅ 依赖安装完成，执行 pytest 测试..."
                    bat '''
                        docker exec api-test sh -c "cd /app && pytest"
                    '''
                    echo "✅ pytest 执行完成"
                }
            }
        }
    }
}
