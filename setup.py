# Copyright (c) 2017, WSO2 Inc. (http://www.wso2.org) All Rights Reserved.
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
    version="1.0.0",
    packages=filtered_packages,
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    install_requires=["requests","pyjnius", "future", "enum34 ; python_version<'3.4'"],
    package_data={
        "PySiddhi4": ["../__PySiddhi4Proxy/target/lib/*.jar",
                      "../__PySiddhi4Proxy/target/*.jar",
                      "../__PySiddhi4Proxy/*.so"]
    },

    # metadata for upload to PyPI
    author="WSO2",
    author_email="dev@wso2.org",
    description="Python wrapper for `Siddhi 4.x.x`.",
    license="Apache2",
    cmdclass={
        'install': PostInstallCommand,
    },
    url="https://github.com/wso2/PySiddhi",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Java Libraries'
    ]
)
