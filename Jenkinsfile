pipeline {
    agent any
    stages {
        stage('拉取 GitHub 代码') {
            steps {
                script {
                    echo "检查 api-test 目录是否存在..."
                    // 使用 Jenkins 内置的 fileExists 步骤判断目录是否存在（相对路径基于 WORKSPACE）
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
                        @echo off
                        REM 使用 docker inspect 检查容器是否存在，重定向输出到空设备
                        docker inspect api-test >nul 2>&1
                        if %errorlevel% equ 0 (
                            echo 检测到同名容器，跳过容器创建
                        ) else (
                            echo 未检测到同名容器，开始创建容器...
                            docker run -d ^
                            --name api-test ^
                            -v %WORKSPACE%/api-test:/app ^
                            python:3.9-slim ^
                            tail -f /dev/null
                            echo 容器启动成功，api-test 文件夹已挂载到 /app 目录
                        )
                    '''
                }
            }
        }
        
        stage('安装依赖并执行 pytest') {
            steps {
                script {
                    echo "进入容器并安装依赖..."
                    bat "docker exec api-test sh -c \"pip install -r /app/requirement.txt\""
                    echo "依赖安装完成，执行 pytest 测试..."
                    bat "docker exec api-test sh -c \"cd /app && pytest\""
                    echo "pytest 执行完成"
                }
            }
        }
    }
}
