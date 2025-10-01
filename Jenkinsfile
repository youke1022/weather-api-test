pipeline {
    agent any

    stages {
        // =============================================
        // 阶段 1：拉取 GitHub 代码（可选保留）
        // =============================================
        stage('拉取 GitHub 代码') {
            steps {
                script {
                    echo "检查 api-test 目录是否存在..."
                    if (fileExists('api-test')) {
                        echo "api-test 目录已存在，跳过克隆环节"
                    } else {
                        echo "api-test 目录不存在，开始克隆 GitHub 代码..."
                        bat '''
                            git clone https://github.com/youke1022/weather-api-test %WORKSPACE%
                        '''
                        echo "代码拉取完成，api-test 文件夹已复制到工作空间"
                    }
                }
            }
        }

        // =============================================
        // 阶段 2：验证 Jenkins 是否能连接并操作 Docker
        // =============================================
        stage('验证 Docker 连接性') {
            steps {
                script {
                    echo "=============================================="
                    echo "开始验证 Jenkins 是否能连接并操作 Docker ..."
                    echo "=============================================="

                    bat '''
                        @echo off
                        echo [DEBUG] ===== 开始执行 Docker 连接性验证脚本 =====
                        
                        REM ======================
                        REM STEP 1: 检查 Docker 版本（验证客户端与服务端通信）
                        REM ======================
                        echo [STEP 1] 执行 docker version...
                        docker version
                        echo [DEBUG] docker version 执行完毕，返回码: %errorlevel%

                        REM ======================
                        REM STEP 2: 查看 Docker 系统信息
                        REM ======================
                        echo [STEP 2] 执行 docker info...
                        docker info
                        echo [DEBUG] docker info 执行完毕，返回码: %errorlevel%

                        REM ======================
                        REM STEP 3: 列出所有容器（包括停止的）
                        REM ======================
                        echo [STEP 3] 执行 docker ps -a...
                        docker ps -a
                        echo [DEBUG] docker ps -a 执行完毕，返回码: %errorlevel%

                        REM ======================
                        REM STEP 4: 拉取一个公共测试镜像（hello-world）
                        REM ======================
                        echo [STEP 4] 执行 docker pull hello-world...
                        docker pull hello-world
                        echo [DEBUG] docker pull hello-world 执行完毕，返回码: %errorlevel%

                        REM ======================
                        REM STEP 5: 列出所有本地镜像
                        REM ======================
                        echo [STEP 5] 执行 docker images...
                        docker images
                        echo [DEBUG] docker images 执行完毕，返回码: %errorlevel%

                        REM ======================
                        REM 验证结束
                        REM ======================
                        echo [DEBUG] ===== 所有 Docker 验证步骤执行完毕！=====
                    '''

                    echo "=============================================="
                    echo "Docker 连接性验证阶段执行完成，请查看上述输出！"
                    echo "=============================================="
                }
            }
        }
    }

    // 可根据需要添加 post 构建动作，如 always、success、failure 等
    post {
        always {
            echo "Pipeline 执行完毕（无论成功或失败）。"
        }
        success {
            echo "✅ Docker 连接性验证成功！可继续后续操作。"
        }
        failure {
            echo "❌ Docker 连接性验证失败！请检查上述日志。"
        }
    }
}
