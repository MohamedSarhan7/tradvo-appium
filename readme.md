## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

1. Install docker: https://docs.docker.com/get-docker/
2. Install docker compose: https://docs.docker.com/compose/install/
3. ensure kvm is enabled in your host machine and enabled you can check using `sudo kvm-ok`
### Installing

1. Clone the repository   `git clone https://github.com/mohamedsarhan7/tradvo-appium.git`
2. run `docker compose -f docker-compose.yaml up `
3. run migrate `docker compose run web python manage.py migrate`
4. create super user `docker compose run web python manage.py createsuperuser`

#### please makesure these ports are not in use [8000, 6080,3306,6379,4723]
### links

1. web <a href="http://localhost:8000/en/dashboard/">http://localhost:8000/en/login/</a>
2. admin <a href="http://localhost:8000/en/admin/">http://localhost:8000/en/admin/</a>
3. android emulator  <a href="http://localhost:6080"> http://localhost:6080 </a>  after multiple restarts android emulator maybe not showing  <a href="https://github.com/budtmo/docker-android/issues/365">https://github.com/budtmo/docker-android/issues/365</a>
4. apk file <a href="https://github.com/MohamedSarhan7/tradvo-appium/apk/base.apk">base.apk</a>