pipeline {
    agent any
    stages {
        // 【可选】保留：拉取 GitHub 代码阶段
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

        // ✅ 新增：专门用于验证 Jenkins 是否能连接并操作 Docker 的阶段
        stage('验证 Docker 连接性') {
            steps {
                script {
                    echo "=============================================="
                    echo "开始验证 Jenkins 是否能连接并操作 Docker ..."
                    echo "=============================================="

                    // 1. 检查 Docker 版本（验证 docker 客户端和服务端通信）
                    bat '''
                        echo [STEP 1] 执行 docker version...
                        docker version
                    '''

                    // 2. 查看 Docker 系统信息
                    bat '''
                        echo [STEP 2] 执行 docker info...
                        docker info
                    '''

                    // 3. 列出当前所有 Docker 容器（查看是否有容器在运行）
                    bat '''
                        echo [STEP 3] 执行 docker ps -a...
                        docker ps -a
                    '''

                    // 4. （可选）拉取一个公共镜像，验证镜像拉取能力
                    bat '''
                        echo [STEP 4] 执行 docker pull hello-world...
                        docker pull hello-world
                    '''

                    // 5. （可选）列出所有镜像，验证是否拉取成功
                    bat '''
                        echo [STEP 5] 执行 docker images...
                        docker images
                    '''

                    echo "=============================================="
                    echo "Docker 连接性验证步骤执行完毕，请查看上方输出！"
                    echo "=============================================="
                }
            }
        }
    }
}
