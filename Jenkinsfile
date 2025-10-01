pipeline {
    agent any
    tools {
        dockerTool 'docker1' // 使用已配置的Docker工具
    }
    
    parameters {
        string(name: 'CONTAINER_NAME', defaultValue: 'api-test', description: '要创建/管理的Docker容器名称')
        string(name: 'IMAGE_NAME', defaultValue: 'python:3.9-slim', description: '基础Docker镜像')
        string(name: 'GITHUB_REPO', defaultValue: 'https://github.com/youke1022/weather-api-test.git', description: 'GitHub仓库地址')
    }
    
    environment {
        WORKSPACE_MOUNT = "${WORKSPACE}/api-test:/app"
        CONTAINER_PORT = "8000:8000" // 如果需要端口映射可以取消注释
    }
    
    stages {
        stage('拉取GitHub代码') {
            steps {
                git url: params.GITHUB_REPO, branch: 'main'
                echo "代码拉取完成，api-test文件夹已复制到工作空间"
            }
        }
        
        stage('管理Docker容器') {
            steps {
                script {
                    def containerName = params.CONTAINER_NAME
                    def image = docker.image(params.IMAGE_NAME)
                    
                    echo "正在检查容器 ${containerName} 的状态..."
                    
                    try {
                        // 尝试获取容器对象
                        def container = docker.containerInspect(containerName)
                        
                        if (container) {
                            def status = container.state.status
                            echo "发现现有容器 ${containerName}，当前状态: ${status}"
                            
                            if (status == "running") {
                                echo "容器已在运行，无需操作"
                            } else {
                                echo "容器处于停止状态(${status})，正在尝试启动..."
                                container.start()
                                echo "容器启动成功"
                            }
                        } else {
                            echo "未找到名为 ${containerName} 的容器，将创建新容器"
                            image.run(
                                '-d',
                                '--name', containerName,
                                '-v', WORKSPACE_MOUNT,
                                // 如果需要端口映射:
                                // '-p', CONTAINER_PORT,
                                'tail', '-f', '/dev/null'
                            )
                            echo "容器 ${containerName} 创建并启动成功"
                        }
                    } catch (Exception e) {
                        error "容器管理失败: ${e.getMessage()}"
                    }
                }
            }
        }
        
        stage('安装依赖并测试') {
            steps {
                script {
                    def containerName = params.CONTAINER_NAME
                    
                    try {
                        echo "进入容器安装Python依赖..."
                        docker.container(containerName).inside {
                            sh 'pip install --upgrade pip'
                            sh 'pip install -r /app/requirements.txt'
                        }
                        
                        echo "执行pytest测试..."
                        def testResult = docker.container(containerName).inside {
                            sh(script: 'cd /app && pytest --junitxml=/app/test-results.xml', returnStatus: true)
                        }
                        
                        // 归档测试结果
                        junit '**/test-results.xml'
                        
                        if (testResult != 0) {
                            error "测试执行失败，退出码: ${testResult}"
                        }
                    } finally {
                        echo "测试阶段完成"
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo "清理工作空间..."
            cleanWs()
            echo "流水线执行完毕"
        }
        
        success {
            echo "✅ 所有阶段成功完成"
        }
        
        failure {
            echo "❌ 流水线执行失败，请检查日志"
        }
    }
}
