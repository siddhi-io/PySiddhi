# Copyright (c) 2016, WSO2 Inc. (http://www.wso2.org) All Rights Reserved.
#
# WSO2 Inc. licenses this file to you under the Apache License,
# Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

import os
from subprocess import check_call
from setuptools import setup, find_packages
from setuptools.command.install import install


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        # Compile JAVA Code here
        if os.name == "nt":
            check_call("mvn clean install".split(), cwd="__PySiddhi4Proxy",
                       shell=True)  # shell=True is necessary for windows
        else:
            check_call("mvn clean install".split(), cwd="__PySiddhi4Proxy")  # shell=True should be skipped for linux

        install.run(self)


packages = find_packages()
filtered_packages = []
for package in packages:
    if package.startswith("Tests"):
        continue
    filtered_packages.append(package)

setup(
    name="PySiddhi4",
    version="0.1.dev",
    packages=filtered_packages,
    install_requires=["pyjnius", "future"],
    package_data={
        "PySiddhi4": ["../__PySiddhi4Proxy/target/lib/*.jar",
                      "../__PySiddhi4Proxy/target/*.jar",
                      "../__PySiddhi4Proxy/*.so"]
    },

    # metadata for upload to PyPI
    author="WSO2",
    author_email="dev@wso2.org",
    description="Distribution of Siddhi CEP Python Wrapper",
    license="Apache2",
    cmdclass={
        'install': PostInstallCommand,
    },
    url="https://github.com/wso2/PySiddhi",
)
