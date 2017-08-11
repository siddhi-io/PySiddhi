from subprocess import check_call

from setuptools import setup, find_packages
from setuptools.command.install import install


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        # Compile JAVA Code here
        check_call("mvn clean install".split(),cwd="__PySiddhi3Proxy", shell=True)

        install.run(self)


packages = find_packages()
filtered_packages = []
for package in packages:
    if package.startswith("Tests"):
        continue
    filtered_packages.append(package)

setup(
    name="PySiddhi3",
    version="0.1.dev",
    packages=filtered_packages,
    install_requires=["pyjnius","future"],

    package_data={"PySiddhi3": ["../__PySiddhi3Proxy/target/lib/*.jar",
                                 "../__PySiddhi3Proxy/target/*.jar",
                                 "../__PySiddhi3Proxy/*.so"]
                  },

    # metadata for upload to PyPI
    author="wso2",
    author_email="dev@wso2.org",
    description="Distribution of Siddhi CEP Python Wrapper",
    license="Apache2",
    cmdclass={
        'install': PostInstallCommand,
    },
    url="https://github.com/wso2/PySiddhi",
)
