import subprocess
import os

def install_docker():
    try:
        update_process = subprocess.run(['sudo', 'apt', 'update'], check=True)
        if update_process.returncode == 0:
            print("Обновление пакетов успешно завершено.")
        else:
            print("Ошибка при обновлении пакетов.")

        install_process = subprocess.run(['sudo', 'apt', 'install', '-y', 'docker.io'], check=True)
        if install_process.returncode == 0:
            print("Установка Docker успешно завершена.")
        else:
            print("Ошибка при установке Docker.")

        start_docker_process = subprocess.run(['sudo', 'systemctl', 'start', 'docker'], check=True)
        if start_docker_process.returncode == 0:
            print("Docker успешно запущен.")
        else:
            print("Ошибка при запуске Docker.")

        enable_docker_process = subprocess.run(['sudo', 'systemctl', 'enable', 'docker'], check=True)
        if enable_docker_process.returncode == 0:
            print("Docker включен в автозагрузку.")
        else:
            print("Ошибка при включении Docker в автозагрузку.")

    except subprocess.CalledProcessError as e:
        print(f"Произошла ошибка: {e}")


def run_portainer_container():
    try:
        subprocess.run(['sudo', 'docker', 'run', '-d', '-p', '9000:9000', '--name', 'portainer','-v', '/var/run/docker.sock:/var/run/docker.sock', 'portainer/portainer'])
        print("Контейнер Portainer успешно запущен.")
    except Exception as e:
        print(f"Ошибка при запуске контейнера Portainer: {e}")

def run_grafana_container():
    try:
        subprocess.run(['sudo', 'docker', 'run', '-d', '-p', '3000:3000', '--name', 'grafana', 'grafana/grafana:8.5.3'])
        print("Контейнер Grafana успешно запущен.")
    except Exception as e:
        print(f"Ошибка при запуске контейнера Grafana: {e}")

def run_prometheus_container():
    try:
        subprocess.run(['sudo', 'docker', 'run', '-d', '-p', '9090:9090', '--name', 'prometheus', '-v', 'prom-data:/prometheus', '-v', 'prom-configs:/etc/prometheus', 'prom/prometheus:v2.36.0'])
        print("Контейнер Prometheus успешно запущен.")
    except Exception as e:
        print(f"Ошибка при запуске контейнера Prometheus: {e}")

def run_blackbox_container():
    try:
        current_dir = os.getcwd()
        subprocess.run(['docker', 'run', '-d', '--name', 'blackbox', '--hostname', 'blackbox', '-p', '9115:9115', '-v', f'{current_dir}/blackbox:/etc/blackbox', 'prom/blackbox-exporter', '--config.file=/etc/blackbox/blackbox.yml'])
        print("Контейнер blackbox_exporter успешно запущен.")
    except Exception as e:
        print(f"Ошибка при запуске контейнера blackbox_exporter: {e}")

def crate_blackbox_config():
    try:
        current_dir = os.getcwd()
        subprocess.run(['sudo', 'cp', 'blackbox.yml', f'{current_dir}/blackbox/blackbox.yml'])
        print("blackbox.yml был скопирован")
    except Exception as e:
        print(f"Ошибка при копировании blackbox.yml: {e}")

def crate_prometheus_config():
    try:
        subprocess.run(['sudo', 'rm', '-rf', '/var/lib/docker/volumes/prom-configs/_data/prometheus.yml'])
        print("Удален старый конфиг prometheus")
        subprocess.run(['sudo', 'cp', 'prometheus.yml', '/var/lib/docker/volumes/prom-configs/_data/prometheus.yml'])
        print("Нужный конфиг скопирован.")
    except Exception as e:
        print(f"Ошибка при копировании prometheus.yml: {e}")

def restart_blackbox_n_prometheus():
    try:
        subprocess.run(['sudo', 'docker', 'container', 'restart', 'prometheus', 'blackbox'])
        print("Рестарт контейнеров.")
    except Exception as e:
        print(f"Ошибка при рестарте контейнеров: {e}")



if __name__ == "__main__":
    install_docker()
    run_portainer_container()
    run_grafana_container()
    run_prometheus_container()
    run_blackbox_container()
    crate_blackbox_config()
    crate_prometheus_config()
    restart_blackbox_n_prometheus()