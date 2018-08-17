from setuptools import setup, find_packages


runtime = set([
    'constraints',
    'pyyaml',
    'tabulate',
])


develop = set([
    'flake8',
    'pytest',
    'ipython',
])


if __name__ == "__main__":
    setup(
        name="musical_desks",
        version="0.0.1",
        description="Given a specification of constraints provides a seating chart that satisfies them.",
        long_description=open("README.md").read(),
        url="https://github.com/csams/musical-desks",
        author="Chris Sams",
        author_email="cwsams@gmail.com",
        packages=find_packages(),
        install_requires=list(runtime),
        package_data={'': ['LICENSE']},
        license='Apache 2.0',
        extras_require={
            'develop': list(runtime | develop),
        },
        include_package_data=True
    )
