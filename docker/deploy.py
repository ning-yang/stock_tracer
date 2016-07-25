import argparse
import subprocess
import signal
import sys

DOCKER_IMAGE = "ningy/stock_tracer"
DEPLOY_CMDS = {
    'backend_service': "docker run -d --link mysql-db:mysql --link mq-stock:rabbit --link elastic:elastic-host -v ~/app:/root/app --name {0} {1}:{2} service",
    'frontend_ui': "docker run -d --link mysql-db:mysql --link mq-stock:rabbit --link elastic:elastic-host -p 80:5000 -v ~/app:/root/app --name {0} {1}:{2} ui ",
    'worker': "docker run -d --link mysql-db:mysql --link mq-stock:rabbit --link elastic:elastic-host -v ~/app:/root/app --name {0} {1}:{2} worker",
}

def deploy_service(service, tag):
    print("stopping current services")
    execute_cmd("docker stop {}".format(service))

    print("removing current container")
    execute_cmd("docker rm {}".format(service))

    print("deploying new container")
    execute_cmd(DEPLOY_CMDS[service].format(service, DOCKER_IMAGE, tag))

    print("attaching to logger")
    execute_cmd("docker logs -f {}".format(service))

def execute_cmd(cmd):
    print("==> Start executing:\t{} ".format(cmd))
    result = subprocess.call(cmd, shell=True)
    print("==> Finish executing with return value:{}\n".format(result))

def signal_handler(signal, frame):
    print("Exiting deploy process...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(description='Deploy docker containers for stock_tracker')
    parser.add_argument('--service', help="back-end, front-end or worker", choices=DEPLOY_CMDS.keys(), required=True)
    parser.add_argument('--tag', help="docker image tag", default="latest")
    args = parser.parse_args()
    print("Start deploying service-{0}:{1}".format(args.service, args.tag))
    deploy_service(args.service, args.tag)
