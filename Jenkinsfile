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
                        @echo off
                        setlocal enabledelayedexpansion
                        
                        REM 检查容器是否存在
                        docker inspect api-test >nul 2>&1
                        if %errorlevel% equ 0 (
                            echo 检测到同名容器，获取运行状态...
                            REM 捕获容器状态（需启用延迟扩展）
                            for /f "delims=" %%i in (\'docker inspect --format="{{.State.Status}}" api-test 2^>nul\') do (
                                set "container_status=%%i"
                            )
                            
                            if "!container_status!" equ "running" (
                                echo 容器状态正常（运行中），跳过操作
                            ) else (
                                echo 容器状态为 !container_status!，尝试启动容器...
                                docker start api-test >nul 2>&1
                                if !errorlevel! equ 0 (
                                    echo 容器启动成功，状态已恢复为 running
                                ) else (
                                    echo 容器启动失败，执行重建流程...
                                    docker rm -f api-test >nul 2>&1
                                    echo 旧容器已删除，重新创建容器...
                                    docker run -d ^
                                    --name api-test ^
                                    -v %WORKSPACE%/api-test:/app ^
                                    python:3.9-slim ^
                                    tail -f /dev/null
                                    echo 新容器启动成功，api-test 文件夹已挂载到 /app 目录
                                )
                            )
                        ) else (
                            echo 未检测到同名容器，开始创建容器...
                            docker run -d ^
                            --name api-test ^
                            -v %WORKSPACE%/api-test:/app ^
                            python:3.9-slim ^
                            tail -f /dev/null
                            echo 容器启动成功，api-test 文件夹已挂载到 /app 目录
                        )
                        endlocal
                    '''
                }
            }
        }
        
        stage('安装依赖并执行 pytest') {
            steps {
                script {
                    echo "进入容器并安装依赖..."
                    bat "docker exec api-test sh -c \\\"pip install -r /app/requirement.txt\\\""
                    echo "依赖安装完成，执行 pytest 测试..."
                    bat "docker exec api-test sh -c \\\"cd /app && pytest\\\""
                    echo "pytest 执行完成"
                }
            }
        }
    }
}
