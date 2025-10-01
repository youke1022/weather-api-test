pipeline {
    agent any

    // ✅ 使用已配置的 Docker 工具（确保 Jenkins 全局工具配置中有一个名为 'docker1' 的 Docker 工具）
    tools {
        dockerTool 'docker1' // ⚠️ 请确保此名称与 Jenkins "Global Tool Configuration" → "Docker" 中配置的名称完全一致
    }

    environment {
        // 定义环境变量，便于维护和修改
        CONTAINER_NAME = "api-test"
        WORKSPACE_MOUNT = "${WORKSPACE}/api-test:/app"  // 挂载工作空间下的 api-test 目录到容器内的 /app
        IMAGE_NAME = "python:3.9-slim"                   // 使用的 Docker 镜像
    }

    stages {
        // ------------------------------------------
        // 阶段 1：拉取 GitHub 代码
        // ------------------------------------------
        stage('拉取GitHub代码') {
            steps {
                script {
                    echo "检查 api-test 目录是否存在..."
                    def apiTestDirExists = fileExists('api-test')
                    if (apiTestDirExists) {
                        echo "api-test 目录已存在，跳过克隆环节"
                    } else {
                        echo "api-test 目录不存在，开始克隆 GitHub 代码..."
                        git url: 'https://github.com/youke1022/weather-api-test.git', branch: 'main'
                        echo "代码拉取完成，api-test 文件夹已复制到工作空间"
                    }
                }
            }
        }

        // ------------------------------------------
        // 阶段 2：管理 Docker 容器（检查/创建/启动 api-test 容器）
        // ------------------------------------------
        stage('管理Docker容器') {
            steps {
                script {
                    echo "正在检查容器 '${CONTAINER_NAME}' 的状态..."

                    // 🔍 步骤 1：使用原生 docker 命令检查容器是否存在
                    def inspectExitCode = bat(
                        script: """
                            @echo off
                            docker inspect ${CONTAINER_NAME} >nul 2>&1
                            echo %errorlevel%
                        """,
                        returnStdout: true
                    ).trim()

                    def containerExists = inspectExitCode == '0'

                    if (containerExists) {
                        echo "✅ 容器 '${CONTAINER_NAME}' 存在，检查运行状态..."

                        // 🟢 步骤 2：获取容器运行状态
                        def status = bat(
                            script: """
                                @echo off
                                docker inspect --format='{{.State.Status}}' ${CONTAINER_NAME}
                            """,
                            returnStdout: true
                        ).trim()

                        echo "容器状态: ${status}"

                        if (status == "running") {
                            echo "容器正在运行，无需操作"
                        } else {
                            echo "容器未运行（状态: ${status}），尝试启动容器..."
                            bat """
                                docker start ${CONTAINER_NAME}
                            """
                            echo "容器已启动"
                        }
                    } else {
                        echo "❌ 容器 '${CONTAINER_NAME}' 不存在，将创建新容器..."
                        bat """
                            docker run -d \
                            --name ${CONTAINER_NAME} \
                            -v "${WORKSPACE_MOUNT}" \
                            ${IMAGE_NAME} \
                            tail -f /dev/null
                        """
                        echo "新容器 '${CONTAINER_NAME}' 创建并启动成功，api-test 文件夹已挂载到 /app 目录"
                    }
                }
            }
        }

        // ------------------------------------------
        // 阶段 3：进入容器，安装依赖并执行 pytest
        // ------------------------------------------
        stage('安装依赖并测试') {
            steps {
                script {
                    echo "进入容器 '${CONTAINER_NAME}' 并安装依赖..."
                    try {
                        // 🐍 进入容器并使用 pip 安装依赖
                        bat """
                            docker exec ${CONTAINER_NAME} sh -c "pip install --upgrade pip && pip install -r /app/requirements.txt"
                        """

                        echo "依赖安装完成，执行 pytest 测试..."
                        // 🧪 执行 pytest 并生成 JUnit 格式的测试报告
                        def testResult = bat(
                            script: """
                                docker exec ${CONTAINER_NAME} sh -c "cd /app && pytest --junitxml=test-results.xml"
                            """,
                            returnStatus: true
                        )

                        // 📊 归档测试结果，便于 Jenkins UI 展示
                        junit '**/test-results.xml'

                        if (testResult != 0) {
                            error "❌ pytest 执行失败，退出码: ${testResult}"
                        }

                        echo "✅ pytest 执行完成"
                    } catch (Exception e) {
                        error "❌ 执行测试时出错: ${e.getMessage()}"
                    }
                }
            }
        }
    }

    // ------------------------------------------
    // 流水线后置操作（清理与通知）
    // ------------------------------------------
    post {
        always {
            echo "🧹 清理工作空间..."
            cleanWs()
            echo "✅ 流水线执行完毕（无论成功或失败）"
        }

        success {
            echo "🎉 所有阶段成功完成！"
        }

        failure {
            echo "❌ 流水线执行失败，请检查上述日志"
        }
    }
}
